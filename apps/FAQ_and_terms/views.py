from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .serializers import *
from .models import *


@api_view(["GET"])
def Get_FAQ(request):
    Which_Page = request.GET.get("Which_Page")

    if not Which_Page:
        return Response(
            {"status": "error", "message": "Which_Page is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if Which_Page != "Investor" and Which_Page != "user":
        return Response(
            {
                "status": "error",
                "message": "Which_Page is invalid you can enter Investor or user",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    FAQ_data = FAQ.objects.filter(Which_Page=Which_Page)
    serializers = FAQSerializer(FAQ_data, many=True)
    return Response(
        {"status": "success", "data": serializers.data}, status=status.HTTP_200_OK
    )


@api_view(["GET"])
def Get_terms_and_condations(request):
    Which_Page = request.GET.get("Which_Page")

    if not Which_Page:
        return Response(
            {"status": "error", "message": "Which_Page is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if Which_Page != "Investor" and Which_Page != "user":
        return Response(
            {
                "status": "error",
                "message": "Which_Page is invalid you can enter Investor or user",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    AboutUs_data = terms_and_condations.objects.filter(Which_Page=Which_Page)
    serializers = terms_and_condationsSerializer(AboutUs_data, many=True)
    return Response(
        {"status": "success", "data": serializers.data}, status=status.HTTP_200_OK
    )
