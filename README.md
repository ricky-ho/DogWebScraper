## DogScraper

# Description
This is a webscraping project that I worked on as my family and I were looking to adopt a dog. Rather than constantly checking 
the websites manually, I automated the process by using Python to scrape the information off of the websites and wrote it
onto an excel sheet which would be emailed to myself. I used Windows Task Schedular to run this Python code every hour in the 
background, so I would be updated every hour of the available adoptable dogs. This code was intended for my own personal use
and will not run properly on any other machines. 

# Dependencies
The program was built using the following libraries which must be installed:
- selenium
- beautifulsoup4
- urllib.request
- email.message
- xlsxwriter
- smtplib
- yaml

