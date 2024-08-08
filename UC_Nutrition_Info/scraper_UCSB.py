import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument('--disable-gpu')

service = Service('/usr/local/bin/chromedriver')
driver = webdriver.Chrome(service = service, options = chrome_options)

def scrape_UCSB():
  try:
    driver.get('https://nutrition.info.dining.ucsb.edu/NetNutrition/1#')

    data =[]
    print('here')
    wait = WebDriverWait(driver, 10)

    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

    item1 = driver.find_element(By.LINK_TEXT, 'Take Out at Ortega Commons').click()

    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

    time.sleep(2)
    print('Clicked\n')

    item2 = driver.find_element(By.LINK_TEXT, "Ortega's Daily Menu").click()

    time.sleep(2)
    print('Clicked\n')

    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

    items = driver.find_elements(By.CSS_SELECTOR, '.cbo_nn_itemHover')

    for item in items:
      item.click()
      time.sleep(1)
      
      try:
        #Food Name, Calories, Total Fat, and, Protein
        food_name = driver.find_element(By.CSS_SELECTOR, '.cbo_nn_LabelHeader')
        calories = driver.find_element(By.CSS_SELECTOR, 'div.inline-div-right.bold-text.font-22' )
        total_fat = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Total Fat']")))
        total_fat_data = total_fat.find_element(By.XPATH, "./following-sibling::span")
        protein = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text() = 'Protein']")))
        protein_data = protein.find_element(By.XPATH, "./following-sibling::span")

        data.append({'Food Name': food_name.text, 'Calories': calories.text, 'Total Fat': total_fat_data.text.strip(), 'Protein': protein_data.text.strip()})
        print('Food Name: ' + food_name.text + ' was scraped\n')

      except NoSuchElementException:
        print('Nutritional information not found for this product.')
    
      wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#btn_nn_nutrition_close'))).click()
      print('Back\n')

  except NoSuchElementException:
    print('Nutritional information not found for this product.')

  finally:
    driver.quit()

  return data

print(scrape_UCSB())
  

