import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException



# Set up Firefox options
firefox_options = Options()
firefox_options.headless = True  # Run the browser in headless mode

# Set up the Firefox driver
driver = webdriver.Firefox()

# Open the webpage
driver.get("https://www.tokopedia.com/benihdramaga/benih-bunga-matahari-ipb-bm1")



# Wait for the "Lihat Pilihan Kurir" button to appear and click it
try:
    wait = WebDriverWait(driver, 10)
    kurir_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Lihat Pilihan Kurir"]')))
    kurir_button.click()
except NoSuchElementException:
    print ('error')    

# Wait for the product weight to appear and extract it
try:
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.weight-value')))
    weight_element = driver.find_element(By.CSS_SELECTOR, 'div.weight-value')
    product_weight = weight_element.text
except NoSuchElementException:
    print ('error')

try:
    wait = WebDriverWait(driver, 10)
    description = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-testid="lblPDPDescriptionProduk"]')))
    description_text = description.text
except NoSuchElementException:
    print ('error')

# Print the product weight
print("Product Weight:", product_weight)
print(description_text)
# Close the browser
driver.quit()