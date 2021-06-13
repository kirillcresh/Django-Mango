
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.views.generic import UpdateView, DeleteView

from .forms import CreateForm
from .models import Blog


class IndexView(generic.ListView):
    template_name = 'blogs/index.html'
    context_object_name = 'latest_blog_list'

    def get_queryset(self):
        return Blog.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Blog
    template_name = 'blogs/detail_blog.html'


def create(request):
    error =''
    if request.method == 'POST':
        form = CreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blogs:success_saved'))
        else:
            error = 'Error'

    form = CreateForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'blogs/create_blog.html', data)


def success_saved(request):
    return render(request, 'blogs/success_saved.html')


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = '/blogs/'
    template_name = 'blogs/delete_blog.html'


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ['title', 'content', 'pub_date', 'image']
    template_name = 'blogs/update_blog.html'


