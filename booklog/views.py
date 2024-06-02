from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy

from .models import Booklog

# Create your views here.
class BooklogList(ListView):
    model = Booklog
    context_object_name = "booklogs"

class BooklogDetail(DetailView):
    model = Booklog
    context_object_name = "booklog"

class BooklogCreate(CreateView):
    model = Booklog
    fields = "__all__"
    success_url = reverse_lazy("list")

class BooklogUpdate(UpdateView):
    model = Booklog
    fields = "__all__"
    success_url = reverse_lazy("list")

class BooklogDelete(DeleteView):
    model = Booklog
    context_object_name = "booklog"
    success_url = reverse_lazy("list")
