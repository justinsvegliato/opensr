from django.shortcuts import render, HttpResponseRedirect, redirect
from django.core.exceptions import ObjectDoesNotExist
from password_required.decorators import password_required
from portal.models import Participant
from datetime import datetime
from django.core.urlresolvers import reverse
import datetime
from django.utils.timezone import utc

#@decorator
#def check_if_finished(f, request):
#    if 'participant' in request.session:
#        participant = request.session['participant']
#        if participant.datetime_finished != None:
#            return redirect(reverse('confirmation'))
#    return f(request)

@password_required
def agreement(request): 
    if 'participant' in request.session:
        participant = request.session['participant']
        if participant.datetime_finished != None:
            return redirect(reverse('confirmation'))
        
    return render(request, 'portal/agreement.html', {})

@password_required
def group(request):
    if 'participant' in request.session:
        participant = request.session['participant']
        if participant.datetime_finished != None:
            return redirect(reverse('confirmation'))
    
    if not 'participant' in request.session:
        def get_next_group():
            GROUPS = ['t', 'p', 'c']
            try:
                latest_group = Participant.objects.latest('id').group
                latest_group_index = GROUPS.index(latest_group)
                if (latest_group_index + 1 < len(GROUPS)):
                    group = GROUPS[latest_group_index + 1]
                else:
                    group = GROUPS[0]
            except ObjectDoesNotExist:
                group = GROUPS[0]
            return group

        group = get_next_group()
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        participant = Participant.objects.create_participant(group, now)
        request.session['participant'] = participant    
        
    if request.session['participant'].group != 'c':
        object_context = {'group': request.session['participant'].group}
        page = render(request, 'portal/group.html', object_context)
    else: 
        page = redirect(reverse('test'))
    return page

@password_required
def test(request): 
    if 'participant' in request.session:
        participant = request.session['participant']
        if participant.datetime_finished != None:
            return redirect(reverse('confirmation'))
    
    return render(request, 'portal/test.html', {})

@password_required
def survey(request):   
    if 'participant' in request.session:
        participant = request.session['participant']
        if participant.datetime_finished != None:
            return redirect(reverse('confirmation'))    
    
    participant = request.session['participant']
    if (participant.id % 2) == 0:
        test_id = "PYDQRHK";
    else:    
        test_id = "T2YYKYX"
    address = 'http://www.surveymonkey.com/s/%s?c=%d' % (test_id, participant.id)
    return HttpResponseRedirect(address)

@password_required
def record(request):
    if 'participant' in request.session:
        participant = request.session['participant']
        if participant.datetime_finished != None:
            return redirect(reverse('confirmation'))
    
    participant = request.session['participant']        
    date = datetime.datetime.now().strftime('%Y-%m-%d-%H-%S')
    file = open("srtframework/media/results/IAT_%s-%s.txt" % (participant.id, date), 'w')
    file.write(request.GET['data'])
    file.close()
    return render(request, 'portal/test.html', {})

@password_required
def confirmation(request):
    participant = request.session['participant']
    participant.datetime_finished = datetime.datetime.utcnow().replace(tzinfo=utc)
    participant.save()
    return render(request, 'portal/confirmation.html', {})