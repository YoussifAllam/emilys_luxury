from django.db.models import Func
from django.db.models import Avg  ,Q , Min ,Max
from rest_framework.pagination import PageNumberPagination
from .serializers import HomeDressesSerializer , AverageRatingSerializer
from .models import dress_reviews  ,Dresses
from collections import defaultdict
from rest_framework.response import Response

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

def filter_service(num_of_Stars , price_from, price_to, measurement, designer_name, Color, will_sort, Target_products, request  ,product_type):
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

    if product_type:
        Target_products = Target_products.filter(
            product_type__icontains=product_type
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

def get_rating_details():
    # Aggregate to compute the average rating for each product
    product_averages = dress_reviews.objects.values('dress').annotate(avg_rating=Avg('Rating_stars'))

    # Dictionary to hold the count of products for each average rating
    average_rating_count = defaultdict(int)

    # Collect data about how many products have each average rating
    for entry in product_averages:
        avg_rating_rounded = int(entry['avg_rating'])  # Round to one decimal place for grouping
        average_rating_count[avg_rating_rounded] += 1

    # Prepare the final list of average ratings and how many products have that average
    ratings_detail = []
    for avg_rating, count in sorted(average_rating_count.items()):
        ratings_detail.append({
            'stars': avg_rating,
            'product_count': count
        })

    result = {
        'ratings_detail': ratings_detail
    }

    return result

def get_unique_data():
    # Get unique colors
    unique_colors = Dresses.objects.values_list('Color', flat=True).distinct()
    # Get unique measurements
    unique_measurements = Dresses.objects.values_list('measurement', flat=True).distinct()
    # Get unique designer names
    unique_designers = Dresses.objects.values_list('designer_name', flat=True).distinct()

    return unique_colors, unique_measurements, unique_designers

def get_slide_data(request):
    # Get categories
    unique_colors, unique_measurements, unique_designers = get_unique_data()
    # Get price range
    price_data = Dresses.objects.aggregate(
        min_price=Min('price_for_3days'),
        max_price=Max('price_for_3days')
    )

    rating_details = get_rating_details()
    rating_seralizer = AverageRatingSerializer(rating_details)
    # Construct response data
    response_data = {
        'rating_details': rating_seralizer.data['ratings_detail'],
        'unique_colors': list(unique_colors),
        'unique_measurements': list(unique_measurements),
        'unique_designers': list(unique_designers),
        'price_range': {
            'min_price': price_data['min_price'],
            'max_price': price_data['max_price'] ,
        }
    }

    return Response(response_data)