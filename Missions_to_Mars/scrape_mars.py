# Dependencies 
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import os
import time
import requests
import warnings

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser("chrome", **executable_path, headless=False)

# Global dictionary to MongoDB
mars_info = {}

# NASA MARS NEWS
def scrape_mars_news():

        # Initialize browser 
        browser = init_browser()

        #browser.is_element_present_by_css("div.content_title", wait_time=)

        # Splinter module
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        # HTML object
        html = browser.html

        # Parse HTML w/ Beautiful Soup
        soup = bs(html, 'html.parser')

        # Retrieve latest element containing news title & news_paragraph
        news_title = soup.find('div', class_='content_title').find('a').text
        news_p = soup.find('div', class_='article_teaser_body').text

        # Dictionary
        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_p

        return mars_info

# FEATURED IMAGE
def scrape_mars_image():

        # Initialize browser 
        browser = init_browser()

        #browser.is_element_present_by_css("img.jpg", wait_time=)

        # Splinter module
        featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(featured_image_url)

        # HTML object 
        html_image = browser.html

        # Parse HTML w/ Beautiful Soup
        soup = bs(html_image, 'html.parser')

        # Retrieve image 
        image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

        # Website url 
        main_url = 'https://www.jpl.nasa.gov'

        # Concatenate website url w/ scrapped route
        image_url = main_url + image_url

        # Display link
        image_url 

        # Dictionary
        mars_info['image_url'] = image_url 
        
        browser.quit()

        return mars_info

        

# Mars Weather 
def scrape_mars_weather():

        # Initialize browser 
        browser = init_browser()

        #browser.is_element_present_by_css("div", wait_time=)

        # Splinter module
        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)

        # HTML object 
        html_weather = browser.html

        # Parse HTML w/ Beautiful Soup
        soup = bs(html_weather, 'html.parser')

        # Find all elements that contain tweets
        latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

        # Retrieve all elements that contain news title in the specified range & retrieve weather word
        for tweet in latest_tweets: 
            mars_weather = tweet.find('p').text
            if 'Sol' and 'pressure' in mars_weather:
                #print(mars_weather)
                break
            else: 
                pass
         # Dictionary
        mars_info['mars_weather'] = mars_weather

        browser.quit()

        return mars_info
        
# Mars Facts
def scrape_mars_facts():

        # Initialize browser 
        browser = init_browser()

         # Facts url 
        url = 'http://space-facts.com/mars/'
        browser.visit(url)

        # Pandas "read_html" to parse URL
        tables = pd.read_html(url)
        #Facts DataFrame
        df = tables[1]
        #Assign columns
        df.columns = ['Description', 'Value']
        html_table = df.to_html(table_id="html_tbl_css",justify='left',index=False)

        # Dictionary
        mars_info['tables'] = html_table

        return mars_info

# Mars Hemisphere

def scrape_mars_hemispheres():

        # Initialize browser 
        browser = init_browser()

        # Splinter module 
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        # HTML object
        html_hemispheres = browser.html

        # Parse HTML w/ Beautiful Soup
        soup = bs(html_hemispheres, 'html.parser')

        # Retreive all items that contain hemispheres
        items = soup.find_all('div', class_='item')

        # List for hemisphere urls 
        hiu = []

        # Store main_ul 
        hemispheres_main_url = 'https://astrogeology.usgs.gov' 

        # Loop through the items previously stored
        for i in items: 
            # Store title
            title = i.find('h3').text
            
            # Store link leading to full image website
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
            # Visit link containing full image website 
            browser.visit(hemispheres_main_url + partial_img_url)
            
            # HTML object of individual hemisphere
            partial_img_html = browser.html
            
            # Parse HTML w/ Beautiful Soup for every hemisphere website 
            soup = bs( partial_img_html, 'html.parser')
            
            # Retrieve full image source 
            img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
            # Append to list of dictionaries 
            hiu.append({"title" : title, "img_url" : img_url})

        mars_info['hiu'] = hiu
        
       
        browser.quit()

        # Mars_data dictionary 

        return mars_info
