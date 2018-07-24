from django.contrib import admin
from catalog.models import Author, Book, BookInstance, Genre, Language


class BookInstanceInline(admin.TabularInline):
  model = BookInstance
  fields = ('language', 'status', 'due_date')
  extra = 0

class BookInline(admin.TabularInline):
  model = Book
  extra = 0

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
  list_display =('last_name', 'first_name', 'date_of_birth', 'date_of_death')
  prepopulated_fields = {'slug': ('first_name', 'last_name')}
  excluded_fields = None


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
  list_display = ('title', 'display_author', 'display_genre')
  prepopulated_fields = {'slug': ('title', )}
  excluded_fields = None
  inlines = [BookInstanceInline, ]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
  list_display = ('book', 'status', 'due_date', 'language')
  excluded_fields = None
  fieldsets = (
    (None, {
      'fields': ('book', 'imprint', 'id')
    }),
    ('Availability', {
      'fields': ('status', 'due_date', 'borrower')
    }),
  )

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
  excluded_fields = None

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
  excluded_fields = None
