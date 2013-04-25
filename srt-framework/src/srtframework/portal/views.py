from django.shortcuts import render, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from password_required.decorators import password_required
from portal.models import Participant
from datetime import datetime

@password_required
def agreement(request):
    return render(request, 'portal/agreement.html', {})

@password_required
def group(request):
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
        participant = Participant.objects.create_participant(group)
        request.session['participant'] = participant
        
    if request.session['participant'].group != 'c':
        page = render(request, 'portal/group.html', {'group': request.session['participant'].group})
    else: 
        page = render(request, 'portal/test.html', {})
    return page

@password_required
def test(request):
    return render(request, 'portal/test.html', {})

@password_required
def survey(request):
    participant = request.session['participant']    
    if (participant.id % 2) == 0:
        test_id = "PYDQRHK";
    else:    
        test_id = "T2YYKYX"
    address = 'http://www.surveymonkey.com/s/%s?c=%d' % (test_id, participant.id)
    return HttpResponseRedirect(address)

@password_required
def record(request):
    participant = request.session['participant']    
    date = datetime.now().strftime('%Y-%m-%d-%H-%s')
    file = open("srtframework/media/results/IAT_%s-%s.txt" % (participant.id, date), 'w')
    file.write(request.GET['data'])
    file.close()
    return render(request, 'portal/test.html', {})

@password_required
def confirmation(request):
    return render(request, 'portal/confirmation.html', {})