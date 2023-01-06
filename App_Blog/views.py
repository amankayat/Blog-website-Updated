import pkgutil
from django.shortcuts import render,HttpResponseRedirect
from django.views.generic import CreateView,UpdateView,ListView,DetailView,TemplateView,DeleteView
from App_Blog.forms import commmentForm

from App_Blog.models import Blog,comment,Likes
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
# Create your views here.

class MyBlog(LoginRequiredMixin,TemplateView):
    template_name = "App_Blog/myblog.html"

class updateBlog(UpdateView,LoginRequiredMixin):
    model = Blog
    fields = ('blog_title','blog_content','blog_image')
    template_name = "App_Blog/edit_blog.html"

    def get_success_url(self,**kwargs) :
        return reverse_lazy('blog_details',kwargs={'pk':self.object.id})
        # return HttpResponseRedirect(reverse('home'))

class BlogList(ListView):
    context_object_name = 'blogs'
    model = Blog
    template_name = 'App_Blog/blog_list.html'
    # queryset = Blog.objects.order_by('-publish_date')



class CreateBlog(LoginRequiredMixin,CreateView):
    model  = Blog
    template_name = 'App_Blog/create_blog.html'
    fields = ('blog_title','blog_content','blog_image')

    def form_valid(self,form):
        blog_obj = form.save(commit=False)
        blog_obj.author = self.request.user
        title = blog_obj.blog_title
        blog_obj.slug = title.replace(" ","-")+ "-"+str(uuid.uuid4)
        blog_obj.save()
        return HttpResponseRedirect(reverse('home'))


def blog_details(requests,pk):
    blog = Blog.objects.get(pk=pk)
    comment_form = commmentForm()
    already_liked = Likes.objects.filter(blog=blog,user=requests.user)
    if already_liked:
        liked = True
    else:
        liked = False
    if requests.method == "POST":
        comment_form = commmentForm(requests.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = requests.user
            comment.blog = blog
            comment.save()
            return HttpResponseRedirect(reverse('blog_details',kwargs = {'pk':pk}))
    return render(requests,'App_Blog/blog_details.html',{'blog':blog,'comment_form':comment_form,'liked':liked})


@login_required
def liked(requests,pk):
    blog = Blog.objects.get(pk=pk)
    user = requests.user
    already_liked = Likes.objects.filter(blog=blog,user=user)
    if not already_liked:
        liked_post =Likes(blog=blog,user=user)
        liked_post.save()
    return HttpResponseRedirect(reverse('blog_details',kwargs={'pk':blog.pk}))

@login_required
def unlike(requests,pk):
    
    blog = Blog.objects.get(pk=pk)
    user = requests.user
    already_liked = Likes.objects.filter(blog=blog,user=user)
    already_liked.delete()
    return HttpResponseRedirect(reverse('blog_details',kwargs={'pk':blog.pk}))


def blogdelete(request,pk):
    blg = Blog.objects.get(pk=pk)
    blg.delete()
    return HttpResponseRedirect(reverse('home'))
