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
        book1 = BookFactory(library=self.library)
        book2 = BookFactory(library=self.library)
        book3 = BookFactory(library=self.library)
        book4 = BookFactory(library=self.library)
        book5 = BookFactory(library=self.library)

        BookBorrowFactory(user=self.user, book=book1)
        BookBorrowFactory(user=self.user, book=book2)
        BookBorrowFactory(user=self.user, book=book3)
        BookBorrowFactory(user=self.user, book=book4)
        BookBorrowFactory(user=self.user, book=book5)

        response = self.get(self.url)

        self.assertEqual(200, response.status_code)
        self.assertContains(response, book1.title)
        self.assertContains(response, book2.title)
        self.assertContains(response, book3.title)
        self.assertContains(response, book4.title)
        self.assertContains(response, book5.title)

    def test_with_several_books_borrowed_by_one_user_and_another_user(self):
        another_user = UserFactory()

        user1_book1 = BookFactory(library=self.library)
        user1_book2 = BookFactory(library=self.library)
        user1_book3 = BookFactory(library=self.library)
        user1_book4 = BookFactory(library=self.library)
        user1_book5 = BookFactory(library=self.library)

        user2_book1 = BookFactory(library=self.library)
        user2_book2 = BookFactory(library=self.library)
        user2_book3 = BookFactory(library=self.library)
        user2_book4 = BookFactory(library=self.library)
        user2_book5 = BookFactory(library=self.library)

        BookBorrowFactory(user=self.user, book=user1_book1)
        BookBorrowFactory(user=self.user, book=user1_book2)
        BookBorrowFactory(user=self.user, book=user1_book3)
        BookBorrowFactory(user=self.user, book=user1_book4)
        BookBorrowFactory(user=self.user, book=user1_book5)

        BookBorrowFactory(user=another_user, book=user2_book1)
        BookBorrowFactory(user=another_user, book=user2_book2)
        BookBorrowFactory(user=another_user, book=user2_book3)
        BookBorrowFactory(user=another_user, book=user2_book4)
        BookBorrowFactory(user=another_user, book=user2_book5)

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