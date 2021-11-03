from test_plus import TestCase
from faker import Factory

from my_library.users.models import User
from my_library.library.models import Book, BookBorrow, Library


faker = Factory.create()


class BookBorrowListViewTests(TestCase):
    def setUp(self):
        self.librarian = User.objects.create(name=faker.name(),
                                             email=faker.email(),
                                             is_superuser=True)
        self.library = Library.objects.create(address=faker.street_address(),
                                              librarian=self.librarian)
        self.user = User.objects.create(name=faker.name(), email=faker.email())
        self.url = self.reverse('library:book_borrow_list',
                                user_id=self.user.id)

    def test_with_several_books_borrowed_by_one_user(self):
        book1 = Book.objects.create(
            library=self.library,
            title=faker.word(),
            description=faker.text()
        )
        book2 = Book.objects.create(
            library=self.library,
            title=faker.word(),
            description=faker.text()
        )
        book3 = Book.objects.create(
            library=self.library,
            title=faker.word(),
            description=faker.text()
        )
        book4 = Book.objects.create(
            library=self.library,
            title=faker.word(),
            description=faker.text()
        )
        book5 = Book.objects.create(
            library=self.library,
            title=faker.word(),
            description=faker.text()
        )

        BookBorrow.objects.create(user=self.user, book=book1, charge=faker.random_number())
        BookBorrow.objects.create(user=self.user, book=book2, charge=faker.random_number())
        BookBorrow.objects.create(user=self.user, book=book3, charge=faker.random_number())
        BookBorrow.objects.create(user=self.user, book=book4, charge=faker.random_number())
        BookBorrow.objects.create(user=self.user, book=book5, charge=faker.random_number())

        response = self.get(self.url)

        self.assertEqual(200, response.status_code)
        self.assertContains(response, book1.title)
        self.assertContains(response, book2.title)
        self.assertContains(response, book3.title)
        self.assertContains(response, book4.title)
        self.assertContains(response, book5.title)

    def test_with_several_books_borrowed_by_one_user_and_another_user(self):
        another_user = User.objects.create(name=faker.name(), email=faker.email())

        user1_book1 = Book.objects.create(
            library=self.library,
            title=faker.word(),
            description=faker.text()
        )
        user1_book2 = Book.objects.create(
            library=self.library,
            title=faker.word(),
            description=faker.text()
        )
        user1_book3 = Book.objects.create(
            library=self.library,
            title=faker.word(),
            description=faker.text()
        )
        user1_book4 = Book.objects.create(
            library=self.library,
            title=faker.word(),
            description=faker.text()
        )
        user1_book5 = Book.objects.create(
            library=self.library,
            title=faker.word(),
            description=faker.text()
        )

        user2_book1 = Book.objects.create(
            library=self.library,
            title=faker.word(),
            description=faker.text()
        )
        user2_book2 = Book.objects.create(
            library=self.library,
            title=faker.word(),
            description=faker.text()
        )
        user2_book3 = Book.objects.create(
            library=self.library,
            title=faker.word(),
            description=faker.text()
        )
        user2_book4 = Book.objects.create(
            library=self.library,
            title=faker.word(),
            description=faker.text()
        )
        user2_book5 = Book.objects.create(
            library=self.library,
            title=faker.word(),
            description=faker.text()
        )

        BookBorrow.objects.create(user=self.user, book=user1_book1, charge=faker.random_number())
        BookBorrow.objects.create(user=self.user, book=user1_book2, charge=faker.random_number())
        BookBorrow.objects.create(user=self.user, book=user1_book3, charge=faker.random_number())
        BookBorrow.objects.create(user=self.user, book=user1_book4, charge=faker.random_number())
        BookBorrow.objects.create(user=self.user, book=user1_book5, charge=faker.random_number())

        BookBorrow.objects.create(user=another_user, book=user2_book1, charge=faker.random_number())
        BookBorrow.objects.create(user=another_user, book=user2_book2, charge=faker.random_number())
        BookBorrow.objects.create(user=another_user, book=user2_book3, charge=faker.random_number())
        BookBorrow.objects.create(user=another_user, book=user2_book4, charge=faker.random_number())
        BookBorrow.objects.create(user=another_user, book=user2_book5, charge=faker.random_number())

        response = self.get(self.url)

        self.assertEqual(200, response.status_code)
        self.assertContains(response, user1_book1.title)
        self.assertContains(response, user1_book2.title)
        self.assertContains(response, user1_book3.title)
        self.assertContains(response, user1_book4.title)
        self.assertContains(response, user1_book5.title)

        self.assertNotContains(response, user2_book1.title)
        self.assertNotContains(response, user2_book2.title)
        self.assertNotContains(response, user2_book3.title)
        self.assertNotContains(response, user2_book4.title)
        self.assertNotContains(response, user2_book5.title)