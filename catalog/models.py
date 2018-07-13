"""
 catalog/models.py
 ----------------------------------------------------------
 A place to define model instances for the Catalog application.
 Remember to define SlugFields for each model we wish to represent in
 our REST API. This will allow us to provide more meaningful URLs and
 improve the SEO.
"""
from django.db import models
from django.urls import reverse

class Genre(models.Model):
    """
    Model representing a genre of literature.
    """
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('auth.User', related_name='genres_created', null=True, on_delete=models.SET_NULL)
    modified_by = models.ForeignKey('auth.User', related_name='genres_modified', null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=True, null=True, help_text='A genre of literature that can be applied to bookd.')

    def __str__(self):
       """
       String for representing a model object
       """
       return self.name

    def get_absolute_url(self):
      return reverse('catalog:genre-detail', kwargs={'pk': self.id, 'genre': self.name})

class Book(models.Model):
    """
    Model representing a book (but not a specific book instance.)
    """
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('auth.User', related_name='books_created', on_delete=models.SET_NULL, null=True)
    modified_by = models.ForeignKey('auth.User', related_name='books_modified', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200, blank=True, null=True, db_index=True, help_text='Enter the book\'s title')
    author = models.ManyToManyField('Author')
    summary=models.TextField(blank=True, null=True, help_text='Enter a brief description of the book.')
    isbn = models.CharField('ISBN',max_length=13, blank=True, null=True, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField('Genre')
    slug = models.SlugField(max_length=30, db_index=True)

    class Meta:
        ordering = ['title', ]
    def __str__(self):
       """
       String representing a book object
       """
       return self.title

    def get_absolute_url(self):
       """
       Returns the url to access the detail record for this book.
       """
       return reverse('catalog:book-detail', kwargs={'id': str(self.id), 'slug': self.slug})

    def save(self):
       """
       Overriding default save behavior to ensure slug generation
       """
       if not self.slug:
         # TODO (ryan@gensci.org): Import slugify function and use it on the title.
         # Custom alternative:
         if not self.slug:
             self.slug = '-'.join(self.title.lower().split(' '))

       super(Book, self).save()

    def display_author(self):
      """
       Create string representation of the Author(s) for this book.
      """
      return ', '.join([f'{author.first_name} {author.last_name}' for author in self.author.all()])
    display_author.short_description = 'Author(s)'

    def display_genre(self):
       """
       Creating a string representation of the genre(s) for this book.
       """
       return ', '.join(genre.name for genre in self.genre.all())
    display_genre.short_description='Genre(s)'


import uuid # Required for uique book instance
class BookInstance(models.Model):
    """
    Model representing a specific physical (or digital) copy of a book.
    """
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('auth.User', related_name='instances_created', on_delete=models.SET_NULL, null=True)
    modified_by = models.ForeignKey('auth.User', related_name='instances_modified', on_delete=models.SET_NULL, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this book across the entire library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200, blank=True, null=True, help_text='The publisher\'s trade name.')
    due_date = models.DateField(null=True, blank=True, db_index=True, help_text='The date this book is due back (if checked out).')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True, related_name='books')

    LOAN_STATUS = (
      ('m', 'Maintenance'),
      ('o', 'On Loan'),
      ('a', 'Available'),
      ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, null=True, default='m',help_text='Book availability')

    class Meta:
      ordering = ['due_date', ]

    def __str__(self):
       """
       String representing specific book instance.
       """
       return f'{self.id} - {self.book.title}'

class Author(models.Model):
    """
    Model representing an author
    """
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('auth.User', related_name='authors_created', on_delete=models.SET_NULL, null=True)
    modified_by = models.ForeignKey('auth.User', related_name='authors_modified', on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True, help_text='The first name of the author.')
    last_name = models.CharField(max_length=100, blank=True, db_index=True, null=True, help_text='The last name of the author.')
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    slug = models.SlugField(max_length=50, db_index=True)

    class Meta:
      ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
       """
       Return the url to access this particular author instance.
       """
       return reverse('catalog:author-detail', kwargs={'id': str(self.id), 'slug': self.slug})

    def __str__(self):
       """
       String representing the author object
       """
       return f'{self.last_name}, {self.first_name}'

    def save(self):
      if not self.slug:
        self.slug = f'{self.first_name}-{self.last_name}'
      super(Author, self).save()


class Language(models.Model):
    """
    A model to define the languages a book instance may be written in.
    """
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('auth.User', related_name='languages_created', on_delete=models.SET_NULL, null=True)
    modified_by = models.ForeignKey('auth.User', related_name='languages_modified', on_delete=models.SET_NULL, null=True)
    language = models.CharField(max_length=100, blank=True, null=True, help_text='A human language a particular book isntances is written in.')

    def __str__(self):
       """
       String representing the language
       """
       return self.language

    def get_absolute_url(self):
      return reverse('catalog:language-detail', kwargs={'pk': str(self.id), 'language': self.language})
