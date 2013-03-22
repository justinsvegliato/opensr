from django.shortcuts import render
from password_required.decorators import password_required
from models import Group, Participant

@password_required
def agreement(request):
    agreement = "Agreement goes here--most likely read from a file of some sort"
    objcontext = {'agreement': agreement}
    return render(request, 'iat/agreement.html', objcontext)
    
@password_required
def instructions(request):
    if not 'participant' in request.session:
        def get_next_group():
            try:
                latest_group_id = Participant.objects.latest('id').group_id
                group = Group.objects.filter(id__gt=latest_group_id).order_by('id')[0]
            except (Participant.DoesNotExist, IndexError):
                try:
                    group = Group.objects.order_by('id')[0]
                except IndexError:
                    # Redirect to error page
                    print "cat"
            return group

        group = get_next_group()
        participant = Participant.objects.create_participant(group)
        request.session['participant'] = participant
    
    title = request.session['participant'].group.title
    description = request.session['participant'].group.description
    
    objcontext = {'title': title, 'description': description}
    return render(request, 'iat/instructions.html', objcontext)

@password_required
def test(request):
    return render(request, 'iat/test.html', {})

@password_required
def survey(request):
    return render(request, 'iat/survey.html', {})

@password_required
def complete(request):
    return render(request, 'iat/complete.html', {})