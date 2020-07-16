from bs4 import BeautifulSoup as Soup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os, shutil
import urllib.request as libreq
import xlsxwriter as xl

CHROME_PATH = "C:/Users/Ricky/Desktop/chromedriver_win32/chromedriver.exe"
CWD_FULL_PATH = "C:/Users/Ricky/source/repos/Webscraper/dogWebscraper/Webscraper"
FOLDER = "./images"
EXCEL_FILE = "available_dogs.xlsx"

NAMES = []
LINKS = []
IMAGES = []


def createExcel():
    
    # Delete the old excel file if it exists
    if os.path.exists(EXCEL_FILE):
        os.remove(EXCEL_FILE)

    # Create a new Excel file and add a worksheet in current directory
    workbook = xl.Workbook("available_dogs.xlsx")
    worksheet = workbook.add_worksheet()

    # Modify cell width/height and links/text formatting
    link_format = workbook.add_format({"color": "blue",
                                       "underline": True,
                                       "text_wrap": True,})

    text_format = workbook.add_format({"text_wrap": True})
    worksheet.set_column(0, 2, 25)
    worksheet.set_default_row(85, hide_unused_rows=True)

    #Insert information into worksheet
    for i in range(len((IMAGES))):
        worksheet.write(i, 0, NAMES[i], text_format)
        worksheet.write(i, 1, LINKS[i], link_format)
        worksheet.insert_image(i, 2, IMAGES[i], {"x_scale": 0.25, "y_scale":0.25})

    workbook.close()


def scrapeInfo(url):
    # Run Chrome without GUI by running in headless mode
    options = Options()
    options.headless = True
    options.add_argument('--log-level=3')   # Suppress error messages (non-fatal)

    # Create the driver to access url
    driver = webdriver.Chrome(options=options, executable_path=CHROME_PATH)
    driver.get(url)

    # Retrieve the url's HTML 
    html_source = driver.execute_script("return document.documentElement.outerHTML")

    # Create the BeautifulSoup data type, with the 'lxml' parser and find all available dog's info  
    soup = Soup(html_source, 'lxml')
    available_dogs = soup.find_all('div', class_="userContent__item")

    # Delete the old folder and its contents if it exists, then create a new folder to save the latest image files
    if os.path.exists(FOLDER):
        shutil.rmtree(FOLDER)
        
    os.mkdir(FOLDER)

    for dog in available_dogs:
        dog_name = dog.div.div.div.text
        profile_link = dog.a['href']
        img_src = dog.div.span.span.img['src']

        # Retrieve the img from the img_src link and save the image file
        img_path = FOLDER + "/" + dog_name + ".jpg"
        libreq.urlretrieve(img_src, img_path)

        NAMES.append(dog_name)
        LINKS.append(profile_link)
        IMAGES.append(img_path)


def main():
    scrapeInfo("https://www.sfspca.org/adoptions/dogs/?")
    createExcel();

#===============================================================================================================#

if __name__ == "__main__":
    main()

