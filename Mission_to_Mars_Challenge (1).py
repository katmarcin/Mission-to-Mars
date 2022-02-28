#!/usr/bin/env python
# coding: utf-8

# In[58]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[61]:


# set up Splinter 
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[39]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1) # searching for elements with a specific combination of tag (div) and attribute (list_text)
# wait 1 second before searching components, useful if image heavy.


# In[40]:


# HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text') # the variable to look for the <div /> tag and its descendent 


# In[41]:


# begin scraping. assign the title and summary text to variables. find () within variable.
slide_elem.find('div', class_='content_title')


# In[42]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[43]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images 

# In[44]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[45]:


# Find and click the full image button. Full image will be displayed in browser. Full_image_elem to hold scraping result.
# we want our browser to click the 2nd button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[46]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[47]:


# Find the relative image url. Point to BS where the image should be instead of grabbing the URL directly
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')  #get pulls the link to the image
img_url_rel
#code will still pull most recent image.


# In[48]:


# Use the base URL to create an absolute URL. Use f-string as a cleaner way to print statements and evaluated at run-time.
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[49]:


#galaxyfacts-mars
df = pd.read_html('https://galaxyfacts-mars.com')[0] #new DataFrame from the HTML table #
# read_html() specifically searches for and returns a list of tables found in the HTML, pull only 1st table. Returns table in DF.
df.columns=['description', 'Mars', 'Earth'] #assigns columns to DF
df.set_index('description', inplace=True) #setting dxn as index. inplace = True means updated index will remain in place w/o reassigned DF to new var.
df


# In[35]:


df.to_html() #adding this DF --> HTML code to web app


# In[19]:


browser.quit()


# ### Starter code

# In[8]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[9]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ## Visit the NASA Mars News Site

# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[ ]:


slide_elem.find('div', class_='content_title')


# In[ ]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[ ]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ## JPL Space Images Featured Image

# In[ ]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[ ]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[ ]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[ ]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[ ]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ## Mars Facts
# 

# In[ ]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[ ]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[ ]:


df.to_html()


# ### D1: Scrape High-Resolution Mars' Hemisphere Images and Titles

# ## Hemispheres

# In[2]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[3]:


# set up Splinter 
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[4]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[5]:





# In[9]:


# TESTER
hemisphere_image_urls = []


for i in range(4):
    
    hemisphere = {}
    
    browser.find_by_css('a.product-item img')[i].click()
    sample_elem = browser.links.find_by_text('Sample').first
    hemisphere['img_url'] = sample_elem['href']
    
    hemisphere['title'] = browser.find_by_css('h2.title').text
    
    hemisphere_image_urls.append(hemisphere)
    
    browser.back()


# In[10]:


hemisphere_image_urls


# In[11]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[8]:


# 5. Quit the browser
browser.quit()


# In[ ]:




