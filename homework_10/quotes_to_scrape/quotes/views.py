from django.shortcuts import render
from .utils import get_mongo
from django.core.paginator import Paginator

# Create your views here.

def main(request, page=1):
    db = get_mongo()
    quotes = db.quotes.find()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quote_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes':quote_on_page })