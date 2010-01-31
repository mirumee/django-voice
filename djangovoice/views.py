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


def detail(request, object_id):
    u = request.user
    feedback = get_object_or_404(Feedback, pk=object_id)
    
    if feedback.private == True:
        if u.is_staff != True and u != feedback.user:
            raise Http404
    
    return render_to_response('detail.html', {'feedback': feedback}, context_instance=RequestContext(request))


def list(request, list=False, type=False, status=False):
    u = request.user
    feedback = Feedback.objects.all().order_by('-created')
    
    if not list:
        list = "open"
    
    if list == "all":
        template = 'all.html'
    elif list == "open":
        template = 'open.html'
        feedback = feedback.filter(status__status='open')
    elif list == "closed":
        template = 'closed.html'
        feedback = feedback.filter(status__status='closed')
    elif list == "mine":
        template = 'mine.html'
        feedback = feedback.filter(user=u)
    
    if not type:
        type = "all"
    elif type != "all":
        feedback = feedback.filter(type__slug=type)
    
    if not status:
        status = "all"
    elif status != "all":
        feedback = feedback.filter(status__slug=status)
    
    if u.is_staff != True:
        feedback = feedback.filter(private=False)
    
    feedback_list = paginate(feedback, 10, request)
    
    return render_to_response(template, {'feedback_list': feedback_list.object_list, 'pagination': feedback_list, 'list': list, 'status': status, 'type': type, 'navigation_active': list}, context_instance=RequestContext(request))


@login_required
def widget(request):
    if request.method == 'POST':
        form = WidgetForm(request.POST)
        u = request.user
        if form.is_valid():
            feedback = form.save(commit=False)
            try:
                if form.data['anonymous'] != "on":
                    feedback.user = u
            except:
                    feedback.user = u
            feedback.save()
            data = simplejson.dumps({'url':feedback.get_absolute_url(), 'errors': False})
        else:
            data = simplejson.dumps({'errors': True})
        
        return HttpResponse(data, mimetype='application/json')
    else:
        form = WidgetForm()
    return render_to_response('widget.html', {'form': form}, context_instance=RequestContext(request))


@login_required
def submit(request):
    if request.method == 'POST':
        form = WidgetForm(request.POST)
        u = request.user
        if form.is_valid():
            feedback = form.save(commit=False)
            try:
                if form.data['anonymous'] != "on":
                    feedback.user = u
            except:
                    feedback.user = u
            feedback.save()
            return HttpResponseRedirect(feedback.get_absolute_url())
    else:
        form = WidgetForm()
    
    return render_to_response('submit.html', {'form': form}, context_instance=RequestContext(request))

@login_required
def edit(request, object_id):
    u = request.user
    if not u.is_staff:
        raise Http404
    feedback = Feedback.objects.get(id=object_id)
    if request.method == 'POST':
        form = EditForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(feedback.get_absolute_url())
    else:
        form = EditForm(instance=feedback)
    return render_to_response('edit.html', {'form': form, 'feedback':feedback}, context_instance=RequestContext(request))



