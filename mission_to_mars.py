{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 34,
   "metadata": {},
   "outputs": [],
   "source": [
    "# import dependencies\n",
    "import pandas as pd\n",
    "from splinter import Browser\n",
    "from bs4 import BeautifulSoup as bs\n",
    "import time\n",
    "#import pymysql\n",
    "#pymysql.install_as_MySQLdb()\n",
    "\n",
    "\n",
    "#import pandas as pd\n",
    "from sqlalchemy import create_engine\n",
    "from sqlalchemy.sql import select\n",
    "\n",
    "\n",
    "from sqlalchemy.ext.automap import automap_base\n",
    "from sqlalchemy.orm import Session\n",
    "from sqlalchemy import func\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 38,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Open brower connection\n",
    "\n",
    "executable_path = {'executable_path': 'chromedriver.exe'}\n",
    "browser = Browser('chrome', **executable_path, headless=False)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "NASA Mars News"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "#declare url and parser\n",
    "url = \"https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest\"\n",
    "browser.visit(url)\n",
    "html = browser.html\n",
    "soup = bs(html, \"html.parser\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Mars InSight Lander Seen in First Images from Space  Look closely, and you can make out the lander's solar panels.\n"
     ]
    }
   ],
   "source": [
    "news_title = soup.find('div', class_='content_title').text\n",
    "news_p =soup.find('div',class_='article_teaser_body').text\n",
    "print(news_title, news_p)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "JPL Featured Image"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "#declare url and parser\n",
    "url = \"https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars\"\n",
    "browser.visit(url)\n",
    "html = browser.html\n",
    "soup = bs(html, \"html.parser\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA14254_ip.jpg'"
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "img = soup.find('a', id='full_image')\n",
    "#print(img['data-fancybox-href'])\n",
    "featured_image_url = 'https://www.jpl.nasa.gov'+img['data-fancybox-href']\n",
    "featured_image_url\n",
    "#browser.click_link_by_partial_text('FULL IMAGE')\n",
    "        "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Mars Weather"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "url = \"https://twitter.com/marswxreport?lang=en\"\n",
    "browser.visit(url)\n",
    "html = browser.html\n",
    "soup = bs(html, \"html.parser\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'Sol 2258 (2018-12-13), high -6C/21F, low -70C/-93F, pressure at 8.41 hPa, daylight 06:37-18:51'"
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#tweets = soup.find('li', {'data-item-type':'tweet'})\n",
    "tweets = soup.find('div', {'class':'tweet','data-screen-name':'MarsWxReport'})\n",
    "\n",
    "#for tweet in tweets:\n",
    "    #print(tweet.text)\n",
    "#soup\n",
    "mars_weather = tweets.p.text\n",
    "mars_weather"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Mars Facts"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 95,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "{'1': ['Equatorial Diameter:', '6,792 km'],\n",
       " '2': ['Polar Diameter:', '6,752 km'],\n",
       " '3': ['Mass:', '6.42 x 10^23 kg (10.7% Earth)'],\n",
       " '4': ['Moons:', '2 (Phobos & Deimos)'],\n",
       " '5': ['Orbit Distance:', '227,943,824 km (1.52 AU)'],\n",
       " '6': ['Orbit Period:', '687 days (1.9 years)'],\n",
       " '7': ['Surface Temperature:', '-153 to 20 °C'],\n",
       " '8': ['First Record:', '2nd millennium BC'],\n",
       " '9': ['Recorded By:', 'Egyptian astronomers']}"
      ]
     },
     "execution_count": 95,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#declare url and parser\n",
    "url = \"http://space-facts.com/mars/\"\n",
    "table = pd.read_html(url)\n",
    "\n",
    "df_mars = pd.DataFrame(table[0])\n",
    "df_mars.columns = [\"fact\",\"value\"]\n",
    "df_marsT = df_mars.T\n",
    "df_marsT.columns=['1','2','3','4','5','6','7','8','9']\n",
    "#df_mars.set_index( 'fact',drop=True, inplace = True)\n",
    "df_marsT.head()\n",
    "m_dict = df_marsT.to_dict('list')\n",
    "m_dict"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Mars Hemispheres"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 39,
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "\n",
    "url = \"https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars\"\n",
    "browser.visit(url)\n",
    "html = browser.html\n",
    "soup = bs(html, \"html.parser\")\n",
    "\n",
    " "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 49,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "/search/map/Mars/Viking/cerberus_enhanced\n",
      "Cerberus Hemisphere http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg\n",
      "/search/map/Mars/Viking/schiaparelli_enhanced\n",
      "Schiaparelli Hemisphere http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg\n",
      "/search/map/Mars/Viking/syrtis_major_enhanced\n",
      "Syrtis Major Hemisphere http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg\n",
      "/search/map/Mars/Viking/valles_marineris_enhanced\n",
      "Valles Marineris Hemisphere http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "[{'title': 'Cerberus Hemisphere',\n",
       "  'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'},\n",
       " {'title': 'Schiaparelli Hemisphere',\n",
       "  'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'},\n",
       " {'title': 'Syrtis Major Hemisphere',\n",
       "  'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'},\n",
       " {'title': 'Valles Marineris Hemisphere',\n",
       "  'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'}]"
      ]
     },
     "execution_count": 49,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "images = soup.find_all('div',class_='item')\n",
    "#browser.click_link_by_partial_href('search/map/Mars/Viking/cerberus_enhanced')\n",
    "#    \n",
    "hemisphere_image_urls = []\n",
    "hemis = {}\n",
    "for image in images:\n",
    "    url2 = image.a['href']\n",
    "    browser.visit('https://astrogeology.usgs.gov'+url2)\n",
    "    html2 = browser.html\n",
    "    soup2 = bs(html2,\"html.parser\")\n",
    "    link = soup2.find('div',{'class':'downloads'})\n",
    "    title = browser.title.replace(' Enhanced | USGS Astrogeology Science Center','')\n",
    "    img_url = link.li.a['href']\n",
    "    hemisphere_image_urls.append({'title':title,'img_url':img_url})\n",
    "hemisphere_image_urls    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
