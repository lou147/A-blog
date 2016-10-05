from django.shortcuts import render
from blog.models import Post
from django.http import Http404


def categories(request):
    cate_list_all = []
    post_list = Post.objects.all()
    for post in post_list:
        cate = post.category
        cate_list_all.append(cate)
    cate_list = list(set(cate_list_all))

    context = {
        'cate_list': cate_list,
        'post_list': post_list,
    }
    return render(request, 'categories.html', context)


def categories_detail(request, cate):
    try:
        post_list = Post.objects.filter(category__iexact=cate)
        num = post_list.count()
    except Post.DoesNotExist:
        raise Http404
    return render(request, 'cate_detail.html', {'post_list': post_list, 'cate': cate, 'num': num})



