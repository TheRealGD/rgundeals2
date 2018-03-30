from django.conf import settings
from django.core.paginator import Paginator


class EnhancedPaginator(Paginator):

    def __init__(self, queryset, per_page, **kwargs):

        # Grab the per-page count from the request parameters or use default
        try:
            per_page = int(per_page)
            if per_page < 1 or per_page > settings.MAX_PAGE_SIZE:
                per_page = settings.DEFAULT_PAGE_SIZE
        except TypeError:
            per_page = settings.DEFAULT_PAGE_SIZE

        super().__init__(queryset, per_page, **kwargs)
