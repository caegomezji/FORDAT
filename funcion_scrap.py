import requests
import lxml
from bs4 import BeautifulSoup

def news(topic):
    """
    Function that scrapps the title, link and image from the news located at Google news, the idea is to generate html
    with a for cycle and generate one card for each new related with the topic that the user is looking for.

    args:
    Topic, this could be different and will depend by the user


    Outputs:
    Titles -> titles of the news
    News_link -> Links of the news
    Images_link -> Links of the images of each new
    Sources -> The source where every new came from
    """
    #Doing the request
    url = "https://news.google.com/search?q={}&hl=es-419&gl=CO&ceid=CO%3Aes-419".format(topic)
    p12 = requests.get(url)

    #Parsing the information requested
    s = BeautifulSoup(p12.text,'lxml')

    #Getting the articles links

    articles=s.find('div',attrs={'class':'lBwEZb BL5WZb xP6mwf'}).find_all('article') #Getting all the articles
    News_link=[]
    for article in articles:
        link=article.a.get('href')
        News_link.append('https://www.news.google.com'+link.replace('.','',1))

    #Getting the titles
    Titles=[]
    for title in articles:
        Titles.append(title.h3.a.string)

    #Getting the image links
    images=s.find('div',attrs={'class':'lBwEZb BL5WZb xP6mwf'}).find_all('img')
    Images_link = []
    for image in images:
        Images_link.append(image.get('src'))

    #Getting the sources:
    Sources=[]
    for source in articles:
        dirty_font=source.find('div',attrs={'class':'SVJrMe'})
        Sources.append(dirty_font.a.string)

    #Getting the dates:
    Dates=[]
    for date in articles:
        dirty_date=date.find('div',attrs={'class':'SVJrMe'})
        dating= dirty_date.find('time',attrs={'class':'WW6dff uQIVzc Sksgp'})
        if dating: 
            Dates.append(dating.string)
        else:
            Dates.append('date not found')          

    return News_link,Titles,Images_link,Sources,Dates
