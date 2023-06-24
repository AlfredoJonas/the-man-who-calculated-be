
def apply_filter_to_paginated_api_view(allowed_filters, filter_conditions, queryset):
        # Apply filter conditions one by one
    for condition in filter_conditions:
        key, value = condition.split(':')

        # Handle different filter conditions based on the key
        if key in allowed_filters:
            queryset = queryset.filter(**{key: value})

def apply_order_to_paginated_api_view(ordering_conditions, queryset):
        # Apply ordering conditions one by one
        for condition in ordering_conditions:
            if condition.startswith('-'):
                field = condition[1:]  # Remove the leading '-' for descending order
                queryset = queryset.order_by('-' + field)
            else:
                queryset = queryset.order_by(condition)
        return queryset
