

```python
# Import all the dependencies
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import requests # This is used to read live websites...
import pandas as pd
import json
import pprint
```

### Note: This code is being run on a Mac Machine


```python
!which chromedriver #Check for chromedriver installed
# Expected output should be /usr/local/bin/chromedriver
```

    /usr/local/bin/chromedriver



```python
# Set the browser path for chrome driver to initialize browser for various steps in our code
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False) #browser variable set, this will be used to invoke browser in the future
```

# NASA Mars News

Scrape the NASA Mars News Site and collect the latest News Title and Paragragh Text. Assign the text to variables that you can reference later.


```python
# URL of the page to be scraped
Mars_URL = 'https://mars.nasa.gov/news/'
# Initiate the splinter browser function to visit the NASA URL
browser.visit(Mars_URL)
# Store the first title in the nasa_mars_news_title variable
nasa_mars_news_title = browser.find_by_css('.content_title').first.text
# Store the first headline in the nasa_mars_news_paragraph variable
nasa_mars_news_paragraph  = browser.find_by_css('.article_teaser_body').first.text
```


```python
# Print the news title and the news paragraph text
print('-------------')
print(nasa_mars_news_title)
print(nasa_mars_news_paragraph)
print('-------------')
```

    -------------
    Mars Helicopter to Fly on NASA’s Next Red Planet Rover Mission
    NASA is adding a Mars helicopter to the agency’s next mission to the Red Planet, Mars 2020.
    -------------


# JPL Mars Space Images - Featured Image

Visit the url for JPL's Featured Space Image here.

Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.

Make sure to find the image url to the full size .jpg image.

Make sure to save a complete url string for this image.


```python
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
print (Featured_Image_URL) # Printing the URL
```

    https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA17462_ip.jpg


# Mars Weather

Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called mars_weather.


```python
# URL of the page to be scraped
Mars_Twitter_URL = 'https://twitter.com/marswxreport?lang=en'
# Initiate the splinter browser function to visit the Mars Twitter URL
browser.visit(Mars_Twitter_URL)

# Creating a simple for loop to scrape the first tweet
for text in browser.find_by_css('.tweet-text'): # Searching for all the tweets
    if text.text.partition(' ')[0] == 'Sol': # Selecting the 'first' tweet in the web page
        mars_weather = text.text # storing the tweet in a variable
        break
print(mars_weather) # printing the text format of the tweet
```

    Sol 2050 (May 13, 2018), Sunny, high 1C/33F, low -71C/-95F, pressure at 7.37 hPa, daylight 05:21-17:20


# Mars Facts

Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.


```python
# URL of the page to be scraped
Mars_Facts_URL = 'http://space-facts.com/mars/'
# Creating Dataframe with the read HTML functionality
mars_planet_profile_df =  pd.read_html (Mars_Facts_URL, attrs = {'id': 'tablepress-mars'})[0]
# Renaming the columns of the dataframe 
mars_planet_profile_df.columns = ['Measurements', 'Values']
mars_df = mars_planet_profile_df.set_index('Measurements') # Changing the index to Measurements
# Displaying the dataframe
mars_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Values</th>
    </tr>
    <tr>
      <th>Measurements</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Equatorial Diameter:</th>
      <td>6,792 km</td>
    </tr>
    <tr>
      <th>Polar Diameter:</th>
      <td>6,752 km</td>
    </tr>
    <tr>
      <th>Mass:</th>
      <td>6.42 x 10^23 kg (10.7% Earth)</td>
    </tr>
    <tr>
      <th>Moons:</th>
      <td>2 (Phobos &amp; Deimos)</td>
    </tr>
    <tr>
      <th>Orbit Distance:</th>
      <td>227,943,824 km (1.52 AU)</td>
    </tr>
    <tr>
      <th>Orbit Period:</th>
      <td>687 days (1.9 years)</td>
    </tr>
    <tr>
      <th>Surface Temperature:</th>
      <td>-153 to 20 °C</td>
    </tr>
    <tr>
      <th>First Record:</th>
      <td>2nd millennium BC</td>
    </tr>
    <tr>
      <th>Recorded By:</th>
      <td>Egyptian astronomers</td>
    </tr>
  </tbody>
</table>
</div>



### Use Pandas to convert the data to a HTML table string.


```python
# Converting our Dataframe to HTML table string using .to_html() feature
mars_facts_HTML_table_string = mars_df.to_html()
pprint.pprint(mars_facts_HTML_table_string) # printing the table string for verfications
```

    ('<table border="1" class="dataframe">\n'
     '  <thead>\n'
     '    <tr style="text-align: right;">\n'
     '      <th></th>\n'
     '      <th>Values</th>\n'
     '    </tr>\n'
     '    <tr>\n'
     '      <th>Measurements</th>\n'
     '      <th></th>\n'
     '    </tr>\n'
     '  </thead>\n'
     '  <tbody>\n'
     '    <tr>\n'
     '      <th>Equatorial Diameter:</th>\n'
     '      <td>6,792 km</td>\n'
     '    </tr>\n'
     '    <tr>\n'
     '      <th>Polar Diameter:</th>\n'
     '      <td>6,752 km</td>\n'
     '    </tr>\n'
     '    <tr>\n'
     '      <th>Mass:</th>\n'
     '      <td>6.42 x 10^23 kg (10.7% Earth)</td>\n'
     '    </tr>\n'
     '    <tr>\n'
     '      <th>Moons:</th>\n'
     '      <td>2 (Phobos &amp; Deimos)</td>\n'
     '    </tr>\n'
     '    <tr>\n'
     '      <th>Orbit Distance:</th>\n'
     '      <td>227,943,824 km (1.52 AU)</td>\n'
     '    </tr>\n'
     '    <tr>\n'
     '      <th>Orbit Period:</th>\n'
     '      <td>687 days (1.9 years)</td>\n'
     '    </tr>\n'
     '    <tr>\n'
     '      <th>Surface Temperature:</th>\n'
     '      <td>-153 to 20 °C</td>\n'
     '    </tr>\n'
     '    <tr>\n'
     '      <th>First Record:</th>\n'
     '      <td>2nd millennium BC</td>\n'
     '    </tr>\n'
     '    <tr>\n'
     '      <th>Recorded By:</th>\n'
     '      <td>Egyptian astronomers</td>\n'
     '    </tr>\n'
     '  </tbody>\n'
     '</table>')


# Mars Hemispheres

Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.

You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.

Save both the image url string for the full resolution hemipshere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.

Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.


```python
# Store the URL in a variable
Mars_Astro_URL = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

#Initiate the splinter browser function to visit the Mars Astro URL
browser.visit(Mars_Astro_URL)
Astro_Response = requests.get(Mars_Astro_URL) # Storing the response variable, Retrieve page with the requests module

#Create BeautifulSoup object; parse with 'HTML'
Astro_Soup = BeautifulSoup(Astro_Response.text, 'html.parser') # Storing the beautiful soup variable for parsing our HTML

# Retrieve the parent div tags (<a> </a>) for all articles
Hemispheres_List = Astro_Soup.find_all('a', class_="itemLink product-item") # find all the <a> </a> elements
# print (Hemispheres_List) # print the list just for verifications
# Commented the print logic out as it was just used for verifications...
```

Save both the image url string for the full resolution hemipshere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.

Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.


```python
# Initialize array to store all the results - this will be an array of dictionaries
hemisphere_image_urls = []

# Loop through results to retrieve article image URL and Title

for image in Hemispheres_List: # start the for loop, Hemispheres_List was defined in the prior cell above
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
    
# Printing the dictionary
pprint.pprint(hemisphere_image_urls)
```

    [{'Image_URL': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg',
      'Title': 'Cerberus Hemisphere Enhanced'},
     {'Image_URL': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg',
      'Title': 'Schiaparelli Hemisphere Enhanced'},
     {'Image_URL': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg',
      'Title': 'Syrtis Major Hemisphere Enhanced'},
     {'Image_URL': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg',
      'Title': 'Valles Marineris Hemisphere Enhanced'}]

