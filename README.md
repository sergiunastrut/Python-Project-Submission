# Movie Recommender App Based on User Chosen Genre
## Overview
This movie recommender app was built as a Python project which consumes user-input genre, then scrapes Top 25 Most Popular IMDb titles for the genre and randomly suggest one of those to the user, via a Tkinter app.
## Features
**Web scraping:** BeautifulSoup was used to scrape Top 25 Most Popular Movies/Genre from IMDb
**Data Processing:** Pandas was used to clean and process the scraped data stored in a CSV file.
**Movies Suggesting App:** Tkinter was used to create an app where user selects genre from a dropdown list, then gets a random movie when clicking the button.
## Requirements
Please make sure you use pip install in your PyCharm IDE and then add the following:
- requests~=2.32.3
- pandas~=2.2.2
- bs4~=0.0.2
- beautifulsoup4~=4.12.3
- lxml~=5.2.2
  
> pip install pandas beautifulsoup4 requests lxml
## User Guide
1. Run the Scraping Script & Wait for 2-3 minutes so that all genres are scraped from IMDb. When finished, movielist.csv will be created.
 
   > run IMDb Movie Recommender (sergiun)
   
2. Interact with the Tkinter App for movie recommendations: as soon as scraping & data processing is complete, the Tkinter app will pop up, you will need to select a genre from the dropdown, then click on 'Suggest Movie' (repeat this as many times as you want).

   > select a genre in the Tkinter app, then click on 'Suggest Movie'
