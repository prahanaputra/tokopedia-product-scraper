import requests
from bs4 import BeautifulSoup
import pandas as pd



headers = {'User-Agent': 'Mozilla/5.0'}

# url = "https://www.tokopedia.com/benihdramaga/benih-bunga-matahari-ipb-bm1"



df = pd.read_excel('tokopedia_urls.xlsx') # Get all the urls from the excel
mylist = df['url'].tolist() #urls is the column name
scraped_data = []

for url in mylist:
    r = requests.get(url, headers=headers)
    soup_1 = BeautifulSoup(r.text, 'html.parser')
    soup_2 = BeautifulSoup(r.text, 'lxml')
    
    try:
        description = soup_1.find('div', attrs={'data-testid': 'lblPDPDescriptionProduk'}).text
        # description = str(description).replace("<br/>", "\n")
        # description = str(description).replace("</div>", "")
        # description = str(description).replace('<div data-testid="lblPDPDescriptionProduk">', "")
        # print(description)
    except:

        print('no description')

    try:
        image = soup_1.find('img', attrs={'data-testid': 'PDPMainImage'})['src']
        # print(image['src'])
    except:
        print('no image')

    scraped_data.append([description, image])

# for i in scraped_data:
#     print(i)
#     print('\n')

df = pd.DataFrame(scraped_data, columns=["description","image_url"])
df.to_excel('tokopedia_description.xlsx', index=False)
