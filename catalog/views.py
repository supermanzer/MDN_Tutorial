from django.shortcuts import render
from django.views import generic
from catalog.models import Author, Book, BookInstance, Genre, Language



def index(request):
  """
   A simple rendering of the library homepage.
  """
  context = {
  'user': request.user,
  'num_authors': Author.objects.all().count(),
  'num_books': Book.objects.all().count(),
  'num_instances': BookInstance.objects.all().count(),
  'num_languages': Language.objects.all().count(),
  'num_genres': Genre.objects.all().count()}

  # Getting the number of times a specfici user (browser) has visited this site.
  num_visits = request.session.get('num_visits', 0)
  request.session['num_visits'] = num_visits +1

  context['num_visits'] = num_visits
  return render(request, template_name='catalog/index.html', context=context)

# Transitioning to class based, generic views because of the wonderful brevity of code required.
class BookListView(generic.ListView):
    model = Book
    paginate_by = 5


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 5

class AuthorDetailView(generic.DetailView):
  model = Author

class LangListView(generic.ListView):
  model = Language

class LangDetailView(generic.DetailView):
  model = Language

class GenreListView(generic.ListView):
  model = Genre

class GenreDetailView(generic.DetailView):
    model = Genre
