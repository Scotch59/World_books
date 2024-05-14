from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from .models import Author, Book, BookInstance
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import Form_add_author
from django.urls import reverse, reverse_lazy
from django import forms


class BookListView(ListView):
    model = Book
    context_object_name = 'books'
    paginate_by = 7


class BookDetailView(DetailView):
    model = Book
    context_object_name = 'book'


class AuthorListView(ListView):
    model = Author
    paginate_by = 7


class AuthorDetailView(DetailView):
    model = Author


# форма для изменения сведений об авторах
class Form_edit_author(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'


# Класс для создания БД новой записи о книге
class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('edit_books')


# Класс для обновления в БД записи о книге
class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('edit_books')

# класс для удаления из БД записи о книге
class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('edit_books')


def index(request):
    text_head = 'На нашем сайте вы можете получить книги в электроном виде'

    # Данные о книгах и их количестве
    books = Book.objects.all()
    num_books = Book.objects.all().count()

    # Данные об экземплярах книг в БД
    num_instances = BookInstance.objects.all().count()

    # Доступные книги (статус = На складе)
    num_instances_available = BookInstance.objects.filter(status__exact=2).count()

    # Данные об авторах книг
    authors = Author.objects
    num_authors = Author.objects.count()

    # Число посещений этого Views, подсчитанное в переменной session
    num_visit = request.session.get('num_visit', 0)
    request.session['num_visit'] = num_visit + 1

    # Словарь для передачи данных в шаблон index.html
    context = {'text_head': text_head, 'books': books, 'num_books': num_books,
               'num_instances': num_instances, 'num_instances_available': num_instances_available,
               'authors': authors, 'num_authors': num_authors, 'num_visit': num_visit}
    return render(request, 'catalog/index.html', context)

# функция представления сведении
def about(request):
    text_head = 'Мотивация'
    name = 'Выписки из книг!'
    rabl1 = 'Только овладение своими страстями и постоянный внутренний анализ дают нам возможность' \
            ' найти правильный путь, ведущий к вершинам добродетели и счастья. Достичь этого можно' \
            ' лишь во внутренней тишине, а не в суете общественной жизни.'
    rabl2 = 'Тем, кто не смог овладеть огромным состоянием, гораздо проще обрести' \
            ' специальные знания, нежели придумать какую-нибудь интересную идею!' \
            ' И именно по этой причине всегда существует спрос на тех, тко способен ' \
            ' помочь людям продать услуги с наибольшей выгодой'
    rabl3 = ''
    rabl4 = ''
    motiv1 = 'Не надо бояться густого тумана,' \
             ' не надо бояться пустого кармана,' \
             ' не надо бояться ни горных потоков, ни топей болотных, ни грязных поддонков.' \
             ' Умейте всем страхам в глаза рассмеяться, лишь собственной трусости надо бояться.' \
             ' Не надо бояться тяжелой задачи, а надо бояться дешевой удачи,' \
             ' не надо бояться быть честным и битым, а надо бояться быть лживым и сытым.' \
             ' Умейте всем страхам в глаза рассмеяться, лишь собственной трусости надо бояться.'
    motiv2 = 'Любой человек, даже без образования, может многому научиться сам и достичь' \
             'невероятного уровня профессионализма, преодолевая социальную дискриминацию'
    motiv3 = ''
    motiv4 = ''
    context = {'text_head': text_head, 'name': name, 'rabl1': rabl1, 'rabl2': rabl2, 'rabl3': rabl3, 'rabl4': rabl4,
               'motiv1': motiv1, 'motiv2': motiv2, 'motiv3': motiv3, 'motiv4': motiv4}
    return render(request, 'catalog/about.html', context)


# функция представления контактных данных
def contact(request):
    text_head = 'Контакты'
    name = 'Copyringht ООО "Scotch_entertainment"'
    telegram = 'https://t.me/Myshkin_Sergey'
    tel = '8-902-83-69-378'
    email = 'sereza.myshkin@gmail.com'
    context = {'text_head': text_head, 'name': name, 'telegram': telegram, 'tel': tel, 'email': email}
    return render(request, 'catalog/contact.html', context)


# функция редактирования информации об авторах
def edit_authors(request):
    author = Author.objects.all()
    context = {'author': author}
    return render(request, 'catalog/edit_authors.html', context)


# функция добавления нового автора, связанная с вышеуказанной функцией
def add_author(request):
    if request.method == 'POST':
        form = Form_add_author(request.POST, request.FILES)
        if form.is_valid():
            # получить данные из формы
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            date_of_birth = form.cleaned_data.get("date_of_birth")
            about = form.cleaned_data.get("about")
            photo = form.cleaned_data.get("photo")
            # создаем объект для записи в БД
            obj = Author.objects.create(
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                about=about,
                photo=photo)
            # сохранение полученных данных
            obj.save()
            # загрузить страницу сос списком авторов
            return HttpResponseRedirect(reverse('authors-list'))
    else:
        form = Form_add_author
        context = {"form": form}
        return render(request, 'catalog/authors_add.html', context)


# Удаление авторов из БД
def delete(request, id):
    try:
        author = Author.objects.get(id=id)
        author.delete()
        return HttpResponseRedirect("/edit_authors/")
    except:
        return HttpResponseNotFound("<h2>Автор не найден</h2>")


# изменение данных об авторе в БД
def edit_author(request, id):
    author = Author.objects.get(id=id)
    if request.method == 'POST':
        instance = Author.objects.get(pk=id)
        form = Form_edit_author(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/edit_authors/")
    else:
        form = Form_edit_author(instance=author)
        content = {'form': form}
        return render(request, "catalog/edit_author.html", content)


# вызов страницы для редактирования книг
def edit_books(request):
    book = Book.objects.all()
    context = {'book': book}
    return render(request, "catalog/edit_books.html", context)
