"""
    Core application filters utility
    core/util/filters.py
"""


from django.core.exceptions import ValidationError


def filter_queryset(queryset, request, target_param=None, is_foreign_key=False):
    """ Filters queryset by target parameter """
    try:
        query = request.query_params.get(target_param)
        if query is not None:
            queryset = eval('queryset.filter({}{}=query)'.format(target_param, '_id' * is_foreign_key))
    except (ValueError, ValidationError):
        queryset = None

    return queryset


def filter_queryset_permission(queryset, request, permissions):
    """ Filters queryset with permissions """
    for i in permissions:
        visible_ids = [
            j.id for j in queryset if i.has_permission(request, None) and i.has_object_permission(request, None, j)
        ]
        queryset = queryset.filter(pk__in=visible_ids)

    return queryset
