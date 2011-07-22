from django.contrib.auth.decorators import login_required
from django.db.models.loading import cache
from django.http import HttpResponse, HttpResponseRedirect, \
    HttpResponseServerError
from follow.utils import follow as _follow, unfollow as _unfollow

def check(func):
    """ 
    Check the permissions, http method and login state.
    """
    def iCheck(request, *args, **kwargs):
        follow = func(request, *args, **kwargs)
        if request.is_ajax():
            return HttpResponse('ok')
        try:
            if 'next' in request.GET:
                return HttpResponseRedirect(request.GET.get('nex'))
            return HttpResponseRedirect(follow.target.get_absolute_url())
        except AttributeError:
            if 'HTTP_REFERER' in request.META:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            return HttpResponseServerError('"%s" object of type ``%s`` has no method ``get_absolute_url()``.' % (
                unicode(follow.get_object()), follow.get_object().__class__))
    return iCheck


@login_required
@check
def follow(request, app, model, id):
    model = cache.get_model(app, model)
    obj = model.objects.get(pk=id)
    return _follow(request.user, obj)

@login_required
@check
def unfollow(request, app, model, id):
    model = cache.get_model(app, model)
    obj = model.objects.get(pk=id)
    return _unfollow(request.user, obj)
