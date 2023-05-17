
from django.shortcuts import render,HttpResponseRedirect,get_object_or_404
from django.views.generic import CreateView,UpdateView,ListView,DetailView,TemplateView,DeleteView
from App_Blog.forms import commmentForm
from django.contrib import messages
from App_Blog.models import Blog,comment,Likes
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from App_Login.token import account_activation_token
from django.core.mail import EmailMessage,send_mail
from django.conf import settings
from django.db.models import Q

# Create your views here.
@ login_required
def favblog(request):
    new = Blog.objects.filter(favourites=request.user)
    return render(request,
                  'App_Blog/favourites.html',
                  {'new': new})

@ login_required
def favourite_add(request, pk):
    blogs = Blog.objects.all()
    blog = get_object_or_404(Blog, id=pk)
    fav = bool
    if blog.favourites.filter(id=request.user.id).exists():
        blog.favourites.remove(request.user)
        fav = False
    else:
        blog.favourites.add(request.user)
        fav = True
    # return render(request,'App_Blog/blog_list.html',{'blogs':blogs,'fav':fav})
    
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

class MyBlog(LoginRequiredMixin,TemplateView):
    template_name = "App_Blog/myblog.html"

class updateBlog(UpdateView,LoginRequiredMixin):
    model = Blog
    fields = ('blog_title','blog_content','blog_image')
    template_name = "App_Blog/edit_blog.html"

    def get_success_url(self,**kwargs) :
        return reverse_lazy('blog_details',kwargs={'pk':self.object.id})
        # return HttpResponseRedirect(reverse('home'))

def BlogList(requests):
    blogs = Blog.objects.all()
    

    
    return render(requests,'App_Blog/blog_list.html',{'blogs':blogs})



# class BlogList(ListView):
#     context_object_name = 'blogs'
#     model = Blog
#     template_name = 'App_Blog/blog_list.html'
    

    
    # def get_context_data(self, *args, **kwargs):
    #     context = super(BlogList, self).get_context_data(*args, **kwargs)
    #     blog = get_object_or_404(Blog,id = self.request.user.id)
    #     context['fav'] = False
    #     if self.blog.favourites.filter(id=self.request.user.id).exists():
    #         context['fav'] = False
    #     return context
    

    
    # queryset = Blog.objects.order_by('-publish_date')
    

def searchview(request):
    query = request.GET.get('search')
    print(query)
    if query:
          postresult = Blog.objects.filter(blog_title__contains=query)
          results = postresult
    else:
        results = None
    return render(request,'App_Blog/search_list.html',{'results':results})

      

def getemail(request):
    user_email = request.user.email
    return user_email


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
        # messages.success(self,"Blog created successfully")
        messages.add_message(self.request, messages.INFO, 'Blog created successfully')
        
        mail_subject = 'Blog Created Successfully '  
        message = render_to_string('App_Blog/active_email.html', {  
            'user': self.request.user,  
             
        })  
        user_email= getemail(self.request)
        # print(user_email)
        send_mail(  
                    mail_subject,message, settings.EMAIL_HOST_USER ,[user_email]  
        )  
        # email.send()  
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
    messages.add_message(request, messages.INFO,'Blog Deleted successfully')
        
    mail_subject = 'Blog Deleted Successfully '  
    message = render_to_string('App_Blog/delete_email.html', {  
        'user': request.user,  
            
    })  
    user_email= getemail(request)
    # print(user_email)
    send_mail(  
                mail_subject,message, settings.EMAIL_HOST_USER ,[user_email]  
    )  
    return HttpResponseRedirect(reverse('myblog'))
