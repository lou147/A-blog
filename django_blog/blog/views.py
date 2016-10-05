from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import PostForm, UserForm, UserRegisterForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.utils.http import quote_plus
from django.contrib.auth.decorators import user_passes_test


def home(request):
    template = 'home.html'
    post_list = Post.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        post_list = Post.objects.all()
    query = request.GET.get('q')
    if query:
        post_list = post_list.filter(
            Q(content__icontains=query) |
            Q(title__icontains=query)
        ).distinct()
    paginator = Paginator(post_list, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:

        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'post_list': posts,
    }
    return render(request, template, context)


def detail(request, slug=None):
    article = get_object_or_404(Post, slug=slug)
    try:
        next_article = article.get_previous_by_timestamp()
    except Post.DoesNotExist:
        next_article = None
    try:
        old_article = article.get_next_by_timestamp()
    except Post.DoesNotExist:
        old_article = None
    # if not request.user.is_staff or not request.user.is_superuser:
    #     raise Http404
    share_string = quote_plus(article.content)
    content_type = ContentType.objects.get_for_model(Post)
    obj_id = article.id
    Post.objects.get(id=article.id)
    comments = Comment.objects.filter(content_type=content_type, object_id=obj_id)

    initial_data = {
        'content_type': article.get_content_type,
        'object_id': article.id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        c_type = form.cleaned_data.get('content_type')
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get('content')
        parent_obj = None
        try:
            parent_id = int(request.POST.get('parent_id'))
        except:
            parent_id = None
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs[0]

        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj,
        )
        return HttpResponseRedirect(article.get_absolute_url())

    context = {
        'title': article.title,
        'content': article.content,
        'image': article.image,
        'date': article.timestamp,
        'cate': article.category,
        'share_string': share_string,
        'comments': comments,
        'comment_form': form,
        'old_article': old_article,
        'next_article': next_article,
        'slug': article.slug,
    }
    return render(request, 'detail.html', context)


@user_passes_test(lambda u: u.is_superuser)
def create(request):
    species = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'form': form,
        'species': species
    }
    return render(request, 'create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def edit(request, slug=None):
    species = 'Edit'
    article = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=article)
    if form.is_valid():
        article = form.save(commit=False)
        article.save()
        return HttpResponseRedirect(article.get_absolute_url())

    context = {
        'species': species,
        'title': article.title,
        'content': article.content,
        'image': article.image,
        'form': form,
    }
    return render(request, 'create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def delete(request, slug=None):
    article = get_object_or_404(Post, slug=slug)
    article.delete()
    return redirect('home')


def register(request):
    registered = False
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        login(request, user)
        registered = True
    if registered is True:
        return redirect('home')
    context = {
        'form': form,
        'registered': registered
    }
    return render(request, 'register.html', context)


def user_login(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('home')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


# class CommentPostView(FormView):
#     form_class = BlogCommentForm
#     template_name = 'detail.html'
#
#     def form_valid(self, form):
#         target_article = get_object_or_404(Post, id=None)
#         comment = form.save(commit=False)
#         comment.article = target_article
#         comment.save()
#
#         self.success_url = target_article.get_absolute_url()
#         return HttpResponseRedirect(self.success_url)
#
#     def form_invalid(self, form):
#         target_article = get_object_or_404(Post, id=id)
#
#         return render(self, 'blog/detail.html', {
#             'form': form,
#             'article': target_article,
#             'comment_list': target_article.blogcomment_set.all(),
#         })

def test(request):
    species = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'form': form,
        'species': species
    }
    return render(request, 'create.html', context)
