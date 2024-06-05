from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Booklog
from .forms import BooklogForm

# Create your views here.
class BooklogList(ListView):
    model = Booklog
    context_object_name = "booklogs"
    paginate_by = 8

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
