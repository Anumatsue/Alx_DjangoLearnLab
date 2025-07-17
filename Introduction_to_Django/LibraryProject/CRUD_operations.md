
Create.md
python
from bookshelf.models import Book

book = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949
)
book
# <Book: 1984 by George Orwell (1949)>

Retrieve.md
python
from bookshelf.models import Book

book = Book.objects.get(id=book.id)
book.title
# '1984'
book.author
# 'George Orwell'
book.publication_year
# 1949

Update.md
book.title = "Nineteen Eighty-Four"
book.save()
book.title
# 'Nineteen Eighty-Four'

Delete.md
python
from bookshelf.models import Book

book = Book.objects.get(id=book.id)
book.delete()
Book.objects.all()
# <QuerySet []>