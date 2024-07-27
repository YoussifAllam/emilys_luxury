from rest_framework.status import HTTP_200_OK , HTTP_201_CREATED ,HTTP_400_BAD_REQUEST 
from ..serializers.InputSerializers import AddOrderSerializer , AddOrderItemSerializer
from . import selectors

def Calculate_total_price(data  ):
    Target_cart = data['Target_cart']
    cart_items = Target_cart.items.all()
    if not cart_items :
        return ( 0, 0,  {'status': 'failed', 'error': 'Cart is empty'} , HTTP_400_BAD_REQUEST)
    
    total_price = 0
    for item in cart_items:
        if not item.product_size.is_available: 
            product_name = item.product_size.product.Product_name
            item.delete()
            return ( 0, 0,  {'status': 'failed', 'error': f'There is item in cart not available which is : {product_name}'} , HTTP_400_BAD_REQUEST)
        
        sale_price = item.product_size.Product_sale_price
        price  = sale_price if sale_price != 0 else item.product_size.Product_regular_price

        total_price += price * item.quantity
        
    return ( total_price , Target_cart , {'status': 'success', 'total_price': total_price } , HTTP_200_OK)

def create_order(request  ,total_price ):
    Target_data = request.data.copy()
    Target_data['user'] = request.user.id
    Target_data['total_price'] = total_price
    serializer = AddOrderSerializer(data=Target_data)
    if serializer.is_valid():
        serializer.save()
        return (serializer.data, HTTP_201_CREATED)
    else: 
        return (serializer.errors, HTTP_400_BAD_REQUEST)
    
def create_order_items(data , Target_cart):
    target_order = selectors.get_order(data)
    target_cart_items = Target_cart.items.all()
    for item in target_cart_items:
        item_data = {
            'order': target_order.uuid,
            'product_size' : item.product_size.id,
            'quantity': item.quantity,
            'price': item.product_size.Product_sale_price if item.product_size.Product_sale_price != 0 else item.product_size.Product_regular_price
        }
        serializer = AddOrderItemSerializer(data=item_data )
        if serializer.is_valid():
            serializer.save(order=target_order)
        else: 
            return ({ 'status': 'failed', 'error':serializer.errors} , HTTP_400_BAD_REQUEST)
    Target_cart.delete()
    return ({'status': 'success' , 'message': f'order created successfully with uuid : {target_order.uuid}'}, HTTP_201_CREATED)
    
def update_order_status(request ):
    new_status = request.data.get('status')
    if not new_status:
        return ({ 'status': 'failed', 'error':'status is required'} , HTTP_400_BAD_REQUEST)

    if new_status not in ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled']:
        return ({ 'status': 'failed', 'error':'status is invalid and should be one of these : Pending, Processing, Shipped, Delivered, Cancelled'} , HTTP_400_BAD_REQUEST)
    
    data , status =  selectors.get_order_using_request(request)
    if status != HTTP_200_OK:
        return (data , status)
    
    target_order = data['Target_order']
    target_order.status = new_status
    target_order.save()
    return ({'status': 'success' , 'message': f'order status updated successfully with uuid : {target_order.uuid}'}, HTTP_200_OK)
