from djangovoice.models import Status
from django.template import Library,Node

register = Library()

def build_status_list(parser, token):
    """
    {% get_status_list %}
    """
    return StatusObject()

class StatusObject(Node):
    def render(self, context):
        context['status_list'] = Status.objects.all()
        return ''

register.tag('get_status_list', build_status_list)
