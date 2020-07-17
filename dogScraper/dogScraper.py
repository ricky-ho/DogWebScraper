from bs4 import BeautifulSoup as Soup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os, shutil
import urllib.request as libreq
import xlsxwriter as xl

GEKKO_PATH = r"C:\Users\Ricky\geckodriver.exe"
IMAGE_FOLDER = "./images"
EXCEL_FILE = "available_dogs.xlsx"
URLs = ["https://www.sfspca.org/adoptions/dogs/?", "https://phs-spca.org/adopt/dogs/"]

NAMES = []
LINKS = []
IMG_FILE_PATHS = []


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
    worksheet.set_default_row(100, hide_unused_rows=True)

    #Insert information into worksheet
    for i in range(len((IMG_FILE_PATHS))):
        worksheet.write(i, 0, NAMES[i], text_format)
        worksheet.write(i, 1, LINKS[i], link_format)
        worksheet.insert_image(i, 2, IMG_FILE_PATHS[i], {"x_scale": 0.25, "y_scale":0.25})

    workbook.close()


def scrape_SFSPCA(html):

    # Create the BeautifulSoup data type, with the 'lxml' parser and find all available dog's info  
    soup = Soup(html, 'lxml')
    available_dogs = soup.find_all('div', class_="userContent__item")

    for dog in available_dogs:
        dog_name = dog.div.div.div.text
        profile_link = dog.a['href']
        img_src = dog.div.span.span.img['src']

        # Retrieve the img from the img_src link and save the image file in img_path
        img_path = IMAGE_FOLDER + "/" + dog_name + ".jpg"
        try:
            libreq.urlretrieve(img_src, img_path)
        except Exception as e:
            # If there is an error accessing the image, skip the image and continue
            print("Error from urlretrieve({}: {}".format(img_src, e))
            continue
            
        IMG_FILE_PATHS.append(img_path)
        NAMES.append(dog_name)
        LINKS.append(profile_link)


def scrape_PHSSPCA(html):

    # Create the BeautifulSoup data type, with the 'lxml' parser and find all available dog's info  
    soup = Soup(html, 'lxml')
    available_dogs = soup.find_all('td', class_='rgtkSearchResultsCell')
    
    i = 1;  # i is an index used in searching for each id tag
    for dog in available_dogs:
        id = "{}{}".format('rgtkSearchPetInfoAnimalName', str(i))
        dog_name = dog.find('div', id=id).a.text
        profile_link = URLs[1]
        img_src = dog.div.a.img['src']
        i += 1

        # Retrieve the img from the img_src link and save the image file in img_path
        img_path = IMAGE_FOLDER + "/" + dog_name + ".jpg"
        try:
            libreq.urlretrieve(img_src, img_path)
        except Exception as e:
            # If there is an error accessing the image, skip the image and continue
            print("Error from urlretrieve({}: {}".format(img_src, e))
            continue

        IMG_FILE_PATHS.append(img_path)
        NAMES.append(dog_name)
        LINKS.append(profile_link)
        

def getHTML(driver, url):
    driver.get(url)
    html = driver.execute_script("return document.documentElement.outerHTML")
    return html


def main():

    # Run Firefox without GUI by running in headless mode and suppress non-fatal error messages
    options = Options()
    options.headless = True
    options.add_argument('--log-level=3')   # Suppress error messages (non-fatal)

    # Create the Firefox driver to be used to access the websites
    driver = webdriver.Firefox(options=options, executable_path=GEKKO_PATH)

    # Delete the old images folder and its contents if it exists, then create a new one to save the latest image files
    if os.path.exists(IMAGE_FOLDER):
        shutil.rmtree(IMAGE_FOLDER)
    os.mkdir(IMAGE_FOLDER)

    # Retrieve each url's HTML source code and call the corresponding function to scrape
    for i in range(len(URLs)):
        html_source = getHTML(driver, URLs[i])
        if i == 0:
            scrape_SFSPCA(html_source)
            print("Finished scraping from SF-SPCA")
        else:
            scrape_PHSSPCA(html_source)
            print("Finished scraping from PHS-SPCA")

    driver.quit()

    # Create the excel spreadsheet using all of the scraped info
    createExcel();

#===============================================================================================================#

if __name__ == "__main__":
    main()

