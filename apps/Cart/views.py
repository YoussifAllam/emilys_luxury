from .models import *
from .serializers import CartSerializer
from apps.Dresses.models import Dresses
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK  , HTTP_404_NOT_FOUND , HTTP_400_BAD_REQUEST , HTTP_201_CREATED , HTTP_204_NO_CONTENT
from .services import Check_if_Cart_Item_Exists , calculate_total_price , calc_total_price_with_coupon
from apps.Coupons.models import Coupon
from . import tasks

@api_view(['POST'])
def create_cart(request):
    if request.method == 'POST':
        cart = Cart.objects.create()
        return Response(
            {'status': 'success', 
            'cart_id': cart.id} ,  status=HTTP_201_CREATED)
    
@api_view(['POST'])
def add_item(request):
    if request.method == 'POST':
        Dress_id = request.data.get('Dress_uuid')
        Cart_id = request.data.get('cart_id')
        booking_start_date = request.data.get('booking_start_date')
        booking_end_date = request.data.get('booking_end_date')
        booking_for_n_days = request.data.get('booking_for_n_days')

        try : dress = Dresses.objects.get(id=Dress_id)
        except Dresses.DoesNotExist: return Response({'status': 'fialed' , 'error': 'Dress not found'}, status=HTTP_404_NOT_FOUND)
        
        try : cart = Cart.objects.get(id=Cart_id)
        except Cart.DoesNotExist: return Response({'status': 'fialed' , 'error': 'Cart not found'}, status=HTTP_404_NOT_FOUND)

        is_cart_item_founded , cart_items = Check_if_Cart_Item_Exists(cart_id=Cart_id, dress_id=Dress_id)
        if is_cart_item_founded: 
            return Response ({ 'status': 'fialed' , 'error':'The item is already in the cart'}, status=HTTP_400_BAD_REQUEST)
          
        response_error , response_status = tasks.process_is_valid(dress, booking_for_n_days, booking_start_date, booking_end_date)
        if response_status != HTTP_200_OK : 
            return Response(response_error, response_status)

        cart_items = Cart_Items.objects.create(cart=cart, dress=dress,  booking_start_date=booking_start_date,
                                                    booking_end_date=booking_end_date, booking_for_n_days=booking_for_n_days, )
            
        return Response(
            {'status': 'success', 
            'cart_items': cart_items.id} ,  status=HTTP_201_CREATED)
    
@api_view(['GET'])
def get_cart_details(request):
    if request.method == 'GET':
        cart_id = request.GET.get('cart_id')
        if not cart_id:
            return Response({'status': 'fialed' , 'error': 'Cart ID is required'}, status=HTTP_400_BAD_REQUEST)
        try:
            cart = Cart.objects.get(id=cart_id)
            serializer = CartSerializer(cart)
            return Response({
                'status': 'success',
                'data': serializer.data
            })
        except Cart.DoesNotExist:
            return Response({'status': 'fialed' , 'error': 'Cart not found'}, status=HTTP_404_NOT_FOUND)

@api_view(['DELETE']) 
def remove_item_from_cart(request): 
    if request.method == 'DELETE':
        cart_item_id = request.GET.get('cart_item_id')
        if not cart_item_id:
            return Response({'status': 'fialed' , 'error': 'cart_item_id is required'}, status=HTTP_400_BAD_REQUEST)
        try:
            cart_item = Cart_Items.objects.get(id=cart_item_id)
            cart_item.delete()
            return Response({'status': 'success' , 'message' :   'cart item deleted successfully'} , status=HTTP_200_OK)
        except Cart_Items.DoesNotExist:
            return Response({'status': 'fialed' , 'error': 'Cart item not found'}, status=HTTP_404_NOT_FOUND)

@api_view(['DELETE']) 
def clear_shopping_cart(request): 
    if request.method == 'DELETE':
        cart_id = request.GET.get('cart_id')
        if not cart_id:
            return Response({'status': 'fialed' , 'error': 'cart_id is required'}, status=HTTP_400_BAD_REQUEST)
        try:
            cart = Cart.objects.get(id=cart_id)
            cart.delete()
            return Response({'status': 'success' , 'message' :  'cart  deleted successfully'}
                            , status=HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response({'status': 'fialed' , 'error': 'cart not found'}, status=HTTP_404_NOT_FOUND)

@api_view(['GET'])    
def cart_total_price(request):
    cart_id = request.GET.get('cart_id')
    coupon_code = request.GET.get('coupon_code')
    try: cart = Cart.objects.get(id=cart_id)
    except Cart.DoesNotExist:  return Response({'status': 'fialed' , 'error': 'Cart not found'}, status=HTTP_404_NOT_FOUND)
    
    cart_items = cart.items_set.all()
    Subtotal , total_price_without_coupon , Shipping_Flat_rate , INSURANCE_rate = calculate_total_price(cart_items )
    # Subtotal is the total price for all items in the cart
    # total_price_without_coupon = Subtotal + Shipping_Flat_rate 
    
    if coupon_code:
        try: coupon = Coupon.objects.get(code=coupon_code)
        except Coupon.DoesNotExist: return Response({'status': 'fialed' , 'error': 'Coupon not found'}, status=HTTP_404_NOT_FOUND)
        
        sale_price , total_price ,  is_coupon_valid = calc_total_price_with_coupon(Subtotal , coupon)
        if not is_coupon_valid : return Response({ 'status': 'field', 'coupon' : 'the_coupon_is_expired' , }, status=HTTP_400_BAD_REQUEST)
        else : return Response({ 'status': 'success',
                                'subtotal': Subtotal ,
                                'total_price_after_coupon' : sale_price ,
                                'DELIVERY' : Shipping_Flat_rate ,
                                'total_price': total_price},
                                 status=HTTP_200_OK)

    return Response({ 'status': 'success', 
                     'subtotal' : Subtotal  ,
                     'DELIVERY' : Shipping_Flat_rate,
                     'total_price': total_price_without_coupon}, status=HTTP_200_OK)


