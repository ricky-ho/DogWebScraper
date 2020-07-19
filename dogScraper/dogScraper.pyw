from bs4 import BeautifulSoup as Soup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os, shutil
import urllib.request as libreq
import xlsxwriter as xl
import smtplib, yaml
from email.message import EmailMessage
from time import strftime, localtime


GEKKO_PATH = r'C:\Users\Ricky\geckodriver.exe'
IMAGE_FOLDER = './images'
EXCEL_FILE = 'available_dogs.xlsx'
URLs = ['https://www.sfspca.org/adoptions/dogs/?', 'https://phs-spca.org/adopt/dogs/']

NAMES = []
LINKS = []
IMG_FILE_PATHS = []


def sendEmail():
    
    # Retrieve the login information from a .yml file 
    USER, PWD = get_login_info()

    # Configure email and generate email content
    msg = EmailMessage()
    msg['From'] = USER
    msg['To'] = 'horicky2016@gmail.com'
    msg['Subject'] = 'Available dogs from sfspca.org & phs-spca.org'
    date = strftime('%m/%d/%Y %H:%M', localtime())
    msg.set_content('Information up-to-date as of: ' + date)

    # Add the excel file as an attachment to the email
    try: 
        with open(EXCEL_FILE, 'rb') as f:
            file_data = f.read()
        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=EXCEL_FILE)

    except Exception as e:
        print("Error creating attachment: {}".format(e))
        del msg
    
    # Send the email over a secure connection using SMTP server
    try:
        with smtplib.SMTP_SSL(host='smtp.gmail.com', port=465) as server:
            server.login(USER, PWD)
            server.send_message(msg)
            print("Email sent")

    except Exception as e:
        print('Error sending email: {}'.format(e))
        del msg


def get_login_info():

    with open('login.yml', 'r') as f:
        yml_file = yaml.load(f, Loader=yaml.BaseLoader)
        email = yml_file['User']['email']
        pwd = yml_file['User']['password']

        return (email, pwd)


def createExcel():
    
    # Delete the old excel file if it exists
    if os.path.exists(EXCEL_FILE):
        os.remove(EXCEL_FILE)

    # Create a new Excel file and add a worksheet in current directory
    workbook = xl.Workbook('available_dogs.xlsx')
    worksheet = workbook.add_worksheet()

    # Modify cell width/height and links/text formatting
    link_format = workbook.add_format({'color': 'blue',
                                       'underline': True,
                                       'text_wrap': True,})

    text_format = workbook.add_format({'text_wrap': True})
    worksheet.set_column(0, 2, 20)
    worksheet.set_default_row(80, hide_unused_rows=True)

    #Insert information into worksheet
    for i in range(len((IMG_FILE_PATHS))):
        worksheet.write(i, 0, NAMES[i], text_format)
        worksheet.write(i, 1, LINKS[i], link_format)
        worksheet.insert_image(i, 2, IMG_FILE_PATHS[i], {'x_scale': 0.18, 'y_scale':0.18})

    workbook.close()


def scrape_SFSPCA(html):

    # Create the BeautifulSoup data type, with the 'lxml' parser and find all available dog's info  
    soup = Soup(html, 'lxml')
    available_dogs = soup.find_all('div', class_='userContent__item')

    for dog in available_dogs:
        dog_name = dog.div.div.div.text
        profile_link = dog.a['href']
        img_src = dog.div.span.span.img['src']

        # Retrieve the img from the img_src link and save the image file in img_path
        img_path = IMAGE_FOLDER + '/' + dog_name + '.jpg'
        try:
            libreq.urlretrieve(img_src, img_path)
        except Exception as e:
            # If there is an error accessing the image, skip the image and continue
            print('Error from urlretrieve({}: {}'.format(img_src, e))
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
        id = '{}{}'.format('rgtkSearchPetInfoAnimalName', str(i))
        dog_name = dog.find('div', id=id).a.text
        profile_link = URLs[1]
        img_src = dog.div.a.img['src']
        i += 1

        # Retrieve the img from the img_src link and save the image file in img_path
        img_path = IMAGE_FOLDER + '/' + dog_name + '.jpg'
        try:
            libreq.urlretrieve(img_src, img_path)
        except Exception as e:
            # If there is an error accessing the image, skip the image and continue
            print('Error from urlretrieve({}: {}'.format(img_src, e))
            continue

        IMG_FILE_PATHS.append(img_path)
        NAMES.append(dog_name)
        LINKS.append(profile_link)
        

def getHTML(driver, url):

    driver.get(url)
    html = driver.execute_script('return document.documentElement.outerHTML')
    return html


def main():

    # Run Firefox without GUI by running in headless mode and suppress non-fatal error messages
    options = Options()
    options.headless = True
    options.add_argument('--log-level=3')   # Suppress non-fatal error messages
    options.add_argument('--disable-gpu')   # Hide console pop ups when running script

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
            print('Finished scraping from SF-SPCA')
        else:
            scrape_PHSSPCA(html_source)
            print('Finished scraping from PHS-SPCA')
    
    # Close all browser windows and terminate the webdriver session
    driver.quit()

    # Create the excel spreadsheet using all of the scraped info
    createExcel()

    # Send an email with the excel file attached 
    sendEmail()

#===============================================================================================================#

if __name__ == '__main__':
    main()

