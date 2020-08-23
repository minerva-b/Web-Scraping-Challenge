# Importing dependencies:
import pandas as pd
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import time


def init_browser():
    executable_path = {"executable_path": "C://Users/mgban/Desktop/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # Visit NASA url:
    nasa_url = "https://mars.nasa.gov/news/"
    browser.visit(nasa_url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time = 1)

    # Scrape page into NASA Soup:
    html = browser.html
    nasa_soup = bs(html, "html.parser")

    # Scraping and collecting the lastest 'News Title' and 'Paragraph Text':
    # latest_news_article = nasa_soup.find('ul', class_='item_list')
    news_title = nasa_soup.find('div', class_='content_title').get_text()
    news_parag = nasa_soup.find('div', class_='article_teaser_body').get_text()

    #-------------------------------------------------------------------------------------

    # Visit JPL url:
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars#submit'
    browser.visit(jpl_url )
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time = 1)

    # Scrape page into JPL Soup:
    html = browser.html
    jpl_soup = bs(html, "html.parser")
    
    # Scraping and collecting JPL's featured image:
    featured_image_path = jpl_soup.find('a', class_='button fancybox').get('data-fancybox-href').strip()
    featured_image_url = jpl_url + featured_image_path

    #-------------------------------------------------------------------------------------

    # Visit Space Facts url:
    space_facts_url  = "https://space-facts.com/mars/"
    browser.visit(space_facts_url )
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time = 1)

    # Scrape page into Space Facts Soup:
    html = browser.html
    space_soup = bs(html, "html.parser")

    # Using pandas we will scrape the webpage to read the table of facts:
    mars_facts = pd.read_html(space_facts_url)
    
    # Printing only the first table from the webpage
    df = mars_facts[0]

    # Renaming the columns:
    mars_facts_df = df.rename(columns={0: "", 1: "Mars"})

    # Using pandas, generate HTML table from Dataframe:
    html_table = mars_facts_df.to_html()

    # Strip unwanted newlines to clean up the table:
    html_table.replace('\n', '')

    # Saving the table directly to a file:
    mars_table = mars_facts_df.to_html('mars_facts.html', index=False)

    #-------------------------------------------------------------------------------------

    # Visit USGS url:
    usgs_url = "https://astrogeology.usgs.gov"

    # Since we must go into each hemisphere's link to gather the appropiate image_url
    # Loop and iterate through all four hemisphere's link:
    urls = [
        'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced',
        'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced',
        'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced',
        'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    ]

    # Scraping for image 'title' and image 'url' for all hemispheres:
    img_url_list = []

    # To search through each link and scrape the image 'title' and 'img_url':
    for url in urls:
        # Creating a path to the 'chromedriver' to be able to use 'Browser' from splinter:
        executable_path = {'executable_path':'C://Users/mgban/Desktop/chromedriver.exe'}
        browser = Browser('chrome', **executable_path, headless=False)
        browser.visit(url)
        browser.is_element_present_by_css("ul.item_list li.slide", wait_time = 10)
        
        # HTML object:
        html = browser.html
        # Parse HTML with BeautifulSoup as bs 'html.parser' or 'lxml':
        soup = bs(html, 'html.parser')
        
        # Searching for through the tags:
        title = soup.find('h2', class_='title').text
        img_url = soup.find('img', class_='wide-image')['src']
        
        # Storing the 'title' and 'img_url':
        img_url_list.append({
            'Image_Title': title, 
            'Image_URL': usgs_url + img_url
        })

    # Creating Python Dictionary:
    scraped_data = {
        'News_Title': news_title,
        'News_Pg': news_parag,
        'Featured_Img_URL': featured_image_url,
        'Mars_Facts_Table': mars_table,
        'Images': img_url_list,
    }

    # Close the browser after scraping:
    browser.quit()

    # Return results:
    return mars_data