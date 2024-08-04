from rest_framework.serializers import ModelSerializer ,SerializerMethodField
# from apps.orders.models import Order , OrderItem , OrderDetails
from apps.Dresses.models import Dresses as Dresses_model
# from apps.Dresses.models import favorite_dresses
# from apps.invitation.models import user_invitation_points 
from apps.investment.models import  investmenter_balance , investmenter_dresses

class GETDressesSerializer(ModelSerializer):
    main_image = SerializerMethodField()

    class Meta:
        model = Dresses_model
        fields = ['id', 'designer_name','main_image','is_approved','Num_of_rentals']

    def get_main_image(self, obj):
        # Assuming the related name for the image set is 'image_set'
        images = obj.image_set.all()
        if images.exists():
            # Return the URL of the first image. Adjust the logic here if you have specific criteria for selecting the image.
            return images.first().image.url
        return None

class InvestorDressesSerializer(ModelSerializer):
    investor_dress = GETDressesSerializer(read_only=True , source = 'dress')
    class Meta:
        model = investmenter_dresses
        fields = ['uuid', 'user', 'investor_dress']

class InvestorBalanceSerializer(ModelSerializer):
    class Meta:
        model = investmenter_balance
        fields = [ 'total_balance', 'curr_balance']
