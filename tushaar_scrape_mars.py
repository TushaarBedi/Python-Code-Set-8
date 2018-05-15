# Import all the dependencies
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import requests # This is used to read live websites...
import pandas as pd
import json
import pprint

# Set the browser path for chrome driver to initialize browser for various steps in our code
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False) #browser variable set, this will be used to invoke browser in the future

# Initialize the scrape () function which will return a Python Dictionary with all the output data
def scrape():
    scrape_mars_dict = {}
    
    #----------------------------------------------------------------------------------------------
    # Scrape code for NASA Mars News
    # URL of the page to be scraped
    Mars_URL = 'https://mars.nasa.gov/news/'
    # Initiate the splinter browser function to visit the NASA URL
    browser.visit(Mars_URL)
    # Store the first title in the nasa_mars_news_title variable
    nasa_mars_news_title = browser.find_by_css('.content_title').first.text
    # Store the first headline in the nasa_mars_news_paragraph variable
    nasa_mars_news_paragraph  = browser.find_by_css('.article_teaser_body').first.text
        
    #----------------------------------------------------------------------------------------------
    # Scrape code for the URL of JPL Mars Space Images - Featured Image

    # URL of the page to be scraped
    JPL_Image_URL = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    # Initiate the splinter browser function to visit the JPL URL
    browser.visit(JPL_Image_URL)
    jpl_html = browser.html # Set a variable for rendering URL's html reponse
    jpl_soup = BeautifulSoup(jpl_html, 'html.parser') # set beautiful soup variable for parsing our HTML
    # The below step is important. When we inspect the JPL_Image_URL in chrome, you will find that the featured image is
    # in the fotter section. We will store this in a variable defined below.
    jpl_results = jpl_soup.find('footer') 
    # We see that image URL is embedded in 'data-fancybox-href' in the <a> </a> tags
    Image_URL = jpl_results.find('a')['data-fancybox-href']
    # When we print Image_URL we find that it is a partial URL and needs to be appended by the leading URL which we do below
    Featured_Image_URL = "https://www.jpl.nasa.gov" + Image_URL

    #----------------------------------------------------------------------------------------------
    # Scrape code for the Mars Weather (from Mars Twitter Page)
    # URL of the page to be scraped
    Mars_Twitter_URL = 'https://twitter.com/marswxreport?lang=en'
    # Initiate the splinter browser function to visit the Mars Twitter URL
    browser.visit(Mars_Twitter_URL)
    # Creating a simple for loop to scrape the first tweet
    for text in browser.find_by_css('.tweet-text'): # Searching for all the tweets
        if text.text.partition(' ')[0] == 'Sol': # Selecting the 'first' tweet in the web page
            mars_weather = text.text # storing the tweet in the mars_weather variable
            break

    #----------------------------------------------------------------------------------------------
    # Scrape code for the Mars Facts
    # URL of the page to be scraped
    Mars_Facts_URL = 'http://space-facts.com/mars/'
    # Creating Dataframe with the read HTML functionality
    mars_planet_profile_df =  pd.read_html (Mars_Facts_URL, attrs = {'id': 'tablepress-mars'})[0]
    # Renaming the columns of the dataframe 
    mars_planet_profile_df.columns = ['Measurements', 'Values']
    # Changing the index of the dataframe to Measurements
    mars_df = mars_planet_profile_df.set_index('Measurements') 
    # Converting our Dataframe to HTML table string using .to_html() feature
    mars_facts_HTML_table_string = mars_df.to_html()

    #----------------------------------------------------------------------------------------------
    # Scrape code for the Mars Hemispheres

    # Store the URL in a variable
    Mars_Astro_URL = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    #Initiate the splinter browser function to visit the Mars Astro URL
    browser.visit(Mars_Astro_URL)
    Astro_Response = requests.get(Mars_Astro_URL) # Storing the response variable, Retrieve page with the requests module
    #Create BeautifulSoup object; parse with 'HTML'
    Astro_Soup = BeautifulSoup(Astro_Response.text, 'html.parser') # Storing the beautiful soup variable for parsing our HTML
    # Retrieve the parent div tags (<a> </a>) for all articles
    Hemispheres_List = Astro_Soup.find_all('a', class_="itemLink product-item") # find all the <a> </a> elements
    # Hemispheres_List # print the list just for verifications
    # Initialize array to store all the results - this will be an array of dictionaries
    hemisphere_image_urls = []

    # Loop through results to retrieve article image URL and Title

    for image in Hemispheres_List:
        image_title = image.find('h3').text # Image titles are in <h3> </h3> tags, found via inspecting the page
        image_link = "https://astrogeology.usgs.gov/" + image['href'] # appending the image link with leading URL and <href> tags
        
        # This function will request the links to be clicked to in order to find the image url to the full resolution image.
        image_request = requests.get(image_link) 
        # Storing the beautiful soup variable for parsing our HTML as we go to a new page
        soup = BeautifulSoup(image_request.text, 'html.parser')
        # Storing image tag variable by finding div in class 'downloads' -> this is found by inspecting the image URL
        image_tag = soup.find('div', class_='downloads')
        # Storing image URL variable loacated in <a> href </a> portion -> this is found by inspecting the image URL
        image_url = image_tag.find('a')['href']
        # Appending all the information in our array of dictionaries, as asked for in the homework    
        hemisphere_image_urls.append({"Title": image_title, "Image_URL": image_url}) 
    
    #----------------------------------------------------------------------------------------------
    # Creating output dictionary which will contail ALL of our scraped data

    scrape_mars_dict = {
                        "News_Title": nasa_mars_news_title,
                        "News_Paragraph": nasa_mars_news_paragraph,
                        "Featured_Image_Link": Featured_Image_URL,
                        "Weather": mars_weather,
                        "Interesting_Facts": mars_facts_HTML_table_string,
                        "Hemisphere_Images": hemisphere_image_urls
                        }
    
    return (scrape_mars_dict)
    








