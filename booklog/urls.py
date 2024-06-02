from django.urls import path
from .views import BooklogList, BooklogDetail, BooklogCreate, BooklogUpdate, BooklogDelete

urlpatterns = [
    path("", BooklogList.as_view(), name="list"),
    path("detail/<int:pk>", BooklogDetail.as_view(), name="detail"),
    path("create/", BooklogCreate.as_view(), name="create"),
    path("update/<int:pk>", BooklogUpdate.as_view(), name="update"),
    path("delete/<int:pk>", BooklogDelete.as_view(), name="delete"),
]
