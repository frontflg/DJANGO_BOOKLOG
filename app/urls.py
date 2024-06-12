from django.urls import path
from app import views
from .views import BooklogList, BooklogDetail, BooklogCreate, BooklogUpdate, BooklogDelete

urlpatterns = [
    path('',                   views.IndexView.as_view(),   name='index'),
    path('books/',             views.IndexView.as_view(),   name='index'),
    path('detail/<str:isbn>',  views.BooksDetail.as_view(), name='detail'),
    path("list/",              BooklogList.as_view(),       name="list"),
    path("logdetail/<int:pk>", BooklogDetail.as_view(),     name="booklog_detail"),
    path("create/",            BooklogCreate.as_view(),     name="booklog_create"),
    path("update/<int:pk>",    BooklogUpdate.as_view(),     name="booklog_update"),
    path("delete/<int:pk>",    BooklogDelete.as_view(),     name="booklog_delete"),
]
