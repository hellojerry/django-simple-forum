from django.contrib.auth.decorators import user_passes_test, login_required




active_required = user_passes_test(lambda u: u.profile.is_active,
                                   login_url = '/profiles/banned/banned/')
                
                
def active_and_login_required(view_function):
    return login_required(active_required(view_function),login_url='/login/')


    


