from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, ProfileForm, InterestForm, MessageForm
from .models import Profile, Interest
from news.models import Category, News




def loginUser(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)

        except:
            print("Username does not exist")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username does not exist')

    return render(request, 'user/sigin.html')


def logoutUser(request):
    logout(request)
    messages.info(request, 'User Successfully logout')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created !')

            login(request, user)
            return redirect('home')
        else:
            messages.success(request, 'An error has occurred during registration')
    context = {
        'page': page,
        'form': form
    }

    return render(request, 'user/signup.html', context=context)


@login_required(login_url='login')
def profile(request, pk):
    profile = Profile.objects.get(id=pk)
    categories = Category.objects.all()
    news = profile.news_set.all()
    context = {
        'profile': profile,
        'categories': categories,
        'news': news
    }
    return render(request, 'user/profile.html', context=context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    interest = Interest.objects.filter(owner=profile)
    news = profile.news_set.all()
    categories = Category.objects.all()
    context = {
        'profile': profile,
        'interests': interest,
        'news': news,
        'categories': categories
    }
    return render(request, 'user/account.html', context=context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'user/profile_form.html', context=context)


@login_required(login_url='login')
def createInterest(request):
    profile = request.user.profile
    form = InterestForm()

    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            interest = form.save(commit=False)
            interest.owner = profile
            interest.save()
            messages.success(request, 'Interest was added successfully!')
            return redirect('account')

    context = {'form': form}
    return render(request, 'user/Interest_form.html', context)


@login_required(login_url='login')
def updateInterest(request, pk):
    profile = request.user.profile
    interest = profile.interest_set.get(id=pk)
    form = InterestForm(instance=interest)

    if request.method == 'POST':
        form = InterestForm(request.POST, instance=interest)
        if form.is_valid():
            form.save()
            messages.success(request, 'Interest was updated successfully!')
            return redirect('account')

    context = {'form': form}
    return render(request, 'user/Interest_form.html', context)


@login_required(login_url='login')
def deleteInterest(request, pk):
    profile = request.user.profile
    interest = profile.interest_set.get(id=pk)
    if request.method == 'POST':
        interest.delete()
        messages.success(request, 'Interest was deleted successfully!')
        return redirect('account')

    context = {'object': interest}
    return render(request, 'delete_template.html', context)



@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}
    return render(request, 'user/inbox.html', context)


@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'user/message.html', context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Your message was successfully sent!')
            return redirect('profile', pk=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'user/message_form.html', context)