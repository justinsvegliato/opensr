from portal.forms import LoginForm
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.http import HttpResponse
from django.contrib.flatpages.models import FlatPage
from django.shortcuts import (
    render, redirect
)
from portal.models import (
    Test, Group, Participant, Block, Label, Anchor, Result
)

def index(request):
    login_form = LoginForm()    
    if request.POST:
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            request.session['test'] = Test.objects.get(id=request.POST['test'])
            return redirect(reverse('informed_consent'))
        
    object_context = {'login_form': login_form}
    return render(request, 'portal/index.html', object_context)

def informed_consent(request):
    object_context = {
        'flatpage': request.session['test'].informed_consent_page,
        'next_page_url': '/introduction/'
    }     
    context_instance = RequestContext(request)
    context_instance.autoescape=False    
    return render(request, 'flatpages/default.html', object_context, context_instance=context_instance)

def introduction(request):
    page = request.session['test'].introduction_page
    if page:
        object_context = {
            'flatpage': page,
            'next_page_url': '/group/'
        } 
        context_instance = RequestContext(request)
        context_instance.autoescape=False
        return render(request, 'flatpages/default.html', object_context, context_instance=context_instance)
    else:
        return redirect(reverse('group'))

def group(request):
    test = request.session['test']
    groups = Group.objects.filter(test=test).order_by('id')

    if not len(groups):
        return redirect(reverse('test'))
    
    def get_next_group():
        try:
            latest_group_id = Participant.objects.latest('id').group.id
            for i in range(len(groups)):
                if groups[i].id == latest_group_id:
                   return groups[0] if (i == (len(groups) - 1)) else groups[i + 1]
        except ObjectDoesNotExist:
            return groups[0]
    
    group = get_next_group()
    
    participant = Participant.objects.create_participant(group, test)
    request.session['participant'] = participant
    
    if not group.page:
        return redirect(reverse('test'))
    
    object_context = {
        'flatpage': group.page,
        'next_page_url': '/test/'
    }
    context_instance = RequestContext(request)
    context_instance.autoescape=False    
    return render(request, 'flatpages/default.html', object_context, context_instance=context_instance)

def test(request):
    test = request.session['test']
    blocks = Block.objects.filter(test=test)
    
    label_ids = []
    for block in blocks:
        label_ids.append(block.primary_left_label_id)
        label_ids.append(block.primary_right_label_id)
        if not block.primary_left_label_id is None:
            label_ids.append(block.secondary_left_label_id)
        if not block.secondary_right_label_id is None:
            label_ids.append(block.secondary_right_label_id)
    labels = Label.objects.filter(id__in=label_ids)
    
    anchors = Anchor.objects.filter(label_id__in=label_ids)
    
    context_instance = RequestContext(request)
    context_instance.autoescape=False    
    object_context = {
        'test': serializers.serialize('json', [test]),
        'blocks': serializers.serialize('json', blocks),
        'labels': serializers.serialize('json', labels),
        'anchors': serializers.serialize('json', anchors),
        'left_key_bind': test.left_key_bind.upper(),
        'right_key_bind': test.right_key_bind.upper(),
        'next_page_url': '/confirmation/' if not test.survey_url else test.survey_url
    }  
    return render(request, 'portal/test.html', object_context, context_instance=context_instance)

def confirmation(request):
    object_context = {
        'flatpage': request.session['test'].confirmation_page
    }     
    context_instance = RequestContext(request)
    context_instance.autoescape=False    
    return render(request, 'flatpages/default.html', object_context, context_instance=context_instance)

def record(request):
    Result.objects.create_result(
        request.GET['primary_left_label'], 
        request.GET['secondary_left_label'], 
        request.GET['primary_right_label'],
        request.GET['secondary_left_label'], 
        request.GET['anchor'], 
        request.GET['reaction_time'], 
        request.GET['correct'] == "true", 
        request.session['participant']
    )
    return HttpResponse('')