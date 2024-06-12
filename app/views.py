from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.shortcuts import render
import json
import requests
from .forms import SearchForm, BooklogForm
from django.urls import reverse_lazy
from .models import Booklog

SEARCH_URL = 'https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404?format=json&applicationId=1002196771843734307'

def get_api_data(params):
    api = requests.get(SEARCH_URL, params=params).text
    result = json.loads(api)
    items = result['Items']
    return items

class IndexView(View):
    def get(self, request, *args, **kwargs):
        form = SearchForm(request.POST or None)
        return render(request, 'app/index.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = SearchForm(request.POST or None)
        if form.is_valid():
            keyword = form.cleaned_data['title']
            params = {
                'title': keyword,
                'hits': 28,
            }
            items = get_api_data(params)
            book_data = []
            for i in items:
                item = i['Item']
                title = item['title']
                image = item['largeImageUrl']
                isbn = item['isbn']
                query = {
                    'title': title,
                    'image': image,
                    'isbn': isbn
                }
                book_data.append(query)
            return render(request, 'app/book.html', {
                'book_data': book_data,
                'keyword': keyword
            })
        return render(request, 'app/index.html', {
            'form': 'form'
        })

class BooksDetail(View):
    def get(self, request, *args, **kwargs):
        isbn = self.kwargs['isbn']
        params = {
            'isbn': isbn
        }
        items = get_api_data(params)
        items = items[0]
        item = items['Item']
        title = item['title']
        image = item['largeImageUrl']
        author = item['author']
        itemPrice = item['itemPrice']
        salesDate = item['salesDate']
        publisherName = item['publisherName']
        size = item['size']
        isbn = item['isbn']
        itemCaption = item['itemCaption']
        itemUrl = item['itemUrl']
        reviewAverage = item['reviewAverage']
        reviewCount = item['reviewCount']
        book_data = {
            'title': title,
            'image': image,
            'author': author,
            'itemPrice': itemPrice,
            'salesDate': salesDate,
            'publisherName': publisherName,
            'size': size,
            'isbn': isbn,
            'itemCaption': itemCaption,
            'itemUrl': itemUrl,
            'reviewAverage': reviewAverage,
            'reviewCount': reviewCount,
            'average': float(reviewAverage) * 20,
        }
        return render(request, 'app/detail.html', {
            'book_data': book_data
        })

class BooklogList(ListView):
    model = Booklog
    context_object_name = "booklogs"
    ordering = '-getdate'
    paginate_by = 7

    # 書名絞り込み
    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        query = self.request.GET
        if q := query.get('q'):
            queryset = queryset.filter(bookname__icontains=q)
        return queryset.order_by('-bookname')

class BooklogDetail(DetailView):
    model = Booklog
    context_object_name = "booklog"

class BooklogCreate(CreateView):
    model = Booklog
  # fields = "__all__"
    form_class = BooklogForm
    success_url = reverse_lazy("list")

class BooklogUpdate(UpdateView):
    model = Booklog
  # fields = "__all__"
    form_class = BooklogForm
    success_url = reverse_lazy("list")

class BooklogDelete(DeleteView):
    model = Booklog
    context_object_name = "booklog"
    success_url = reverse_lazy("list")
