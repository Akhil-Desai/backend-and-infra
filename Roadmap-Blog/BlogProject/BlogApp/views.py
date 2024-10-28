from .models import Article
from .forms import ArticleForm
from django.shortcuts import render, redirect

# Create your views here.

#C
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

#R

#Update
def updateArticleView(request, f_uid):
    obj = Article.objects.get(id = f_uid)
    form = ArticleForm(instance=obj)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("show_url")
    template_name = "BlogApp/Article_form.html"
    context = {"form": form}
    return render(request, template_name, context)

#Delete
def deleteArticleView(request, f_uid):
    obj = Article.objects.get(id = f_uid)
    if request.method == "POST":
        obj.delete()
        return redirect("show_url")

    template_name = "BlogApp/show.html"
    context = {"obj": obj}
    return render(request, template_name, context)


#Search/Filter
def showArticleView(request):
    obj = Article.objects.all()
    t3 = obj[:3]
    template_name = "BlogApp/show.html"
    context = {"obj": obj,
               "t3": t3
               }
    return render(request, template_name, context)
