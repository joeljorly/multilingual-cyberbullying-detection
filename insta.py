from selenium import webdriver
import time
import sys                                ##Insta scrapping-https://github.com/AgiMaulana/Instagram-Comments-Scraper
import requests                           ##By- AgiMaulana
import logging

logging.basicConfig(filename="logs/scrap.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w') 
logger=logging.getLogger() 
logger.setLevel(logging.DEBUG)

driver = webdriver.Chrome()
#post url
driver.get('https://www.instagram.com/p/B9wvgT6pvrC/?igshid=9whhvyiaqxkb')
time.sleep(3)
class ig_scrap():
  def __init__(self):

    self.scrap()

  def scrap(self):
    get_url = driver.current_url 
    print(get_url)
    #if user not logined
    try:
        close_button = driver.find_element_by_class_name('xqRnw')
        close_button.click()
    except:
        logging.error('Selenium could not start')
        pass
    logging.info('scrapping started')

    ## Iterate through the comments
    try:
        load_more_comment = driver.find_element_by_css_selector('.MGdpg > button:nth-child(1)') #css element
        print("Found {}".format(str(load_more_comment)))
        i = 0
        while load_more_comment.is_displayed() and i < int(sys.argv[1]):
            load_more_comment.click()
            time.sleep(1.5)
            load_more_comment = driver.find_element_by_css_selector('.MGdpg > button:nth-child(1)')
            print("Found {}".format(str(load_more_comment)))
            i += 1
    except Exception as e:
        print(e)
        pass

    user_names = []
    user_comments = []
    comment = driver.find_elements_by_class_name('gElp9 ')
    for c in comment:
        container = c.find_element_by_class_name('C4VMK')
        name = container.find_element_by_class_name('_6lAjh').text 
        content = container.find_element_by_tag_name('span').text  #get contents from span class
        content = content.replace('\n', ' ').strip().rstrip()
        user_names.append(name)
        user_comments.append(content)
    user_names.pop(0)
    user_comments.pop(0)
    import excel_exporter
    excel_exporter.export(user_comments)

    driver.close()

ig_scrap()