from django.core.paginator import Paginator

def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return page_obj

