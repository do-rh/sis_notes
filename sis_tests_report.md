### Report Objectives
* Overview of testing strategy
* Current test coverage / status
* Go over Django specific testing
    * factories
    * faker data
    * selenium
    * coverage
* Teach team how to run tests

**Core Tests**
* admin
* models
* views
* api

# Testing in SIS

**Overview**
* 562 tests
* coverage tbd
* Before PR submission, always run coverage of new code 

**Testing Strategy**

*Backend*
* Django's built in testing infrastructure
* Target: 100% coverage
* All directories containing Python code should have an `__init__.py` file so that they are considered under our coverage system.
* Factories???
* M-M relationships (enrollment & staffing), need to manually create enrollment and staffing factory instances that set the relationships
* fun fact: factory boy was chosen because in Rails they chose factory girl :) 

*Frontend*
* Selenium for functional tests for assessment submissions by students and the welcome form for new students.
* Rely on backend testing for HTML tests

**Coverage.py**
* coverage.py module provides a coverage report, similar to jest.
* module is already in the package and installed
* within project/ run command: `coverage run --source='.' manage.py test`
* `coverage html` - makes directory of htmlcov with html reports of all individual test groups. index.html shows all cases and can nav through
* `coverage report`

**Testing Commands**
* All: `python manage.py test --keepdb --settings=sis.settings.testing`
* App: `python manage.py test --keepdb --settings=sis.settings.testing <APP_NAME>`
    * ex: <APP_NAME> = staff students
* Files or Test Functions:
```
  python manage.py test --keepdb --settings=sis.settings.testing \
    students.tests.test_models \
    students.tests.test_models.StudentModelTestCase \
    students.tests.test_models.StudentModelTestCase.test_student_url
```
* PDB access via command line: `python manage.py test --keepdb --settings=sis.settings.testing --pdb`
* breakpoint inserted where test fails, use up key to nav through the code frames.

## Backend Testing
* Django apps use model template view structure
    - models = data access layer to handle data
    - template = presentation layer to handle UI
    - view = exectues business logic and interacts with model to carry data and render the template
* To test, need to create some model instances and work with a database
* Create fake data for tests
    * Factories - factory_boy - py package that creates factories of models
    * Fakers - fakers - py package that creates fake data
* Enables auto-generation of unique random strings / numbers
* Enables for unique instances of models that don't duplicate
* Ex. Instead of testing only with 1 user and coming up with 1 name, can test 10000s of users.

**Faker**
```python
book1 = Book.objects.create(
    library=self.library,
    title='Test Title 1',
    description='asdf'
)
```
*with faker:*
```python
from faker import Factory
import factory

faker = Factory.create()

book1 = Book.objects.create(
    library=self.library,
    title=faker.word(),
    description=faker.text()
)
```
basic methods:
* faker.random_number()
* faker.word()
* faker.text()

other cool stuff to look into @ https://faker.readthedocs.io/en/master/providers.html:
* providers: `faker.providers`

**Fuzzy** 

* alternative to faker, generates random values. older version, now factory_boy has factory.Faker class.

**Factories**
* Django's way of boxing up all the data you need to test something
* Factories generate a whole ecosystem of objects that are already related to each other. ex. in order to test assessments, you need a student who's in a chohort
* Python classes that behave similarly to Django models – they write to your database as Django models do.
* TODO: figure out what cases to create factories - so far it looks like each model has a factory. 

```python
import factory

class UserFactory(factory.django.DjangoModelFactory):
    """Factory class that helps create test users."""

    class Meta:
        model = 'users.User'
        django_get_or_create = ('username',)

    date_joined = make_aware(datetime(2020, 1, 1))
    first_name = 'Jane'
    last_name = 'Smith'
    ...
    course = factory.SubFactory(CourseFactory)

```

* `factory.django.DjangoModelFactory` - dedicated class for Django `Model` factories.
* Use for initializing a factory class for your model
    * `model` attribute
    * `create()` = `Model.objects.create()`
    * `class Meta` section specifies the model you want to factory-ize, and the additional option to use `django_get_or_create` for specified fields instead of create.
    * `django_get_or_create` will first try and get the data from the model when a field is passed in, otherwise will create a new instance. This way, it won't throw an error if it doesn't exist in the db OR avoid any clashes of unique fields.
    * related data should be assigned to another factory class via `factory.SubFactory(FACTORY_NAME)`
    * 

## Testing using Factories

* create_batch - `books = BookFactory.create_batch(5, library=self.library)`
* for loop through book in books.

```python
from django.test import TestCase
from staff.factories import StaffMemberFactory
from students.factories import StudentFactory

class APICourseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cohort = CohortFactory(course__dri=StaffMemberFactory())
        cls.cohort_2 = CohortFactory(id="r100")
        cls.student = StudentFactory()

    def test_auth_req(self):
        response = self.client.get("/api/cohorts/")
        self.assertEqual(response.status_code, 401)
    ...
```

**Common Tools**
`from factory import LazyAttribute as Lazy, fuzzy`
* Lazy - Most factory attributes can be added using static values that are `evaluated when the factory is defined`, but some attributes (such as fields whose value is computed from other elements) will `need values assigned each time an instance is generated`. expects function as an argument. It’s convenient to use lambda here

* fuzzy

**useful methods**
* self.client.force_login -> logs in given an instance of a user

### Sources
1) fakes & factories https://www.hacksoft.io/blog/improve-your-tests-django-fakes-and-factories

## Test Types

| ID | Folder      | admin | api | models| views | other                                        |
|----|-------------|-------|-----|-------|-------|----------------------------------------------|
| 3  | assets      | x     | x   | x     |  x    |                                              |
| 8  | events      | x     | x   | x     |  x    |                                              |
| 9  | exercises   | x     | x   | x     |  x    |                                              |
| 10 | lectures    | x     | x   | x     |  x    |                                              |
| 11 | projects    | x     | x   | x     |  x    |                                              |
| 14 | staff       | x     | x   | x     |  x    |                                              |
| 2  | assessments | x     | x   | x     |  x    |download_zip, email                           | 
| 7  | courses     | x     | x   | x     |  x    |clone, cohortitems, manage, publishweegroup   |
| 15 | students    | x     | x   | x     |  x    |import_from_csv                               |
| 16 | users       | x     |     | x     |  x    |auth, mail,                                   |
| 6  | core        | x     |     |       |       |dbutils, fake_dev_db, templatetags            |
| 1  | api         |       |     |       |  x    |                                              | 
| 4  | calendars   |       |     |       |  x    |                                              |
| 12 | sis         |       |     |       |  x    |middleware, response_debug, s3, settings, wsgi|
1) faker documentation: https://faker.readthedocs.io/en/master/providers.html
