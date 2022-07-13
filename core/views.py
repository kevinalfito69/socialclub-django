import profile
from django.shortcuts import render, redirect,  get_object_or_404  
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Profile, Post, comment, LikePost

from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/signin', redirect_field_name='you_moust_login')
def index(request):
    user_object = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user = user_object)
    post_feed = Post.objects.all()
    # post_profileimg = Profile.objects.get(user = post_feed.user)
    context={
        'user_profile': user_profile,
        'post_feed': post_feed,
        # 'post_profileimg': post_profileimg
    }
    return render(request, 'index.html', context )
@login_required(login_url='/signin', redirect_field_name='you_moust_login')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES['image']
        caption = request.POST['caption']
        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')

def commentViews(request, ):
    if request.method == 'POST':
        post_id = request.GET.get('post_id')
        user = request.user.username
        comment = request.POST['comment']
        new_comment = Post.comment.create(user=user, comment=comment)
        new_comment.save()
        return redirect('/')
    else:
        return redirect('/')

def profile(request, pk):
    user_object = User.objects.get(username = pk)
    user_profile = Profile.objects.get(user = user_object)
    user_post = Post.objects.filter(user=pk)
    user_post_length = len(user_post)
    context ={
        'user_object': user_object,
        'user_profile':user_profile,
        'user_post':user_post,
        'user_post_length':user_post_length
    }
    return render(request, 'profile.html', context)

@login_required(login_url='/signin', redirect_field_name='you_moust_login')
def like(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    like_filter = LikePost.objects.filter(post_id=post_id,  username=username).first()
    if like_filter is None:
        new_like = LikePost.objects.create(post_id=post_id,  username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes +1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')

def signup(request):
    if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']
            if password == password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username Taken')
                    return redirect('signup')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email Taken')
                    return redirect('signup')
                else:
                    user = User.objects.create_user(username=username, email=email , password=password)
                    user.save()
                    user_login = auth.authenticate(username=username, password=password)
                    auth.login(request, user_login)
                    # create profile from user
                    user_model = User.objects.get(username = username)
                    new_profile = Profile.objects.create(user=user_model, id_user = user_model.id)
                    new_profile.save()
                    # user redirect to settings
                    return redirect('settings')
            else:   
                messages.info(request, 'Password not matching')
                return redirect('signup')
    else:       
        return render(request, 'signup.html')

@login_required(login_url='/signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    user = User.objects.get(username=request.user)
    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            bio = request.POST['bio']
            location = request.POST['location']
            birth_date = request.POST['birth_date']
            user_profile.profileimg = image
            user.first_name = first_name
            user.last_name = last_name
            user_profile.bio = bio
            user_profile.location = location
            user_profile.birth_date = birth_date
            user.save()
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES['image']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            bio = request.POST['bio']
            location = request.POST['location']
            birth_date = request.POST['birth_date']
            user_profile.profileimg = image
            user.first_name = first_name
            user.last_name = last_name
            user_profile.bio = bio
            user_profile.location = location
            user_profile.birth_date = birth_date
            user.save()
            user_profile.save()

        return redirect('settings')
    return render(request,'setting.html',{'user_profile':user_profile})

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('signin')
    else:
        return render(request, 'signin.html')
@login_required(login_url='/signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')