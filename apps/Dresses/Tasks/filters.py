# from abc import ABC, abstractmethod

# class ProductFilter(ABC):
#     @abstractmethod
#     def apply(self, queryset, request):
#         pass


# class StarsFilter(ProductFilter):
#     def apply(self, queryset, request):
#         num_of_Stars = request.GET.get('num_of_Stars')
#         if num_of_Stars:
#             num_of_Stars = [float(star) for star in num_of_Stars.split(',')]
#             star_conditions = Q()
#             for star in num_of_Stars:
#                 star_conditions |= Q(rounded_average__gte=star, rounded_average__lt=star + 1)

#             queryset = queryset.annotate(
#                 average_rating=Avg('review_set__Rating_stars')
#             ).annotate(
#                 rounded_average=Round('average_rating')
#             ).filter(star_conditions)
#         return queryset

# class PriceFilter(ProductFilter):
#     def apply(self, queryset, request):
#         price_from = request.GET.get('price_from')
#         price_to = request.GET.get('price_to')
#         if price_from and price_to:
#             queryset = queryset.filter(
#                 Q(price_for_3days__gte=price_from, price_for_3days__lte=price_to)
#             ).distinct()
#         elif price_from:
#             queryset = queryset.filter(Q(price_for_3days__gte=price_from)).distinct()
#         elif price_to:
#             queryset = queryset.filter(Q(price_for_3days__lte=price_to)).distinct()
#         return queryset

# # Similarly, create other filter classes for measurement, designer_name, color, product_type, etc.

# def filter_service(request, queryset):
#     filters = [
#         StarsFilter(),
#         PriceFilter(),
#         # Add other filters here...
#     ]

#     for product_filter in filters:
#         queryset = product_filter.apply(queryset, request)

#     will_sort = request.GET.get('sort?')
#     if will_sort == 'True':
#         queryset = sort_products(queryset, request)

#     return queryset

# @api_view(['GET'])
# def Filter_Products(request):
#     Target_products = Dresses.objects.all()

#     if not any(request.GET.get(param) for param in ['num_of_Stars', 'price_from', 'price_to', 'measurement', 'designer_name', 'color', 'product_type', 'sort?']):
#         return Response({"detail": "No filter applied."}, status=HTTP_400_BAD_REQUEST)

#     Target_products = filter_service(request, Target_products)

#     response_data = pagenator(Target_products, request, 'HomeDressesSerializer')
#     return Response(response_data, status=HTTP_200_OK)
