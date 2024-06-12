from django import forms
from django.forms import ModelForm
from .models import Booklog

class DateInput(forms.DateInput):
    input_type = 'date'

class SearchForm(forms.Form):
    title = forms.CharField(label='タイトル', max_length=200, required=True)

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

    def clean_isbn13(self):
        value = self.cleaned_data['isbn13']
        if len(value) < 13:
            raise forms.ValidationError("13桁入力してください!")
        return value
