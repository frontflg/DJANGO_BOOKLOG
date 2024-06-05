from django import forms
from django.forms import ModelForm
from .models import Booklog

class DateInput(forms.DateInput):
    input_type = 'date'

class BooklogForm(ModelForm):
    class Meta:
        model = Booklog
        fields = ['bookname', 'isbn13', 'isbn10', 'author', 'publisher', 'genre', 
                  'issuedate', 'getdate', 'readdate', 'purchase', 'ownership',
                  'library', 'state', 'overview', 'impressions', 'coverimg',
                 ]
        widgets = {
            'issuedate': DateInput(),
            'getdate':   DateInput(),
            'readdate':  DateInput(),
        }
