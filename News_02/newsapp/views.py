from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from .models import *
from .filters import PostFilter
from .forms import PostForm, AuthorForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dateCreation'
    queryset = Post.objects.filter(categoryType='NW')
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


# class PostDetail(DetailView):
#     # Модель всё та же, но мы хотим получать информацию по отдельному товару
#     model = Post
#     # Используем другой шаблон — product.html
#     template_name = 'post.html'
#     # Название объекта, в котором будет выбранный пользователем продукт
#     context_object_name = 'post'

    # def index(request):
    #     return render(request, 'posts.html')


def post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'flatpages/post.html', {'post': post})


class PostSearch(PostsList):
    queryset = Post.objects.filter(categoryType='NW')
    ordering = 'dateCreation'
    template_name = 'flatpages/search.html'
    context_object_name = 'search'
    filter_class = PostFilter
    paginate = 10

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.get_filter().qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(
            self.request.GET, queryset=self.get_queryset())
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    template_name = 'flatpages/add.html'
    form_class = PostForm
    permission_required = ('newsapp.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        return super().form_valid(form)

    # def form_valid(self, form):
    #     self.object = services.create_news(form, self.request)
    #
    #     return super(generic.CreateView, self).form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    template_name = 'flatpages/edit.html'
    form_class = PostForm
    permission_required = ('newsapp.change_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(PermissionRequiredMixin, DeleteView):
    template_name = 'flatpages/delete.html'
    queryset = Post.objects.all()
    success_url = reverse_lazy('posts')
    permission_required = ('newsapp.delete_post',)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'author_update.html'
    form_class = AuthorForm

    def get_object(self, **kwargs):
        return self.request.user


class CategorySubscribeView(ListView):
    model = Category
    template_name = 'flatpages/post_category.html'
    context_object_name = 'post_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
def subscribe_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    id_u = request.user.id
    email = category.subscribers.get(id=id_u).email
    send_mail(
        subject=f'News Portal: подписка на обновления категории {category}',
        message=f'«{request.user}», вы подписались на обновление категории: «{category}».',
        from_email='leafarskill@yandex.ru',
        recipient_list=[f'{email}', ],
    )
    return redirect('/posts')


@login_required
def subscribe(request, pk):
    user = request.user
    subscriber = User.objects.filter().last()
    category = Category.objects.get(id=pk)
    category.subscribers.add(subscriber)

    html_content = render_to_string(
        'subscribe_created.html',
        {
            'subscribe': subscribe,
        }
    )

    # в конструкторе уже знакомые нам параметры, да? Называются правда немного по другому, но суть та же.
    msg = EmailMultiAlternatives(
        subject=f'Подписка на {category}',
        body=category,
        to=[user],  # это то же, что и recipients_list
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html

    msg.send()  # отсылаем

    return redirect(request.META.get('HTTP_REFERER'))
