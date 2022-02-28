# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    news_title, news_paragraph = mars_news(browser)
    img_urls_titles = mars_hemis(browser)

    data = {
        'news_title' : news_title,
        'news_paragraph' : news_paragraph,
        'featured_image' : featured_image(browser),
        'facts' : mars_facts(),
        'hemisphere' : img_urls_titles,
        'last_modified' : dt.datetime.now()
    }
    browser.quit()
    return data    
    
    
def mars_news(browser):  #by adding browser variable, defined outside, we add an argument to the fxn, b/c scraping code utilizes #automated browser
    
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1) # searching for elements with a specific
    #combination of tag (div) and attribute (list_text)
    # wait 1 second before searching components, useful if image heavy.


# HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
# Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
             
    except AttributeError:  #nothing will returned, instead of T and P, if AttributeE occurs.
        return None, None

    return news_title, news_p  #return them FROM the function


# ### Featured Images 

def featured_image(browser):

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
    
    # Add try/except for error handling
    try:
        # Find the relative image url. Point to BS where the image should be instead of grabbing URL directly.
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src') #get pulls the link to the image

    except AttributeError:
        return None
    
    # Use the base URL to create an absolute URL. Use f-string as a cleaner way to print statements and evaluated at run-time.
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
        
    return img_url

def mars_facts():

    try:
      # use 'read_html" to scrape the facts HTML table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
  
    except BaseException:
        return None

   # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True) #setting dxn as index. inplace = True means updated index
    
    return df.to_html(classes="table table-striped") #adding this DF --> HTML code to web app, add bootstrap

    
### hemisphere images

def mars_hemis(browser):
    
    url = 'https://marshemispheres.com/'
    browser.visit(url)


    hemisphere_image_urls = []
    for i in range(4):
    
        hemispheres = {}
    
        browser.find_by_css('a.product-item img')[i].click()
        sample_elem = browser.links.find_by_text('Sample').first
        hemispheres['img_url'] = sample_elem['href']
    
        hemispheres['title'] = browser.find_by_css('h2.title').text
    
        hemisphere_image_urls.append(hemispheres)
    
        browser.back()
    
    return hemisphere_image_urls


if __name__ == "__main__":
    print(scrape_all())
    