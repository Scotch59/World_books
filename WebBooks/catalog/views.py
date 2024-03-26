from django.shortcuts import render
from .models import Author, Book, BookInstance
from django.views.generic import ListView, DetailView
from django.http import HttpResponse


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


def about(request):
    text_head = 'Сведения о компании'
    name = 'ООО «Интеллектуальные информационные системы»'
    rabl1 = 'Разработка приложений на основе систем искусственного интеллекта'
    rabl2 = 'Распознание объектов дорожной инфраструктуры'
    rabl3 = 'Создание графических АРТ-объектов на основе систем искусственного интеллекта'
    rabl4 = 'Создание цифровых интерактивных книг, учебных пособий автоматизированных обучающих систем'
    context = {'text_head': text_head, 'name': name, 'rabl1': rabl1, 'rabl2': rabl2, 'rabl3': rabl3, 'rabl4': rabl4}
    return render(request, 'catalog/about.html', context)


def contact(request):
    text_head = 'Контакты'
    name = 'ООО «Интеллектуальные информационные системы»'
    address = 'Москва, ул. Планерная, д. 20, к. 1'
    tel = '495-345-45-45'
    email = 'iis_info@mail.ru'
    context = {'text_head': text_head, 'name': name, 'address': address, 'tel': tel, 'email': email}
    return render(request, 'catalog/contact.html', context)