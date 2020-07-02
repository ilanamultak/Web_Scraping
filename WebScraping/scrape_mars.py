import pandas as pd
from splinter import Browser 
from bs4 import BeautifulSoup

executable_path = {"executable_path": "chromedriver.exe"}
browser = Browser("chrome", **executable_path, headless=False)

#Nasa Mars News
def mars_news(browser):
    
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    news_title = soup.find("li", class_="slide").find("div", class_="content_title").text
    news_paragraph = soup.find("li", class_="slide").find("div", class_="article_teaser_body").text
    
    print(news_title)
    print(news_paragraph)
    
    return news_title, news_paragraph
    
#JPL Mars Images
def mars_images(browser): 
    
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    featured_img_base = "https://www.jpl.nasa.gov"
    featured_img_url_raw = soup.find("div", class_="carousel_items").find("article")["style"]
    featured_img_url = featured_img_url_raw.split("'")[1]
    featured_img_url = featured_img_base + featured_img_url
    
    return featured_img_url
    
#Mars Facts
def mars_facts(browser):
    facts_url = "https://space-facts.com/mars/"

    mars_facts = pd.read_html(facts_url)
    mars_facts
    mars_df = mars_facts[0]

    mars_df.columns = ["Description", "Value"]

    mars_df.set_index("Description", inplace=True)
    mars_df
    
    html_table = mars_df.to_html()

    html_table.replace("\n", '')

    mars_df.to_html("mars_facts.html")
    
    return mars_df.to_html(classes="table table-striped") 
    
#Mars Hemispheres    
def mars_hemispheres (browser):
     
    base_hemisphere_url = "https://astrogeology.usgs.gov"
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    hemisphere_image_urls = []

    links = soup.find_all("div", class_="item")

    for link in links:
        img_dict = {}
        title = link.find("h3").text
        next_link = link.find("div", class_="description").a["href"]
        full_next_link = base_hemisphere_url + next_link
        
        browser.visit(full_next_link)
        
        pic_html = browser.html
        pic_soup = BeautifulSoup(pic_html, 'html.parser')
        
        url = pic_soup.find("img", class_="wide-image")["src"]

        img_dict["title"] = title
        img_dict["img_url"] = base_hemisphere_url + url
        
        hemisphere_image_urls.append(img_dict)
        
    return hemisphere_image_urls

def scrape_everything():
 
    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)
    featured_img_url = mars_images(browser)
    facts = mars_facts()
    hemisphere_image_urls = mars_hemispheres(browser)
    
    mars_data = {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_image': featured_img_url,
        'facts': facts,
        'hemispheres': hemisphere_image_urls,
        }
    browser.quit()
    return mars_data


if __name__ == "__main__":
    print(scrape_everything())