from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from catalog.models import Author, Book, BookInstance, Genre, Language
import datetime



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
class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    paginate_by = 5


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book


class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    paginate_by = 5

class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
  model = Author

class LangListView(LoginRequiredMixin, generic.ListView):
  model = Language

class LangDetailView(LoginRequiredMixin, generic.DetailView):
  model = Language

class GenreListView(LoginRequiredMixin, generic.ListView):
  model = Genre

class GenreDetailView(LoginRequiredMixin, generic.DetailView):
    model = Genre

class LoannedBooksByUserListView(LoginRequiredMixin, generic.ListView):
  """
   Generic CBV for listing books on loan to current user.
  """
  model = BookInstance
  template_name = 'catalog/bookinstance_list_borrowed_user.html'
  paginate_by = 5

  def get_queryset(self):
    return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_date')

class AllBorrowedBooksListView(PermissionRequiredMixin, generic.ListView):
  permission_required = 'can_mark_returned'
  # I'm going a slightly more convoluated route and organising our borrowed books by User.  I think this would allow librarians to spot repeat offenders easier.
  model = User
  paginate_by = 5
  template_name='catalog/all_borrowed_books.html'

  def get_queryset(self):
    return User.objects.filter(borrowed_books__isnull=False).distinct()

class BorrowedBookDetailView(PermissionRequiredMixin, generic.DetailView):
  """
   The purpose for this CBV is really a custom POST method that allows a librarian to check books back into stock.
  """
  permission_required='can_mark_returned' # only librarians have this permission
  model = BookInstance

  def post(self, request, *args, **kwargs):
    """
     Checking a book in.
    """
    book_inst = self.get_object()
    book_inst.status = 'a' # Marking the book as available
    book_inst.due_date = None # Setting the due date to None
    book_inst.borrower = None # Setting the borrower to Nonen
    book_inst.save()
    return HttpResponseRedirect(reverse('catalog:all-books'))

class CheckoutBookInstance(LoginRequiredMixin, generic.DetailView):
  """
   The purpose for this CBV is a custom POST method that allows library patrons (and librarians) to check out books.
  """
  model = BookInstance

  def post(self, request, *args, **kwargs):
    """
     Checking out a book.
    """
    # Setting a 2 week period a patron can check a book out for.
    checkout_period = datetime.timedelta(weeks=2)
    book_inst = self.get_object()
    book_inst.status = 'o'
    book_inst.due_date = datetime.date.today() + checkout_period
    book_inst.borrower = request.user
    book_inst.save()
    return HttpResponseRedirect(reverse('catalog:my-borrowed-books'))
