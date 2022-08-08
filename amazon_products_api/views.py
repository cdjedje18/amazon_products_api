from django.http import JsonResponse
from rest_framework.decorators import api_view
import requests
from bs4 import BeautifulSoup



def extract_data_from_page(search_params):
    baseUrl = "https://www.amazon.com"

    url = baseUrl+"/s?k=joker+t+shirts+for+men&sprefix=joker+t+s%2Caps%2C503&ref=nb_sb_ss_mission-aware-v1_1_9"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
        'Accept-Language': 'en-US, en;q=0.5'
    }

    html_page_Container = requests.get(url, headers=headers)
    html_page = html_page_Container.text

    page = BeautifulSoup(html_page, 'lxml')

    products_wrapper = page.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})
    # pagination_wrapper = page.find_all(class_="s-pagination-item")
    # print(pagination_wrapper[-2].text)

    new_products = []
    for product in products_wrapper:
        new_product = {}

        name = product.h2.text
        img_wrapper = product.find('img', class_="s-image")
        price_int = product.find('span', {'class': 'a-price-whole'}) 
        price_decimal = product.find('span', {'class': 'a-price-fraction'})
        rating = product.find('i', {'class': 'a-icon'})

        # print(img_wrapper['src'])

        new_product['name'] = name
        new_product['img'] = img_wrapper['src']
        new_product['price'] = float(price_int.text +price_decimal.text) if price_int is not None and price_decimal is not None else None
        new_product['rating'] = rating.text if rating is not None else None

        new_products.append(new_product)
    
    return new_products



@api_view(['GET'])
def get_products(request):
    # search_params = request.GET['search']
    data = extract_data_from_page(None)
    # print(data)
    return JsonResponse(data=data, safe=False)


