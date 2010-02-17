from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.models import User 
from django import forms
from django.forms import ModelForm
from django.forms import widgets
from django.forms.util import ValidationError
import datetime, time
from django.contrib.auth.decorators import login_required
from djangovoice.models import Feedback
from djangovoice.forms import *
from djangovoice.utils import paginate
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

def detail(request, object_id):
    feedback = get_object_or_404(Feedback, pk=object_id)
    
    if feedback.private == True:
        if request.user.is_staff != True and request.user != feedback.user:
            return Http404
    
    return render_to_response('djangovoice/detail.html', {'feedback': feedback}, context_instance=RequestContext(request))


def list(request, list=False, type=False, status=False):
    feedback = Feedback.objects.all().order_by('-created')
    
    if not list:
        list = "open"
    
    title = _("Feedback")
    
    if list == "open":
        title = _("Open Feedback")
        feedback = feedback.filter(status__status='open')
    elif list == "closed":
        title = _("Closed Feedback")
        feedback = feedback.filter(status__status='closed')
    elif list == "mine":
        title = _("My Feedback")
        if request.user.is_authenticated():
            feedback = feedback.filter(user=request.user)
        else:
            feedback = feedback.none()
    
    if not type:
        type = "all"
    elif type != "all":
        feedback = feedback.filter(type__slug=type)
    
    if not status:
        status = "all"
    elif status != "all":
        feedback = feedback.filter(status__slug=status)
    
    if request.user.is_staff != True:
        feedback = feedback.filter(private=False)
    
    feedback_list = paginate(feedback, 10, request)
    
    return render_to_response('djangovoice/list.html', {'feedback_list': feedback_list.object_list, 'pagination': feedback_list, 'list': list, 'status': status, 'type': type, 'navigation_active': list, 'title': title,}, context_instance=RequestContext(request))


@login_required
def widget(request):
    if request.method == 'POST':
        form = WidgetForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            try:
                if form.data['anonymous'] != "on":
                    feedback.user = request.user
            except:
                    feedback.user = request.user
            feedback.save()
            data = simplejson.dumps({'url':feedback.get_absolute_url(), 'errors': False})
        else:
            data = simplejson.dumps({'errors': True})
        
        return HttpResponse(data, mimetype='application/json')
    else:
        form = WidgetForm()
    return render_to_response('djangovoice/widget.html', {'form': form}, context_instance=RequestContext(request))


@login_required
def submit(request):
    if request.method == 'POST':
        form = WidgetForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            try:
                if form.data['anonymous'] != "on":
                    feedback.user = request.user
            except:
                    feedback.user = request.user
            feedback.save()
            return HttpResponseRedirect(feedback.get_absolute_url())
    else:
        form = WidgetForm()
    
    return render_to_response('djangovoice/submit.html', {'form': form}, context_instance=RequestContext(request))

@login_required
def edit(request, object_id):
    feedback = get_object_or_404(Feedback, pk=object_id)

    if request.user.is_staff:
        form_class = EditForm
    elif request.user == feedback.user:
        form_class = WidgetForm
    else:
        return Http404

    if request.method == 'POST':
        form = form_class(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(feedback.get_absolute_url())
    else:
        form = form_class(instance=feedback)
    return render_to_response('djangovoice/edit.html', {'form': form, 'feedback':feedback}, context_instance=RequestContext(request))

@login_required
def delete(request, object_id):
    feedback = get_object_or_404(Feedback, pk=object_id)
    if request.user != feedback.user and not request.user.is_staff:
        return Http404
    if request.method == 'POST':
        feedback.delete()
        return HttpResponseRedirect(reverse('feedback_home'))
    return render_to_response('djangovoice/delete.html', {'feedback':feedback}, context_instance=RequestContext(request))



