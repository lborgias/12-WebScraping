import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time

#Open brower connection
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
        
    browser = init_browser()

    #declare url and parser
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")

    news_title = soup.find('div', class_='content_title').text
    news_p =soup.find('div',class_='article_teaser_body').text


    #declare url and parser
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")

    img = soup.find('a', id='full_image')
    #print(img['data-fancybox-href'])
    featured_image_url = 'https://www.jpl.nasa.gov'+img['data-fancybox-href']

    #browser.click_link_by_partial_text('FULL IMAGE')
            
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")


    #tweets = soup.find('li', {'data-item-type':'tweet'})
    tweets = soup.find('div', {'class':'tweet','data-screen-name':'MarsWxReport'})

    #for tweet in tweets:
        #print(tweet.text)
    #soup
    mars_weather = tweets.p.text


    #declare url and parser
    url = "http://space-facts.com/mars/"
    table = pd.read_html(url)

    df_mars = pd.DataFrame(table[0])
    df_mars.columns = ["fact","value"]
    #df_marsT = df_mars.T
    #df_marsT.columns=['1','2','3','4','5','6','7','8','9']
    df_mars.set_index( 'fact',drop=True, inplace = True)
    #df_marsT.head()
    m_dict = df_mars.to_html(escape=False)


    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")

    h_images = soup.find_all('div',class_='item')
    #browser.click_link_by_partial_href('search/map/Mars/Viking/cerberus_enhanced')
    #    
    hemisphere_image_urls = []
    for image in h_images:
        url2 = image.a['href']
        browser.visit('https://astrogeology.usgs.gov'+url2)
        html2 = browser.html
        soup2 = bs(html2,"html.parser")
        link = soup2.find('div',{'class':'downloads'})
        title = browser.title.replace(' Enhanced | USGS Astrogeology Science Center','')
        img_url = link.li.a['href']
        hemisphere_image_urls.append({'title':title,'img_url':img_url})
    hemisphere_image_urls    


    mars_data = {
            "news_title": news_title,
            "news_p": news_p,
            "featured_image_url": featured_image_url,
            "mars_weather":mars_weather,
            "df_mars":m_dict,
            "hemisphere_image_urls":hemisphere_image_urls
        }

    browser.quit()

    return mars_data
