from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd 
import requests

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
 #-----------------------------------------------
    # NASA NEWS 
 #-----------------------------------------------  
    browser = init_browser()
        
    # first URL for the title & article 
    url = f'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'


    #inform the browser to visit the page
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Using BS, we can execute standard functions to capture the page's content
    title = soup.find_all('div', class_='content_title')[1].text
    p_words = soup.find_all('div', class_='article_teaser_body')[0].text 

 #----------------------------------------------- 
    #JPL Mars Space Images / Featured Images
 #----------------------------------------------- 
    browser = init_browser 
    featured_image = []

    #get the url for the featured images
    image_url = f'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    #inform the browser to visit the page
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

 #-----------------------------------------------    
   # MARS Facts
 #----------------------------------------------- 
    browser = init_browser 
    mars_facts = []

    #url for Mars Facts 
    url = f'https://space-facts.com/mars/'

    #read html page with pandas
    facts = pd.read_html(url)

    #find the table for the table needed on the site 
    df = facts[2]
    df.keys()

    df.columns = ['', 'Mars']
    df

    #convert to html
    html_table = df.to_html()
    print(html_table)

    mars_table = df.to_html('table.html')

 #-----------------------------------------------     
    # Mars Hemispheres
 #----------------------------------------------- 
    browser = init_browser 
    

    #get the url 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    #use BS to bring in the browser
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #create the list
    mars_urls = []

    #retrieve all elements that contain the information needed 
    results = soup.find('div', class_='result-list')
    each_hemisphere = results.find_all('div', class_='item')

    #create a for loop to get all the information
    for i in each_hemisphere:
        title = i.find('h3').text
        each_link = i.find('a')['href']
        img_url = 'https://astrogeology.usgs.gov/' + each_link
#     get the link to visit each page and get the image 
        browser.visit(img_url)
        html = browser.html
        soup = BeautifulSoup(html,'html.parser')
        each_pg = soup.find('div', class_='downloads')
        image = each_pg.find('a')['href']
        mars_urls.append({'title': title, 'img_url': image})

 #-----------------------------------------------     
    # Mars Info Dictionary 
 #----------------------------------------------- 
    mars_info = {
        'title': title,
        'article_text': p_words,
        'featured_image_url': featured_image_url,
        'table': mars_table,
        'hemisphere':mars_urls
    }
    
    print(mars_info)