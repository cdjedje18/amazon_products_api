from django.http import JsonResponse
from rest_framework.decorators import api_view
import requests
from bs4 import BeautifulSoup



@api_view(['GET'])
def get_products(request):

    return JsonResponse(data={"message": "Hello world"}, safe=False)


