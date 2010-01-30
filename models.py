from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

TYPE_CHOICES = (
    ('idea', 'Idea'),
    ('problem', 'Problem'),
    ('general', 'General'),
)
STATUS_CHOICES = (
    ('new', 'New'),
    ('accepted', 'Accepted'),
    ('done', 'Done'),
    ('wontdo', "Won't Do"),
    ('duplicate', 'Duplicate'),
)

class Feedback(models.Model):
    feedback_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    anonymous = models.BooleanField(blank=True, help_text='Do not show who sent this')
    private = models.BooleanField(blank=True, help_text='Hide from public pages. Only site administrators will be able to view and respond to this.')
    user = models.ForeignKey(User, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="new")
    duplicate = models.ForeignKey('self', null=True, blank=True)
    
    def get_absolute_url(self):
        return "/feedback/%s/" % (self.id)
    
    def __unicode__(self):
        return self.title
