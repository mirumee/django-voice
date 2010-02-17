from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

STATUS_CHOICES = (
    ('open', 'Open'),
    ('closed', 'Closed'),
)

class Status(models.Model):
    title = models.CharField(_('title'), max_length=500)
    slug = models.SlugField(_('slug'), max_length=500)
    default = models.BooleanField(_('default'), blank=True, help_text=_('New feedback will have this status'))
    status = models.CharField(_('status'), max_length=10, choices=STATUS_CHOICES, default="open")

    class Meta:
        verbose_name = _('status')
        verbose_name_plural = _('statuses')

    def save(self):
        if self.default == True:
            try:
                default_project = Status.objects.get(default=True)
                default_project.default = False
                default_project.save()
            except:
                pass
        super(Status, self).save()

    def __unicode__(self):
        return self.title

class Type(models.Model):
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500)

    class Meta:
        verbose_name = _('type')
        verbose_name_plural = _('types')

    def __unicode__(self):
        return self.title


class Feedback(models.Model):
    type = models.ForeignKey(Type, verbose_name=_('type'))
    title = models.CharField(_('title'), max_length=500)
    description = models.TextField(_('description'), blank=True, help_text=_('This will be viewable by other people - do not include any private details such as passwords or phone numbers here.'))
    anonymous = models.BooleanField(_('anonymous'), blank=True, help_text=_('Do not show who sent this'))
    private = models.BooleanField(_('private'), blank=True, help_text=_('Hide from public pages. Only site administrators will be able to view and respond to this.'))
    user = models.ForeignKey(User, blank=True, null=True)
    created = models.DateTimeField(_('created'), auto_now_add=True, blank=True, null=True)
    status = models.ForeignKey(Status, verbose_name=_('status'))
    duplicate = models.ForeignKey('self', null=True, blank=True)

    class Meta:
        verbose_name = _('feedback')
        verbose_name_plural = _('feedbacks')

    def save(self):
        try:
            self.status
        except:
            try:
                default = Status.objects.get(default=True)
            except:
                default = Status.objects.filter()[0]
            self.status = default
        super(Feedback, self).save()
    
    def get_absolute_url(self):
        return ('djangovoice_item', (self.id,))
    get_absolute_url = models.permalink(get_absolute_url)
    
    def __unicode__(self):
        return self.title

