from typing import Text
from django.shortcuts import render
import urllib.request,urllib.parse,urllib.error
from urllib.request import urlopen

# Create your views here.


def get_html_content(city):
    import requests
    #city = request.GET.get('city')
    city = city.replace(" ", "+")
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(f'https://www.google.com/search?q=weather+{city}').text
    return html_content
def index(request):
    result = None
    if 'city' in request.GET:
        city = request.GET.get('city')
        # fetch the weather from Google.
        html_content = get_html_content(city)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        result =dict()

        result['region']=soup.find("span", attrs={"class": "BNeawe tAd8D AP7Wnd"}).text
        result['temp'] =soup.find("div", attrs={"class": "BNeawe iBp4i AP7Wnd"}).text
        result['daytime'], result['weathernow'] = soup.find("div", attrs={"class": "BNeawe tAd8D AP7Wnd"}).text.split(
            '\n')
        listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
        strd = listdiv[5].text
        pos = strd.find('Wind')
        other_data = strd[pos:]
        #result['Wind']=other_data
        print(other_data)

    return render(request, 'index.html',{'result': result})