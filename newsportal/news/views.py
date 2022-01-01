from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from .forms import NewsForm, ReviewForm
from .models import News, TopNews, Category
import datetime

from .utils import searchNews, paginateNews


def home(request):
    news, search_query = searchNews(request)
    custom_range, news = paginateNews(request, news, 6)
    date = datetime.datetime.now()
    top = TopNews.objects.all()
    categories = Category.objects.all()
    context = {
        'news': news,
        'topNews': top,
        'categories': categories,
        'date': date,
        'search_query': search_query,
        'custom_range': custom_range
    }
    return render(request, 'index.html', context=context)


def Topic(request, pk):
    category_one = Category.objects.get(id=pk)
    categories = Category.objects.all()
    category_news = News.objects.filter(category=category_one)
    context = {
        'category_one': category_one,
        'news': category_news,
        'categories': categories
    }
    return render(request, 'category.html', context=context)


def singleNews(request, pk):
    news = News.objects.get(id=pk)
    categories = Category.objects.all()
    context = {
        'news': news,
        'categories': categories
    }

    projectObj = News.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()
        projectObj.getVoteCount

        messages.success(request, 'Your review was successfully submitted!')
        return redirect('project', pk=projectObj.id)
    return render(request, 'news/single-news.html', context=context)


@login_required(login_url="login")
def createNews(request):
    profile = request.user.profile
    form = NewsForm()

    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.owner = profile
            news.save()

            return redirect('account')

    context = {'form': form}
    return render(request, 'news/news_form.html', context)


@login_required(login_url='login')
def updateNews(request, pk):
    profile = request.user.profile
    news = profile.news_set.get(id=pk)
    form = NewsForm(instance=news)

    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            news = form.save()
            # tag
            return redirect('account')
    context = {
        'form': form,
        'news': news
    }
    return render(request, 'news/news_form.html', context)


@login_required(login_url='login')
def deleteNews(request, pk):
    profile = request.user.profile
    news = profile.news_set.get(id=pk)
    if request.method == 'POST':
        news.delete()
        return redirect('home')
    context = {'object': news}
    return render(request, 'delete_template.html', context)
