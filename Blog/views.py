from django.shortcuts import render
from Blog.models import Post


def blog(request):
    all_post = Post.objects.all()
    if all_post.exists():
        context = {
            'all_post' : all_post,
        }
        return render(request, 'Blogs\Blog.html', context)
    else:
        return render(request, 'Blogs\Blog.html')


def post_detail(request, slug):
    try:
        post = Post.objects.get(slug=slug)
        context = {
            'post' : post,
        }
        print(post)
        return render(request, 'Blogs\Post_detail.html', context)
    except:
        context = {
            'message' : 'Something Went Wrong',
        }
        return render(request, 'Blogs\Post_detail.html', context)


