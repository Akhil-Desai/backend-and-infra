from .models import Article
from django import forms


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'

class SearchForm(forms.Form):
    query = forms.CharField(label="Search", max_length=100)
