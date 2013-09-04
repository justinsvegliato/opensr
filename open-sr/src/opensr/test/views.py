from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from itertools import chain
from django.shortcuts import (render, redirect)
from test.models import (Test, ExperimentalGroup, Participant, Block, Category, ImageStimulus, TextStimulus, Trial)
from test.forms import (IndexLoginForm, EntranceLoginForm)
from test.decorators import (has_participant_id, has_completed_test, has_not_completed_test, has_no_participant_id, has_test_id)

@has_no_participant_id
def index(request):
    login_form = IndexLoginForm()    
    if request.POST:
        login_form = IndexLoginForm(request.POST)
        if login_form.is_valid():
            request.session['test'] = Test.objects.get(id=request.POST['test'])
            return redirect(reverse('informed_consent'))
        
    object_context = {'login_form': login_form}
    return render(request, 'test/index.html', object_context)

@has_no_participant_id
def entrance(request, test_id):
    login_form = EntranceLoginForm()    
    if request.POST:
        login_form = EntranceLoginForm(request.POST, test_id=test_id)
        if login_form.is_valid():
            request.session['test'] = Test.objects.get(id=test_id)
            return redirect(reverse('informed_consent'))
        
    object_context = {
    'login_form': login_form,
    'test_id': test_id
    }
    return render(request, 'test/entrance.html', object_context)   

@has_test_id
def informed_consent(request):
    object_context = {
        'flatpage': request.session['test'].informed_consent_page,
        'next_page_url': '/introduction/'
    }     
    context_instance = RequestContext(request)
    context_instance.autoescape=False    
    return render(request, 'flatpages/default.html', object_context, context_instance=context_instance)

@has_test_id
def introduction(request):
    page = request.session['test'].introduction_page
    if page:
        object_context = {
            'flatpage': page,
            'next_page_url': '/experimental-group/'
        } 
        context_instance = RequestContext(request)
        context_instance.autoescape=False
        return render(request, 'flatpages/default.html', object_context, context_instance=context_instance)
    else:
        return redirect(reverse('experimental-group'))

@has_test_id
def experimental_group(request):
    test = request.session['test']
    groups = ExperimentalGroup.objects.filter(test=test).order_by('id')
    
    if not 'participant' in request.session:
        def get_next_group():
            try:
                latest_group_id = Participant.objects.latest('id').experimental_group.id
                for i in range(len(groups)):
                    if groups[i].id == latest_group_id:
                       return groups[0] if (i == (len(groups) - 1)) else groups[i + 1]
            except ObjectDoesNotExist:
                return groups[0]

        group = get_next_group()
    
        participant = Participant.objects.create_participant(group, test)
        request.session['participant'] = participant
    else:
        group = request.session['participant'].experimental_group
                               
    if not group.page:
        return redirect(reverse('test'))
    
    object_context = {
        'flatpage': group.page,
        'next_page_url': '/test/'
    }
    context_instance = RequestContext(request)
    context_instance.autoescape=False    
    return render(request, 'flatpages/default.html', object_context, context_instance=context_instance)

@has_participant_id
@has_not_completed_test
def test(request):    
    def get_blocks(test):
        blocks = Block.objects.filter(test=test)    
        distinct_trials = Trial.objects.filter(participant=request.session['participant']).values('block').distinct()
        for distinct_trial in distinct_trials:
            block = blocks.get(block_name=distinct_trial['block'])
            block_trials = Trial.objects.filter(participant=request.session['participant'], block=distinct_trial['block'])
            if block.number_of_stimuli == block_trials.count():
                blocks = blocks.exclude(id=block.id)
            else:
                block_trials.delete()
        return blocks
    
    test = request.session['test']    
    blocks = get_blocks(test) 
                
    category_ids = []
    for block in blocks:
        category_ids.append(block.primary_left_category_id)
        category_ids.append(block.primary_right_category_id)
        if not block.primary_left_category_id is None:
            category_ids.append(block.secondary_left_category_id)
        if not block.secondary_right_category_id is None:
            category_ids.append(block.secondary_right_category_id)
          
    categories = Category.objects.filter(id__in=category_ids)   
    image_stimuli = ImageStimulus.objects.filter(category_id__in=category_ids)
    text_stimuli = TextStimulus.objects.filter(category_id__in=category_ids)
    stimuli = list(chain(image_stimuli, text_stimuli))
    
    context_instance = RequestContext(request)
    context_instance.autoescape=False    
    object_context = {
       'test': serializers.serialize('json', [test]),
        'blocks': serializers.serialize('json', blocks),
        'categories': serializers.serialize('json', categories),
        'stimuli': serializers.serialize('json', stimuli),
        'left_key_bind': test.left_key_bind.upper(),
        'right_key_bind': test.right_key_bind.upper(),
        'next_page_url': '/confirmation/' if not test.survey_url else test.survey_url,
        'media_url': settings.MEDIA_URL,
    }  
    return render(request, 'test/test.html', object_context, context_instance=context_instance)

@has_participant_id
@has_completed_test
def confirmation(request):
    object_context = {
        'flatpage': request.session['test'].confirmation_page
    }     
    context_instance = RequestContext(request)
    context_instance.autoescape=False    
    return render(request, 'flatpages/default.html', object_context, context_instance=context_instance)

@has_participant_id
def record_trial(request):
    Trial.objects.create_result(
        request.session['test'], 
        request.session['participant'].experimental_group,
        request.GET['block'], 
        request.GET['practice'] == 'true', 
        request.GET['primary_left_category'], 
        request.GET['secondary_left_category'], 
        request.GET['primary_right_category'],
        request.GET['secondary_right_category'], 
        request.GET['stimulus'], 
        request.GET['latency'], 
        request.GET['correct'] == 'true', 
        request.session['participant']
    )
    return HttpResponse('OK')

@has_participant_id
def record_test_status(request):
    request.session['participant'].has_completed_test = (request.GET['test_status'] == 'true')
    request.session['participant'].save()
    return HttpResponse('OK')

def error(request):
    return render(request, 'test/error.html', {})