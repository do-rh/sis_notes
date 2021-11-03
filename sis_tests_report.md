### Report Objectives
* Overview of testing strategy
* Current test coverage / status
* Go over Django specific testing
    * factories
    * faker data
    * selenium
    * coverage
* Teach team how to run tests

# Testing in SIS

**Overview**
* 562 tests
* coverage tbd
* Before PR submission, always run coverage of new code 
**Testing Strategy**

*Backend*
* Django's built in testing infrastructure
* Target: 100% coverage
* All directories containing Python code should have an ``__init__.py`` file so that they are considered under our coverage system.
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
* within 

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

* Factory Boy:
    As a fixtures replacement tool, it aims to replace static, hard to maintain 
    fixtures with easy-to-use factories for complex objects.

    Instead of building an exhaustive test setup with every possible combination 
    of corner cases, factory_boy allows you to use objects customized for the 
    current test, while only declaring the test-specific fields:

* Lazy Attribute: 
    Most factory attributes can be added using static values that are evaluated when the factory is defined, but some attributes (such as fields whose value is computed from other elements) will need values assigned each time an instance is generated. Use lazy to facilitate this.

```python
book1 = Book.objects.create(
    library=self.library,
    title='Test Title 1',
    description='asdf'
)
```
*with faker:*
```python
book1 = Book.objects.create(
    library=self.library,
    title=faker.word(),
    description=faker.text()
)
```
* faker.random_number()
* faker.word()
* faker.text()

**Factories**
* Django's mocking system

### Sources
1) fakes & factories https://www.hacksoft.io/blog/improve-your-tests-django-fakes-and-factories