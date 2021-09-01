# Web Scraper for Adoptable Dogs

## Description
A webscraping Python script that scrapes information on all available adoptable dogs from the [San Francisco SPCA](https://sfspca.org) and [Peninsula Humane Society & SPCA](https://phs-spca.org/) websites. The information is then written and saved to an XLSX file and emailed to my inbox. The web scraping functionality was implemented with Selenium and BeautifulSoup4. The Python script was executed at one hour intervals throughout the day using Windows Task Scheduler to automate the process of checking the websites for adoptable dogs.

## Motivation
My family and I were looking to adopt a dog at the time. However, there was an extremely large pool of adopters and we would often miss the chance in getting to meet the dog that we were interested in. Rather than constantly checking the website for updates, I decided to automate this process and had the script run in the background with my email inbox open to be notified hourly. Although simply checking the websites was a simple task, I wanted to use this opportunity to learn new technologies while also creating something that had a real-world personal use case.

## Dependencies
- [Selenium](https://www.selenium.dev/)
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
- [email.message](https://docs.python.org/3/library/email.message.html)
- [xlsxwriter](https://xlsxwriter.readthedocs.io/)
- [smtplib](https://docs.python.org/3/library/smtplib.html)

