# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# set up Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1) # searching for elements with a specific combination of tag (div) and attribute (list_text)
# wait 1 second before searching components, useful if image heavy.


# HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text') # the variable to look for the <div /> tag and its descendent 


# begin scraping. assign the title and summary text to variables. find () within variable.
slide_elem.find('div', class_='content_title')


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images 

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# Find and click the full image button. Full image will be displayed in browser. Full_image_elem to hold scraping result.
# we want our browser to click the 2nd button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# Find the relative image url. Point to BS where the image should be instead of grabbing the URL directly
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')  #get pulls the link to the image
img_url_rel
#code will still pull most recent image.


# Use the base URL to create an absolute URL. Use f-string as a cleaner way to print statements and evaluated at run-time.
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


#galaxyfacts-mars
df = pd.read_html('https://galaxyfacts-mars.com')[0] #new DataFrame from the HTML table #
# read_html() specifically searches for and returns a list of tables found in the HTML, pull only 1st table. Returns table in DF.
df.columns=['description', 'Mars', 'Earth'] #assigns columns to DF
df.set_index('description', inplace=True) #setting dxn as index. inplace = True means updated index will remain in place w/o reassigned DF to new var.
df


df.to_html() #adding this DF --> HTML code to web app



browser.quit()






