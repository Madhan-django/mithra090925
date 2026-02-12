from django.shortcuts import redirect
from django.http import HttpResponse
from django.shortcuts import redirect
from staff.models import staff


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('institutions')
        elif request.user.is_authenticated == None:
            return redirect('login_user')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_authenticated:
                user_groups = [group.name for group in request.user.groups.all()]
                if any(group in allowed_roles for group in user_groups):
                    return view_func(request, *args, **kwargs)
                else:
                    # Displaying the user's group(s) in the unauthorized message
                    user_groups_str = ', '.join(user_groups)
                    return HttpResponse(f'You are not authorised. Your group(s): {user_groups_str}')
            else:
                return HttpResponse('You are not authorised')
                
        return wrapper_func
    return decorator

