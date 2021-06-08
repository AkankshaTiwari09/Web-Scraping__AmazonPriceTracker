from django.shortcuts import render,redirect
from bs4 import BeautifulSoup
from .models import *

# Create your views here.

def home(request):
    if request.method=='POST':
        url=request.POST.get('url')
        html_content=get_html_content(url)
        soup= BeautifulSoup(html_content, 'html.parser')
        try:
            name=soup.find('span',attrs={"class":"a-size-large product-title-word-break"}).text.strip()
            old_price=soup.find('span',attrs={"class":"priceBlockStrikePriceString a-text-strike"}).text.strip()
            #discounted_price=soup.find('span',attrs={"class":"a-size-medium a-color-price priceBlockBuyingPriceString"}).text.strip()
            discounted_price=soup.find('span',attrs={"class":"a-size-medium a-color-price priceBlockBuyingPriceString"})
            if discounted_price == None:
                discounted_price=soup.find('span',attrs={"class":"a-size-medium a-color-price priceBlockSalePriceString"})
            if discounted_price== None:
                discounted_price=soup.find('span',attrs={"class":"a-size-medium a-color-price priceBlockDealPriceString"})
            discounted_price=discounted_price.text.strip()
            #print(discounted_price)

            discount=soup.find('td',attrs={"class":"a-span12 a-color-price a-size-base priceBlockSavingsString"}).text.strip()
            #print(discount)
            prod_obj=Product.objects.create(name=name, old_price=old_price, new_price=discounted_price, discount=discount,url=url)
            prod_obj.save()
            products=Product.objects.all()
            return render(request, 'products.html', {'products':products})  
        except Exception as e:
            err="Error capturing product details..."
            print(err)
            return render(request,'home.html', {'err':err})

        
    return render(request,'home.html')



def get_html_content(url):
    import requests
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content=session.get(url).text
    return html_content

def products(request):
    products=Product.objects.all()
    return render(request, 'products.html', {'products':products})  

def confirm_delete(request,prod_id):
    prod=Product.objects.get(pk=prod_id)
    prod.delete()
    return redirect('products')


