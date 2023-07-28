import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException


# Set up Chrome options
# chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run the browser in background
# chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument("disable-quic")
options.add_argument('--ignore-certificate-errors-spki-lists')

# caps = webdriver.DesiredCapabilities.CHROME.copy()
# caps['acceptInsecureCerts'] = True

webdriver_service = Service("C:\Chrome\chromedriver.exe")
driver = webdriver.Chrome(service=webdriver_service, options=options)
driver.get("https://www.tokopedia.com/benihdramaga/benih-bunga-matahari-ipb-bm1")



# Wait for the "Lihat Pilihan Kurir" button to appear and click it
try:
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="pdp_comp-shipment"]')))
    driver.find_element((By.XPATH, '//*[@id="pdp_comp-shipment"]')).click()
except NoSuchElementException:
    print ('error')    

# Wait for the product weight to appear and extract it
try:
    wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="mud-alert-message"]')))
    weight_element = driver.find_element(By.XPATH, '//div[@class="mud-alert-message"]')
    product_weight = weight_element.text
except NoSuchElementException:
    print ('error')

# Print the product weight
print("Product Weight:", product_weight)

# Close the browser
driver.quit()