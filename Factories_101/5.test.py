from test_plus import TestCase

from my_library.seed.factories import (
    UserFactory,
    BookFactory,
    LibraryFactory,
    BookBorrowFactory,
)


class BookBorrowListViewTests(TestCase):
    def setUp(self):
        self.librarian = UserFactory(is_superuser=True)
        self.library = LibraryFactory(librarian=self.librarian)
        self.user = UserFactory()
        self.url = self.reverse('library:book_borrow_list',
                                user_id=self.user.id)

    def test_with_several_books_borrowed_by_one_user(self):
        books = BookFactory.create_batch(5, library=self.library)

        for book in books:
            BookBorrowFactory(user=self.user, book=book)

        response = self.get(self.url)

        self.assertEqual(200, response.status_code)
        for book in books:
            self.assertContains(response, book.title)

    def test_with_several_books_borrowed_by_one_user_and_another_user(self):
        another_user = UserFactory()

        user1_books = BookFactory.create_batch(5, library=self.library)
        user2_books = BookFactory.create_batch(5, library=self.library)

        for book in user1_books:
            BookBorrowFactory(user=self.user, book=book)

        for book in user2_books:
            BookBorrowFactory(user=another_user, book=book)

        response = self.get(self.url)

        self.assertEqual(200, response.status_code)
        for book in user1_books:
            self.assertContains(response, book.title)
        for book in user2_books:
            self.assertNotContains(response, book.title)