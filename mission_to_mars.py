#Dependencies
import pandas as pd
import numpy as np
import time
from bs4 import BeautifulSoup as bs
from splinter import Browser

def scrape():
    ## Step 1 - Scraping
    mars_dictionary = {}
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    #Scrape the NASA Mars News Site
    url_news = "https://mars.nasa.gov/news/"
    browser.visit(url_news)

    ## NASA Mars News

    ##Use Beautiful soup to parse html
    html = browser.html
    soup = bs(html, 'lxml')

    #get  latest News Title and Paragragh Text
    title = soup.find('div', class_='content_title').get_text()
    time.sleep(5)
    p_text = soup.find('div', class_='article_teaser_body').get_text()
    
    mars_dictionary['title'] = title
    mars_dictionary['p_text'] = p_text
    
    # JPL Mars Space Images - Featured Image

    #Visit the url for JPL's Featured Space Image
    browser = Browser('chrome', **executable_path, headless=False)
    url_jpl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_jpl)
    html_image = browser.html
    soup_image = bs(html_image, 'lxml')
    featured_image = soup_image.find('a', class_='fancybox')
    featured_image_url = "https://www.jpl.nasa.gov/" + featured_image["data-fancybox-href"]
    
    mars_dictionary['featured_image_url'] = featured_image_url
    
    # Mars Weather

    #Visit the Mars Weather twitter account
    browser = Browser('chrome', **executable_path, headless=False)
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)
    html_weather = browser.html
    soup_weather = bs(html_weather, 'lxml')

    mars_weather = soup_weather.find("p",class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").get_text()
    
    mars_dictionary['mars_weather'] = mars_weather

    # Mars Facts

    mars_facts_df = pd.read_html('http://space-facts.com/mars/')
    mars_data_df = pd.DataFrame(mars_facts_df[0])
    mars_data_df.columns=['Mars', 'Facts']
    mars_data_df = mars_data_df.set_index("Mars")
    marsfacts = str(mars_data_df.to_html(index=False))
    
    mars_dictionary['mars_facts'] = marsfacts

    # Mars Hemispheres

    #Visit the USGS Astrogeology site
    browser = Browser('chrome', **executable_path, headless=False)
    url_hemispheres = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemispheres)
    html = browser.html
    soup = bs(html, 'lxml')
    hemisphere_image_urls = []

    for i in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = bs(html, 'lxml')
        part_url = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ part_url
        dictn={"title":img_title,"img_url":img_url}
        hemisphere_image_urls.append(dictn)
        browser.back()
    
    mars_dictionary['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_dictionary
#print(scrape())

