from django.core.paginator import Paginator, InvalidPage, EmptyPage

def paginate(queryset, items, request):
    paginator = Paginator(queryset, items)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        queryset_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        queryset_list = paginator.page(paginator.num_pages)
    
    return queryset_list
