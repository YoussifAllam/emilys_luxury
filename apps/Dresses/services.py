from django.db.models import Func
from django.db.models import Avg  ,Q
from rest_framework.pagination import PageNumberPagination
from .serializers import HomeDressesSerializer


def sort_products(Target_products, request):
    sort_by = request.GET.get('sort_by')
    if sort_by == 'low_to_high':
        Target_products = Target_products.order_by('price_for_3days')
    elif sort_by == 'high_to_low':
        Target_products = Target_products.order_by('-price_for_3days')
    elif sort_by == 'latest':
        Target_products = Target_products.order_by('uploaded_at')
    elif sort_by == 'popularity':
        Target_products = Target_products.order_by('-id')
    elif sort_by == 'average_rating':
        Target_products = Target_products.annotate(
            average_rating=Avg('review_set__Rating_stars')
        ).order_by('-average_rating')
    return Target_products

def filter_service(num_of_Stars , price_from, price_to, measurement, designer_name, Color, will_sort, Target_products, request):
    if num_of_Stars:
        num_of_Stars = [float(star) for star in num_of_Stars.split(',')]
        star_conditions = Q()
        for star in num_of_Stars:
            star_conditions |= Q(rounded_average__gte=star, rounded_average__lt=star + 1)

        Target_products = Target_products.annotate(
            average_rating=Avg('review_set__Rating_stars')  # Corrected from dress_reviews to review_set
        ).annotate(
            rounded_average=Round('average_rating')
        ).filter(star_conditions)

    if price_from and price_to:
        # Filter products where either the regular price or the sale price is within the specified range
        Target_products = Target_products.filter(
            Q(price_for_3days__gte=price_from, price_for_3days__lte=price_to) 
        ).distinct()

    elif price_from :
        Target_products = Target_products.filter(
            Q(price_for_3days__gte=price_from) 
        ).distinct()
        
    elif price_to and not price_from:
        Target_products = Target_products.filter(
            Q(price_for_3days__lte=price_to ) 
        ).distinct()

    if measurement:
        Target_products = Target_products.filter(
            measurement__icontains=measurement
        ).distinct()

    if designer_name:
        Target_products = Target_products.filter(
            designer_name__icontains=designer_name
        ).distinct()

    if Color:
        Target_products = Target_products.filter(
            Color__icontains=Color
        ).distinct()

    if will_sort == 'True':
        Target_products = sort_products(Target_products , request  )

    return Target_products

def increment_dress_number_of_visitors(dress_target_dress_n_vistors_instance):
   dress_target_dress_n_vistors_instance.number_of_visitors += 1
   dress_target_dress_n_vistors_instance.save()

class Round(Func):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 1)'  # rounding to 1 decimal place

def pagenator(Target_products , request , serializer):
    paginator = PageNumberPagination()
    paginator.page_size = 12  # or use CustomPagination class
    paginated_products = paginator.paginate_queryset(Target_products, request)

    if serializer == 'HomeDressesSerializer':
        serializer = HomeDressesSerializer(paginated_products, many=True, context={'request': request})
   #  elif serializer == 'Products_search_Serializer':
   #      serializer = Products_search_Serializer(paginated_products, many=True, context={'request': request})

    paginated_response = paginator.get_paginated_response(serializer.data)
    
    # Add custom status field to the response data
    paginated_response.data['status'] = 'success'

    # return paginated_response
    response_data = {
        'status': 'success',
        'Products': {
        'count': paginated_response.data['count'],
        'next': paginated_response.data['next'],
        'previous': paginated_response.data['previous'],
        'results': paginated_response.data['results']
        }

    }
    return response_data

