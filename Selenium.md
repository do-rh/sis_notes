https://www.ordinarycoders.com/blog/article/testing-django-selenium
## What is Selenium:
Selenium is a framework for testing web applications and automating web 
browsers. Selenium actually automates user interaction on a given website as 
if a real user is performing the actions. 

## Execution Steps
1. pip install selenium
2. Download Chrome Driver 
(https://sites.google.com/a/chromium.org/chromedriver/)
3. Add driver to executable path
(https://zwbetz.com/download-chromedriver-binary-and-add-to-your-path-for-automated-functional-testing/)
4. Build test.py like below:

```py
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Create your tests here.
class PlayerFormTest(LiveServerTestCase):

  def testform(self):
    selenium = webdriver.Chrome()
    #Choose your url to visit
    selenium.get('http://127.0.0.1:8000/')
    #find the elements you need to submit form
    player_name = selenium.find_element_by_id('id_name')
    player_height = selenium.find_element_by_id('id_height')
    player_team = selenium.find_element_by_id('id_team')
    player_ppg = selenium.find_element_by_id('id_ppg')

    submit = selenium.find_element_by_id('submit_button')

    #populate the form with data
    player_name.send_keys('Lebron James')
    player_team.send_keys('Los Angeles Lakers')
    player_height.send_keys('6 feet 9 inches')
    player_ppg.send_keys('25.7')

    #submit form
    submit.send_keys(Keys.RETURN)

    #check result; page source looks at entire html document
    assert 'Lebron James' in selenium.page_source
```
5. run test with `python manage.py test`