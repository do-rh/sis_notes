# in factories.py

import factory
from faker import Factory

from my_library.users.models import User
from my_library.library.models import (
    Book,
    Library,
    BookBorrow,
)


faker = Factory.create()


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    name = faker.name()
    email = faker.email()


class LibraryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Library

    address = faker.street_address()
    librarian = factory.SubFactory(UserFactory)


class BookFactory(factory.DjangoModelFactory):
    class Meta:
        model = Book

    library = factory.SubFactory(LibraryFactory)
    title = faker.word()
    description = faker.text()


class BookBorrowFactory(factory.DjangoModelFactory):
    class Meta:
        model = BookBorrow

    book = factory.SubFactory(BookFactory)
    user = factory.SubFactory(UserFactory)
    charge = faker.random_number()