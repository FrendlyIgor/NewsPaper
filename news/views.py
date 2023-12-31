from typing import Any, Dict
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, User, Author
from datetime import datetime
from django.shortcuts import render
from .filters import PostFilter
from django.core.paginator import Paginator
from django.views import View
from .forms import PostForm
from django.urls import reverse_lazy


    # Create your views here.
class PostList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'news/posts.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'posts'
    ordering = ['-id']
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['choices'] = Post.how_choise
        context['form'] = PostForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST) # создаём новую форму, забиваем в неё данные из POST-запроса
        if form.is_valid(): # если пользователь ввёл всё правильно и нигде не накосячил, то сохраняем новый товар
           form.save()
        return super().get(request, *args, **kwargs)
    
        # дженерик для получения деталей о посте    
class PostDetailView(DetailView):
   template_name = 'news/post_detail.html'
   queryset = Post.objects.all()

    # дженерик для создания объекта. Надо указать только имя шаблона и класс формы
class PostCreateView(CreateView):
    template_name = 'news/post_add.html'
    form_class = PostForm
    
    # дженерик для редактирования объекта
class PostUpdateView(UpdateView):
    template_name = 'news/post_edit.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
   
   
    # дженерик для удаления товара
class PostDeleteView(DeleteView):
    template_name = 'news/post_delete.html'
    queryset = Post.objects.all()
    success_url = reverse_lazy('news:posts') # не забываем импортировать функцию reverse_lazy из пакета django.urls
    
    
class PostDetail(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'

class Posts(View):

   def get(self, request):
        posts = Post.objects.order_by('-id')
        p = Paginator(posts, 1) # Создаём объект класса пагинатор, передаём ему список наших товаров и их количество для одной страницы
        posts = p.get_page(request.GET.get('page', 1)) # Берём номер страницы из get-запроса. Если ничего не передали, будем показывать первую страницу
        # Теперь вместо всех объектов в списке товаров хранится только нужная нам страница с товарами

        data = {
        'posts': posts,
        }

        return render(request, 'news/posts.html', data)

""" class AuthorList(ListView):
    model = Author  # указываем модель, объекты которой мы будем выводить
    template_name = 'news/authors.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'authors'
    queryset = Author.objects.order_by('-id')

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context

class AuthorDetail(DetailView):
    model = User
    template_name = 'news/author.html'
    context_object_name = 'author' """

class postSearch(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'news/search.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'posts'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    ordering = ['-id'] # сортировка по цене в порядке убывания
    paginate_by = 1 # поставим постраничный вывод в один элемент
  
        # метод get_context_data нужен нам для того, чтобы мы могли передать переменные в шаблон. В возвращаемом словаре context будут храниться все переменные. Ключи этого словари и есть переменные, к которым мы сможем потом обратиться через шаблон
    def get_context_data(self, **kwargs): # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        return context
