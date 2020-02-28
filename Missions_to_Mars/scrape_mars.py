from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=True)

def scrape():
    mars_info_dict = {}
  
# NASA Mars News scrape
    browser = init_browser()
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)

    time.sleep(1)

    html_news = browser.html
    soup_news = BeautifulSoup(html_news, "html.parser")

    title = soup_news.find('div', class_="content_title").get_text()
    mars_info_dict["news_title"] = title
    paragraph = soup_news.find('div', class_="article_teaser_body").get_text()
    mars_info_dict["news_paragraph"] = paragraph

    browser.quit()

# JPL Mars Space Images - Featured Image
    browser = init_browser()
    pic_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(pic_url)

    time.sleep(1)

    html_pic = browser.html
    soup_pic = BeautifulSoup(html_pic, 'html.parser')

    image_url = soup_pic.find('a', class_="button fancybox").get('data-fancybox-href')
    base_url = "https://www.jpl.nasa.gov"
    featured_image_url = base_url + image_url
    mars_info_dict["featured_image_url"] = featured_image_url

    browser.quit()

# Mars Facts
    browser = init_browser()
    mars_facts_url = "https://space-facts.com/mars/"
    browser.visit(mars_facts_url)
    
    tables = pd.read_html(mars_facts_url)
    mars_facts_df = tables[0]
    mars_facts_df.columns = ['Description', 'Value']
    mars_facts_df.set_index('Description', inplace=True)
    
    mars_facts_html = mars_facts_df.to_html()
    mars_info_dict["mars_facts_html"] = mars_facts_html

    browser.quit()

# Mars Hemispheres
    browser = init_browser()
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    time.sleep(1)

    html_hemispheres = browser.html
    soup_hemispheres = BeautifulSoup(html_hemispheres, 'html.parser')

    hemisphere_image_urls = []
    hemisphere_dict = {}

    results = soup_hemispheres.find_all('h3')

    for result in results:
        title_text = result.text.split("E")[0]
        browser.click_link_by_partial_text(title_text)
    
        html2 = browser.html
        soup2 = BeautifulSoup(html2, 'html.parser')
    
        image_section = soup2.find('div', class_="downloads")
        image_url = image_section.find('a').get('href')

        hemisphere_dict["title"] = title_text
        hemisphere_dict["image_url"] = image_url
    
        hemisphere_image_urls.append(hemisphere_dict)
    
        hemisphere_dict = {}
    
        browser.visit(hemispheres_url)

    mars_info_dict["hemisphere_image_urls"] = hemisphere_image_urls

    browser.quit()

    return mars_info_dict
