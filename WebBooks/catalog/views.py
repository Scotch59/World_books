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
    paginate_by = 5


class BookDetailView(DetailView):
    model = Book
    context_object_name = 'book'


class AuthorListView(ListView):
    model = Author
    paginate_by = 5


class AuthorDetailView(DetailView):
    model = Author


# форма для изменения сведений об авторах
class Form_edit_author(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'


# Класс для создания БД новой записи о книге
class BookCreate(CreateView):
    model =Book
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
    text_head = 'Сведения о компании'
    name = 'ООО «Интеллектуальные информационные системы»'
    rabl1 = 'Разработка приложений на основе систем искусственного интеллекта'
    rabl2 = 'Распознание объектов дорожной инфраструктуры'
    rabl3 = 'Создание графических АРТ-объектов на основе систем искусственного интеллекта'
    rabl4 = 'Создание цифровых интерактивных книг, учебных пособий автоматизированных обучающих систем'
    context = {'text_head': text_head, 'name': name, 'rabl1': rabl1, 'rabl2': rabl2, 'rabl3': rabl3, 'rabl4': rabl4}
    return render(request, 'catalog/about.html', context)


# функция представления контактных данных
def contact(request):
    text_head = 'Контакты'
    name = 'ООО «Интеллектуальные информационные системы»'
    address = 'Москва, ул. Планерная, д. 20, к. 1'
    tel = '495-345-45-45'
    email = 'iis_info@mail.ru'
    context = {'text_head': text_head, 'name': name, 'address': address, 'tel': tel, 'email': email}
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
