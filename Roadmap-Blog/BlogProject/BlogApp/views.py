from .models import Article
from .forms import ArticleForm
from django.shortcuts import render, redirect

# Create your views here.
def createArticleView(request):
    form = ArticleForm
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("show_url")

    template_name = "BlogApp/Article_form.html"
    context = {"form": form}
    return render(request, template_name, context)

def showArticleView(request):
    obj = Article.objects.all()
    template_name = "BlogApp/show.html"
    context = {"obj": obj}
    return render(request, template_name, context)
