# Importing dependencies:
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import time

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    #-------------------------------------------------------------------------------------

    # Visit NASA url:
    nasa_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(nasa_url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time = 1)

    # Scrape page into nasa_soup:
    html = browser.html
    nasa_soup = bs(html, "html.parser")

    # Scraping the lastest Mars 'News Title' and 'News Text':
    news_title = nasa_soup.find("div.content_title").text
    news_text = nasa_soup.find("div.article_teaser_body").text

    # Closing the browser after scraping:
    browser.quit()

    #-------------------------------------------------------------------------------------

    # Visit JPL url:
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    base_url = "https://www.jpl.nasa.gov"
    browser.visit(jpl_url)
    browser.is_element_present_by_css("div.carousel_items", wait_time = 1)

    # Scrape page into jpl_soup:
    html = browser.html
    jpl_soup = bs(html, "html.parser")

    # Scraping the 'Featured Image' from JPL:
    featured_image_path = jpl_soup.find('a', class_='button fancybox').get('data-fancybox-href').strip()
    featured_image_url = base_url + featured_image_path

    # Closing the browser after scraping:
    browser.quit()

    #-------------------------------------------------------------------------------------

    # Visit Space Facts url:
    space_facts_url = "https://space-facts.com/mars/"
    browser.visit(space_facts_url)

    # Scrape page into space_soup:
    html=browser.html
    space_soup = bs(html, "html.parser")

    # Using pandas we will read the table:
    mars_table = pd.read_html(space_facts_url)

    # Setting up Df:
    df = mars_table[0]
    
    # Renaming the columns:
    mars_facts =df.rename(columns={0: "", 1: "Mars"})

    # Using pandas to generate HTML table from DF:
    html_table = mars_facts.to_html()

    # Strip the unwanted newlines to clean up table:
    html_table.replace("\n", "")

    # Saving the table as an html file:
    mars_html = mars_facts.to_html("mars_html.html", index=False)

    # Closing the browser after scraping:
    browser.quit()

    #-------------------------------------------------------------------------------------

    # Visit USGS url:
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    base_usgs_url = "https://astrogeology.usgs.gov"
    browser.visit(usgs_url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time = 1)

    # HTML Object:
    html = browser.html
    time.sleep(10)
    # Parse HTML with BeautifulSoup (bs) "html.parser" or "lxml":
    hemi_soup = bs(html, "html.parser")

    # Narrowing down the search:
    hemi_results = hemi_soup.find("div", class_="result-list")
    hemi_item = hemi_results.find_all("div", class_="item")

    # A list of all four links to each hemisphere:
    mars_imgs = []

    # A loop to iterate through all four links:
    for i in range(4):
        try:
            # Find the link:
            # browser.find_by_css("a.product-item h3")[i].click()
            time.sleep(1)
            # Find the "Image Title":
            img_title = i.find("h2", class_="title").text
            # Find the path to the image:
            img_pg_url = i.find("a")["href"]
            # Combining the usgs url with the image path to get the "Image URL":
            img_url = base_usgs_url + img_pg_url
            # Visit the image's url:
            browser.visit(img_url)
            # HTML Object:
            img_html = browser.html
            # Parse HTML with BeautifulSoup (bs) "html.parser" or "lxml":
            img_soup = bs(img_html, "html.parser")
            # Find the full image(s):
            img = img_soup.find("img", class_="wide-image")["src"]
            full_img = base_usgs_url + img
            # Storing the titles and images into the list:
            mars_imgs.append({
                "image_title": img_title,
                "image_link": full_img
            })
        except Exception as e:
            print(e)

        # Closing the browser after scraping:
        browser.quit()

    # Creating a dictionary for all of the scraped/collected mars data from all websites:
    mars_info = {
        "news_title": news_title,
        "news_text": news_text,
        "featured_image": featured_image_url,
        "mars_facts_table": mars_html,
        "images": mars_imgs
    }

    # Return results:
    return mars_info