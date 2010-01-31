from djangovoice.models import Status
from django.template import Library, Variable, TemplateSyntaxError, Node

register = Library()

class StatusObject(Node):
    def __init__(self, list):
        self.list = Variable(list)
    
    def render(self, context):
        list = self.list.resolve(context)
        status_list = Status.objects.all()
        
        if list == "open":
            status_list = status_list.filter(status="open")
        elif list == "closed":
            status_list = status_list.filter(status="closed")
        
        context['status_list'] = status_list
        return ''

def build_status_list(parser, token):
    """
    {% get_status_list %}
    """
    bits = token.contents.split()
    if len(bits) != 2:
        raise TemplateSyntaxError, "'%s' tag takes exactly 1 arguments" % bits[0]
    return StatusObject(bits[1])

register.tag('get_status_list', build_status_list)
