from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd 
import requests
import time

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

 #-----------------------------------------------
    # NASA NEWS 
 #----------------------------------------------- 
def scrape():
 
    browser = init_browser()
    mars_info = {}
        
    # first URL for the title & article 
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    #inform the browser to visit the page
    browser.visit(url)

    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Using BS, we can execute standard functions to capture the page's content
    news_title = soup.find_all('div', class_='content_title')[1].text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text

    mars_info['news_title'] = news_title
    mars_info['news_p'] = news_p
    
   
 #----------------------------------------------- 
    #JPL Mars Space Images / Featured Images
 #----------------------------------------------- 
        
    #get the url for the featured images
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    #inform the browser to visit the page
    browser.visit(image_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #try to get all of the html related to the images
    images = soup.find_all('a', class_='fancybox')
    images

    large_image = []
    for image in images:
        photo = image['data-fancybox-href']
        large_image.append(photo)
    
    large_image

    featured_image_url = 'https://www.jpl.nasa.gov' + photo

    #add this information to our dictionary 
    mars_info['featured_image_url'] = featured_image_url

 #-----------------------------------------------    
   # MARS Facts
 #----------------------------------------------- 
        
    #url for Mars Facts 
    mars_facts = 'https://space-facts.com/mars/'
    browser.visit(mars_facts)

    #read html page with pandas
    facts = pd.read_html(mars_facts)

    #find the table for the table needed on the site 
    df = facts[2]
    df.keys()

    df.columns = ['', 'Mars']
    df

    #convert to html
    html_table = df.to_html()
    print(html_table)

    mars_table = df.to_html('table.html')
    mars_info['mars_facts'] = html_table

 #-----------------------------------------------     
    # Mars Hemispheres
 #----------------------------------------------- 

    #get the url 
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    #use BS to bring in the browser
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #create the list
    hemisphere_image_urls = []

    #retrieve all elements that contain the information needed 
    results = soup.find('div', class_='result-list')
    each_hemisphere = results.find_all('div', class_='item')

    #create a for loop to get all the information
    for i in each_hemisphere:
        hemi_title = i.find('h3').text
        each_link = i.find('a')['href']
        img_url = 'https://astrogeology.usgs.gov/' + each_link
#     get the link to visit each page and get the image 
        browser.visit(img_url)
        html = browser.html
        soup = BeautifulSoup(html,'html.parser')
        each_pg = soup.find('div', class_='downloads')
        image = each_pg.find('a')['href']
        hemisphere_image_urls.append({'title': hemi_title, 'img_url': image})

    mars_info['hemisphere_image_urls'] = hemisphere_image_urls

 #-----------------------------------------------     
    # Mars Info Dictionary 
 #----------------------------------------------- 
    mars_info = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'mars_facts': html_table,
        'hemisphere_image_urls':hemisphere_image_urls
    }

    browser.quit()
    return mars_info
