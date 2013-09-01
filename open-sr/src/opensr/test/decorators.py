from decorator import decorator
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

@decorator
def has_participant_id(f, request):
    if not 'participant' in request.session:
        return redirect(reverse('error'))
    return f(request)

@decorator
def has_completed_test(f, request):
    if not request.session['participant'].has_completed_test:
        return redirect(reverse('error'))
    return f(request)

@decorator
def has_not_completed_test(f, request):
    if request.session['participant'].has_completed_test:
        return redirect(reverse('error'))
    return f(request)