from decorator import decorator
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

@decorator
def has_participant_id(f, request):
    if not 'participant' in request.session:
        return get_redirection(request)  
    return f(request)

@decorator
def has_no_participant_id(f, request, *args):
    if 'participant' in request.session:
        return get_redirection(request)  
    return f(request) if len(args) == 0 else f(request, args[0])

@decorator
def has_completed_test(f, request):
    if not request.session['participant'].has_completed_test:
        return get_redirection(request)  
    return f(request)

@decorator
def has_not_completed_test(f, request):
    if request.session['participant'].has_completed_test:
        return get_redirection(request)  
    return f(request)

@decorator
def has_test_id(f, request):
    if not 'test' in request.session:
        return get_redirection(request)  
    return f(request)

@decorator
def has_no_test_id(f, request, *args):
    if 'test' in request.session:
        return get_redirection(request)
    return f(request) if len(args) == 0 else f(request, args[0])

def get_redirection(request):
    if 'test' in request.session:
        if 'participant' in request.session:
            return redirect(reverse('test'))  
        return redirect(reverse('informed_consent'))
    return redirect(reverse('index'))
    