from django.http import HttpResponse
from django.shortcuts import redirect

# decorator is a function that takes another function as a parameter and lets
# us add a little extra functionality before the original function is called
def unauthenticated_user(view_func):

    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts-account')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func
