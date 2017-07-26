#the decorator
def myuser_login_required(f):
        def wrap(request, *args, **kwargs):
                #this check the session if userid key exist, if not it will redirect to login page
                if 'userid' not in request.session.keys():
                        return HttpResponseRedirect("/mysite/login")
                return f(request, *args, **kwargs)
        wrap.__doc__=f.__doc__
        wrap.__name__=f.__name__
        return wrap

#how you use this decorator is simple, same as the @login_required decorator
@myuser_login_required
def myuser_create(request):
         #blahblah here's how you create your user....
         #and you can make sure your user already logined.

#remember to register session id in your login function
#this is just a naive sample
import md5
def my_login(request):
         if request.POST:
                   try:
                          m = myuser.objects.filter(userid__exact=request.POST['userid'])
                          if str(m.get().password) == md5.md5(request.POST["password"]).hexdigest():
                                     request.session['userid'] = str(m.get().userid)
                          else:
                                     raise
                   except:
                                      return HttpResponseRedirect("/mysite/login")
