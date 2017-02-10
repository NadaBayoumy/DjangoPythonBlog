#nada
from django.shortcuts import render
from django.template.context_processors import request
from .models import ForbiddenWords
from .forms import CategoryForm
from .forms import ForbiddenWordsForm
from .forms import PostForm
import re
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger #for pagination
from django.core import mail #for send email on subscription
#end nada

#alem
from .models import Category, Post, Reply
from .forms import Post_Form, Comment_Form
#end alem

#hossam
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from .forms import EditUserForm, CreateUserForm ,ChangePwForm
#end hossam



#simona
from .forms import RegistrationForm
#end simona



# Create your views here.

#category 
def all_category(request):
    all_category = Category.objects.all()
    context = {'all_category' : all_category}
    return render(request, 'BlogApp/list_category.html', context)




def new_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST) 
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/category/')
    context = {'category_form' : form }
    return render(request, 'BlogApp/category_form.html', context)



def edit_category(request, c_id):
    c = Category.objects.get(id= c_id)
    form = CategoryForm(instance= c)
    if request.method == 'POST':
        print("form method is post")
        form = CategoryForm(request.POST , instance= c)
        if form.is_valid():
            print("form method is valid")
            form.save()
            return HttpResponseRedirect('/category/')
    context = {'category_form' : form}
    return render(request, 'BlogApp/category_form.html', context)



def delete_category(request, c_id):
    category = Category.objects.get(id= c_id)
    category.delete()
    return HttpResponseRedirect('/category/')
#end category




#forbidden words
def all_forbidden_words(request):
    all_forbidden_words = ForbiddenWords.objects.all()
    context = {'all_forbidden_words' : all_forbidden_words}
    return render(request, 'BlogApp/list_forbidden_words.html', context)




def delete_forbidden_word(request, w_id):
    word = ForbiddenWords.objects.get(id= w_id)
    word.delete()
    return HttpResponseRedirect('/forbidden_words/')



def new_forbidden_word(request):
    form = ForbiddenWordsForm()
    if request.method == 'POST':
        form = ForbiddenWordsForm(request.POST) 
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/forbidden_words/')
    context = {'forbidden_words_form' : form }
    return render(request, 'BlogApp/forbidden_words_form.html', context)


#TO DO : take comment text to be replaced with the original comment on post
def check_forbidden_words_in_comment(request, comment_txt):
    coment_txt_arr = comment_txt.split(",")
    all_forbidden_words = ForbiddenWords.objects.all()
    for word in all_forbidden_words:
        replaced=""
        if comment_txt.find(word.forbiddenWord):
            for c in word.forbiddenWord:
                replaced+="*"
            comment_txt= comment_txt.replace(word.forbiddenWord,replaced)
           
    return HttpResponseRedirect('/forbidden_words/')
     
#end forbidden words




#posts 

def all_post(request):
    all_post = Post.objects.all()
    context = {'all_post' : all_post}
    return render(request, 'BlogApp/list_post.html', context)

def new_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST) 
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/post/')
    context = {'post_form' : form }
    return render(request, 'BlogApp/post_form.html', context)

def edit_post(request, p_id):
    p = Post.objects.get(id= p_id)
    form = PostForm(instance= p)
    if request.method == 'POST':
        form = PostForm(request.POST , instance= p)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/post/')
    context = {'post_form' : form}
    return render(request, 'BlogApp/post_form.html', context)

def delete_post(request, p_id):
    post = Post.objects.get(id= p_id)
    post.delete()
    return HttpResponseRedirect('/post/')

#end posts







#alem views



# Create your views here.

"""
    This function handles the view of subscribed categories and unsubscribed categories
    pattern is home/user_id

"""

def show_categories(request):
    #subquery that returns category objects that relates to a certain user who's id is attained from site parameters
    categories = Category.objects.all()
    categories_for_user = Category.objects.filter(id__in = Category.users.through.objects.filter(user_id = request.user.id).values_list('category_id'))
    subscribed = {}
    for category in categories_for_user:
        subscribed[category.id] = True
    context = {
        "categories": categories,
        "subscribed": subscribed,
        "user": request.user,
        "posts": Post.objects.all()
        }
    return render(request, "BlogApp/user_home.html", context)

"""
    This function handles the task of displaying all posts in a certain category
    pattern is home/user_id(not used in query)/category_id

"""

def show_posts(request, c_id):
    # returns all related posted to a certain category ordered by its date
    posts = Post.objects.filter(postCategory_id = c_id).order_by('postDate')
    #here pagination starts
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    #here pagination ends
    context = {"posts" : posts, 'user_id' : str(request.user.id), 'category_id' : c_id}

    return render(request, "BlogApp/posts.html", context)

"""
    This function handles the task of displaying a certain post and all its comments including replies
    pattern is home/user_id(not used)/category_id(not used)/post_id

"""

def post_display(request, c_id, p_id):
    post = Post.objects.get(pk = p_id) # returns an object contains all post info
    comments = Reply.objects.filter(postID_id = p_id) # returns an queryset contains all the comments/replies to this post

    # comment_dict key is the original comment id
    # where its value is a list that holds instances of replies to this particlar comment
    # Original comment will have key 0

    comments_dict = {}
    comments_dict[0] = []
    for comment in comments:
        #print "Checking", comment.comment_id
        if comment.comment_id is None:
            #print "None"
            comments_dict[0].append(comment) # pushing an original comment to the end of the list with key 0
            comments_dict[comment.id] = []
        else:
            #print comment, "Will be added"
            comments_dict[comment.comment_id].append(comment) # pushing a reply to the end of the list with its parent comment id as key
    comment_form = Comment_Form()
    """if request.method == "POST":
        comment_form = Comment_Form(request.POST)
        if comment_form.is_valid():
            comment_form = comment_form.save(commit = False)
            comment_form.userID = User.objects.get(pk = u_id)
            comment_form.postID = Post.objects.get(pk = p_id)
            comment_form.save()
            return HttpResponseRedirect("/home/" + u_id + "/" + c_id + "/" + p_id)
    """
    context = {
        'post' : post,
        'comments': comments_dict,
        'comment_form' : comment_form
        }
    return render(request, "BlogApp/post.html", context)

def check_profanity(content):
    filtered = ''
    first_word = True
    for word in content.split():
        if not first_word:
            filtered += ' '
        first_word = False
        if ForbiddenWords.objects.filter(forbiddenWord = word.lower()):
            filtered += ('*' * len(word))
        else:
            filtered += word
    return filtered

def add_comment(request, c_id, p_id):
    if request.method == "POST":
        comment_form = Comment_Form(request.POST)
        if comment_form.is_valid():
            comment_form = comment_form.save(commit = False)
            #comment_form.userID = User.objects.get(pk = request.user.id)
            comment_form.userID = request.user
            comment_form.postID = Post.objects.get(pk = p_id)
            comment_form.replyContent = check_profanity(comment_form.replyContent)
            comment_form.save()
            return HttpResponseRedirect("/home/" + c_id + "/" + p_id)

def add_reply(request, ca_id, p_id, co_id):
    if request.method == "POST":
        comment_form = Comment_Form(request.POST)
        if comment_form.is_valid():
            comment_form = comment_form.save(commit = False)
            #comment_form.userID = User.objects.get(pk = request.user.id)
            comment_form.userID = request.user
            comment_form.postID = Post.objects.get(pk = p_id)
            comment_form.comment = Reply.objects.get(pk = co_id)
            comment_form.replyContent = check_profanity(comment_form.replyContent)
            comment_form.save()
            return HttpResponseRedirect("/home/" + ca_id + "/" + p_id)


def subscribe_category(request, c_id):
    category = Category.objects.get(pk = c_id)
    #user = User.objects.get(pk = request.user.id)
    user = request.user
    category.users.add(user)
    return HttpResponseRedirect("/home/" + c_id)

def unsubscribe_category(request, c_id):
    category = Category.objects.get(pk = c_id)
    #user = User.objects.get(pk = request.user.id)
    user = request.user
    category.users.remove(user)
    return HttpResponseRedirect("/home/")

def add_new_post(request, c_id):
    form = Post_Form()
    if request.method == "POST":
        form = Post_Form(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit = False)
            #form.userID = User.objects.get(pk = request.user.id)
            form.userID = request.user
            form.postCategory = Category.objects.get(pk = c_id)
            form.postContent = check_profanity(form.postContent)
            form.save()
            return HttpResponseRedirect("/home/" + c_id)
    context = {'form' : form}
    return render(request, "BlogApp/new_post.html", context)

def modify_post(request, c_id, p_id):
    post = Post.objects.get(pk = p_id)
    form = Post_Form(instance = post)
    if request.method == 'POST':
        form = Post_Form(request.POST, instance = post)
        if form.is_valid():
            form = form.save(commit = False)
            #form.userID = User.objects.get(pk = request.user.id)
            form.userID = request.user
            form.postCategory = Category.objects.get(pk = c_id)
            form.postContent = check_profanity(form.postContent)
            form.save()
            return HttpResponseRedirect("/home/" + c_id)
    context = {'form' : form}
    return render(request, "BlogApp/new_post.html", context)

def delete_post(request, c_id, p_id):
    post = Post.objects.get(pk = p_id)
    post.delete()
    return HttpResponseRedirect("/home/" + c_id)


#alem views ends









#################################################################
#hossam
#################################################################
# Create your views here.


def login_user(request):
    """ This view render the login page for normal users"""
    if not request.user.is_authenticated:
        active = True   # If user is inactive it will be reassigned to FALSE!
        is_user = True  # Checks if the given username and password belongs to some user or not.
        if request.POST:
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                try:
                    user = User.objects.get(username=username)
                    if check_password(password, user.password):
                        active = user.is_active
                    else:
                        is_user = False
                except ObjectDoesNotExist:
                    is_user = False
        return render(request, 'BlogApp/login_user.html', {'active': active, 'is_user': is_user})
    else:
        return HttpResponseRedirect('/')


def login_admin(request):
    """ This view render the login page for admins """
    if not request.user.is_authenticated:
        is_super = True     # changes to FALSE if the user is not a superuser
        if request.POST:
            admin_name = request.POST['admin_name']
            admin_pw = request.POST['admin_pw']

            user = authenticate(username=admin_name, password=admin_pw)
            if user is not None and user.is_superuser:
                login(request, user)
                return HttpResponseRedirect('/users/')
            else:
                is_super = False
        return render(request, 'BlogApp/login_admin.html', {'is_super': is_super})
    else:
        return HttpResponseRedirect('/')

def users_list(request):
    """ Lists the users for admin for the CRUD operations. With 2 options,
    block/unblock and promote/un-promote to/from admin"""
    if request.user.is_superuser:   # Checks if admin else redirect the user to home page.
        users = User.objects.all()
        context = {'users': users}
        return render(request, 'BlogApp/users_list.html', context)
    else:
        return HttpResponseRedirect('/')


def block_user(request, user_id):
    """ Block/unblock user """
    if request.user.is_superuser:   # Checks if admin else redirect the user to home page.
        user = User.objects.get(pk=user_id)
        user.is_active = not user.is_active
        user.save()
        return HttpResponseRedirect('/users')
    else:
        return HttpResponseRedirect('/')


def promote_user(request, user_id):
    """ Promote/un-promote user to/from admin"""
    if request.user.is_superuser:   # Checks if admin else redirect the user to home page.
        user = User.objects.get(pk=user_id)
        user.is_superuser = not user.is_superuser
        user.save()
        return HttpResponseRedirect('/users')
    else:
        return HttpResponseRedirect('/')


def change_pw(request, user_id):
    """ Change password:
        1- Admin can change password of any user, but NOT other admins.
        2- User can change only his/her password. """
    done = False    # Checks if password has changed to display a paragraph in the template says that pw has changed.
    user = get_object_or_404(User, pk=user_id)
    if request.user.is_superuser and user.is_superuser and request.user.pk != user_id:
        return HttpResponse("You can't change other admin's password!")
    elif request.user.is_superuser or request.user.pk == user_id:
        form = ChangePwForm(instance=user)
        if request.method == 'POST':
            form = ChangePwForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                done = True
                return render(request, 'BlogApp/change_pw.html', {'form': form, 'done': done})
        return render(request, 'BlogApp/change_pw.html', {'form': form, 'done': done})
    else:
        return HttpResponseRedirect('/')

""" Admin CRUD OPERATIONS """


def edit_user(request, user_id):
    if request.user.is_superuser:   # Checks if admin else redirect the user to home page.
        user = get_object_or_404(User, pk=user_id)
        form = EditUserForm(instance=user)
        if request.method == 'POST':
            form = EditUserForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/users/')
        return render(request, 'BlogApp/edit_user.html', {'form': form, 'user': user})
    else:
        return HttpResponseRedirect('/')


def create_user(request):
    if request.user.is_superuser:   # Checks if admin else redirect the user to home page.
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/users/')
        return render(request, 'BlogApp/new_user.html', {'form': form})
    else:
        return HttpResponseRedirect('/')


def delete_user(request, user_id):
    if request.user.is_superuser:   # Checks if admin else redirect the user to home page.
        user = get_object_or_404(User, pk=user_id)
        user.delete()
        return HttpResponseRedirect('/users/')
    else:
        return HttpResponseRedirect('/')


###################################################################################
#endhossam
###################################################################################




#simona


#function to go home to choose between(rigester as user or adimn or login)
def Home_options(request):
    helloText='welcome :)'
    context = {'category_form' : helloText}
    #return HttpResponseRedirect('BlogApp/home.htm')
    return render(request,'BlogApp/home.html',context)

def registration(request):
    form = RegistrationForm()
    if request.method=='POST':
        form = RegistrationForm(request.POST)
#         print(form.data)
        if form.is_valid():
            form.save()
            name=form.data['username']
            obj = User.objects.get( username= name)
#             uid=obj.id
#             user = User.objects.get(id=1)
            group = Group.objects.get(id=1)
            obj.groups.add(group)
#             group = auth_user_groups.objects.create(user_id=uid, group_id=1)
            group.save()
            #here we will add contanier
            return HttpResponseRedirect("/login")
    context = {'registration_form' : form }
    return render(request, 'BlogApp/registration.html',context)

def manage(request):
    if request.user.is_superuser:
        return render(request,'BlogApp/mange.html',{})
    else:
        return HttpResponseForbidden()

#end simona
