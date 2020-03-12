from django.shortcuts import render
from . import models
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from PIL import Image

BASE_URL = 'https://sfbay.craigslist.org/search/bbb?query={}'
IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

def home(request):
    return render(request,'home.html')

def search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data , features='html.parser')
    post_listings = soup.find_all('li', class_='result-row')

    final_postings = []

    for post in post_listings:
        final_content = post.find(class_='result-title').text
        final_url = post.find('a').get('href')

        if(post.find(class_='result-image').get('data-ids')):

            final_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            final_image = IMAGE_URL.format(final_image_id)

        else:
            final_image = ('https://journocode.com/wp-content/uploads/2018/01/scraping.jpg')


        final_postings.append((final_content,final_url, final_image))


    stuff_to_render = {

        'search' : search,
        'final_postings' : final_postings,
    }

    return render(request,'my_app/search.html' , stuff_to_render)

