from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
#from django.template.defaultfilters import slugify

STATUS_CHOICES = (
    ('open', 'Open'),
    ('closed', 'Closed'),
)

class Status(models.Model):
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500)
    default = models.BooleanField(blank=True, help_text='New feedback will have this status')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="open")
    
    def save(self):
        #self.slug = slugify(self.title)
        
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
    
    def save(self):
        self.slug = slugify(self.title)
        super(Type, self).save()
    
    def __unicode__(self):
        return self.title


class Feedback(models.Model):
    type = models.ForeignKey(Type)
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    anonymous = models.BooleanField(blank=True, help_text='Do not show who sent this')
    private = models.BooleanField(blank=True, help_text='Hide from public pages. Only site administrators will be able to view and respond to this.')
    user = models.ForeignKey(User, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    status = models.ForeignKey(Status)
    duplicate = models.ForeignKey('self', null=True, blank=True)
    
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
        return "/feedback/%s/" % (self.id)
    
    def __unicode__(self):
        return self.title

