from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.shortcuts import render
import json
import requests
from .forms import SearchForm, BooklogForm
from django.urls import reverse_lazy
from .models import Booklog

SEARCH_URL = 'https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404?format=json&applicationId=1002196771843734307'

GOOGLE_URL = 'https://www.googleapis.com/books/v1/volumes?q='

def get_api_data(params):
  # print(params)
    api = requests.get(SEARCH_URL, params=params).text
    result = json.loads(api)
    items = result['Items']
    return items

def get_gglls_data(params):
    print(params)
  # url = GOOGLE_URL + params['title'] + '&imaxResults=' + str(params['hits'])
    url = GOOGLE_URL + params['title'] + '&imaxResults=28'
    print(url)
    api = requests.get(url).text
    result = json.loads(api)
    items = result['items']
    return items

def get_ggl_data(params):
    print(params['isbn'])
    url = GOOGLE_URL + 'isbn:' + params['isbn']
    api = requests.get(url).text
    result = json.loads(api)
    try:
        items = result['items']
    except KeyError:
        items = []
    return items

class IndexView(View):
    def get(self, request, *args, **kwargs):
        form = SearchForm(request.POST or None)

        return render(request, 'app/index.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = SearchForm(request.POST or None)

        if "rakuten" in request.POST:
            print('Rukuten検索時の処理')
        elif "google" in request.POST:
            print('Google検索の処理')

        if form.is_valid():
            keyword = form.cleaned_data['title']
            params = {
                'title': keyword,
                'hits': 28,
            }
            if "rakuten" in request.POST:
                items = get_api_data(params)
            elif "google" in request.POST:
                items = get_gglls_data(params)

            book_data = []
            for i in items:
                if "rakuten" in request.POST:
                    item = i['Item']
                    title = item['title']
                    image = item['largeImageUrl']
                    isbn = item['isbn']
                elif "google" in request.POST:
                    item = i['volumeInfo']
                    title = item['title']
                    imageLNK = item.get('imageLinks',{'thumbnail':''})
                    image = imageLNK['thumbnail']
                    try:
                        isbns = item['industryIdentifiers']
                        isbn = isbns[0]['identifier']
                    except KeyError:
                        isbn = 'notFoundIsbnForGoogle'

                if len(isbn) > 13:
                    print(isbn + ' LEN=' + str(len(isbn)))
                query = {
                    'title': title,
                    'image': image,
                    'isbn': isbn
                }
                if len(isbn) < 14:
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

        items = get_ggl_data(params)
        if items==[]:
            print('GoogleBooksApi 対象なし')
            items = get_api_data(params)
            items = items[0]
            item  = items['Item']
            title = item['title']
            image = item['largeImageUrl']
            author = item['author']
            itemPrice = item['itemPrice']
            salesDate = item['salesDate']
            publisherName = item['publisherName']
            isbn = item['isbn']
            itemCaption = item['itemCaption']
            itemUrl = item['itemUrl']
        else:
            items = items[0]
            item  = items['volumeInfo']
            title = item['title']
            imageLNK = item.get('imageLinks',{'thumbnail':'NO IMAGE'})
            image = imageLNK['thumbnail']
            try:
                author = item['authors'][0]
            except KeyError:
                author = ''
            sale = items['saleInfo']
            try:
                price = sale['listPrice']
                itemPrice = price['amount']
            except KeyError:
                itemPrice = 'NOT_FOR_SALE　'
            try:
                salesDate = item['publishedDate']
            except KeyError:
                salesDate = ''
            try:
                publisherName = item['publisher']
            except KeyError:
                publisherName = ''
            try:
                itemCaption = item['description']
            except KeyError:
                itemCaption = ''
            itemUrl = item['infoLink']

        book_data = {
            'title': title,
            'image': image,
            'author': author,
            'itemPrice': itemPrice,
            'salesDate': salesDate,
            'publisherName': publisherName,
            'isbn': isbn,
            'itemCaption': itemCaption,
            'itemUrl': itemUrl,
        }

        return render(request, 'app/detail.html', {
            'book_data': book_data
        })

class BooklogList(ListView):
    model = Booklog
    context_object_name = 'booklogs'
    ordering = ['-getdate']
    paginate_by = 8

    # 書名絞り込み
    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        query = self.request.GET

        if q := query.get('q'):
            queryset = queryset.filter(bookname__icontains=q)

        return queryset.order_by('-getdate')

class BooklogDetail(DetailView):
    model = Booklog
    context_object_name = "booklog"

class BooklogCreate(CreateView):
    model = Booklog
  # fields = "__all__"
    form_class = BooklogForm
    success_url = reverse_lazy("list")

    def get_initial(self, **kwargs):
        initial = super().get_initial()
        try:
            isbn = self.kwargs['isbn']
        except:
            isbn = ''

        params = {
            'isbn': isbn
        }
        if isbn:
            items = get_ggl_data(params)
            try:
                items = items[0]
                item  = items['volumeInfo']
                tmp = item["industryIdentifiers"]
                if len(isbn) == 10:
                    initial["isbn10"]    = isbn
                    if tmp[0]["type"] == "ISBN_13":
                        initial["isbn13"] = tmp[0]["identifier"]
                    if tmp[1]["type"] == "ISBN_13":
                        initial["isbn13"] = tmp[1]["identifier"]
                else:
                    initial["isbn13"]    = isbn
                    if tmp[0]["type"] == "ISBN_10":
                        initial["isbn10"] = tmp[0]["identifier"]
                    if tmp[1]["type"] == "ISBN_10":
                        initial["isbn10"] = tmp[1]["identifier"]
                try:
                    initial["bookname"]  = item['title']
                except:
                    initial["bookname"]  = ""
                try:
                    initial["author"]    = item['authors'][0] + "／" + item['authors'][1]
                except:
                    initial["author"]    = item['authors'][0]
                try:
                    initial["issuedate"] = item['publishedDate']
                except:
                    initial["issuedate"] = ""
                try:
                    initial["publisher"] = item['publisher']
                except:
                    initial["publisher"] = ""
                try:
                    initial["overview"]  = item['description']
                except:
                    initial["overview"]  = ""
                try:
                    sale = items['saleInfo']
                    price = sale['listPrice']
                    initial["purchase"]  = price['amount']
                    print(price)
                except:
                    initial["purchase"]  = ''
            except:
                print('例外発生 ' + isbn)

        return initial

class BooklogUpdate(UpdateView):
    model = Booklog
  # fields = "__all__"
    form_class = BooklogForm
    success_url = reverse_lazy("list")

class BooklogDelete(DeleteView):
    model = Booklog
    context_object_name = "booklog"
    success_url = reverse_lazy("list")
