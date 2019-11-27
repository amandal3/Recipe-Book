import requests
import time
from bs4 import BeautifulSoup
from lxml import html
import urllib.parse
import urllib.request
import re

# Obtain Top Loaded Results from Site in Search Page
def list_allRecipes():
    
    url = "https://allrecipes.com/search/results/"
    req = urllib.request.Request(url)
    html_content = urllib.request.urlopen(req).read()
    
    soup = BeautifulSoup(html_content, 'lxml')
    search_data = []
    articles = soup.findAll("article", {"class": "fixed-recipe-card"})
    
    iterarticles = iter(articles)

    for article in iterarticles:
        data = {}
        try:
            data["name"] = article.find("h3", {"class": "fixed-recipe-card__h3"}).get_text().strip(' \t\n\r')
            data["description"] = article.find("div", {"class": "fixed-recipe-card__description"}).get_text().strip(' \t\n\r')
            data["url"] = article.find("a", href=re.compile('^https://www.allrecipes.com/recipe/'))['href']
        except Exception as e2:
            pass

        if data:
            search_data.append(data)
        
    return search_data


def listToString(s):
    str1 = " " 
    return (str1.join(s)) 

# Extract Information from all the Recipes
def allRecipes_Info(url):
    
    pageContent = requests.get(url)
    tree = html.fromstring(pageContent.content)
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    
    # Ratings:
    try:
        rating = float(soup.find("div", {"class": "rating-stars"})["data-ratingstars"])
    except TypeError:
        ratingT = listToString(tree.xpath('/html/body/div[1]/div/main/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/a[1]/span[1]/text()'))
        temp = ratingT.split()
        rating = float(temp[1])
    except ValueError:
        rating = None
    
    # Recipe Name:
    name = listToString(tree.xpath('/html/body/div[1]/div/main/div[1]/div[2]/div[1]/div[1]/div[1]/div/h1/text()'))
    if not name:
        name = listToString(tree.xpath('/html/body/div[1]/div[2]/div/div[3]/section/div[1]/div/section[2]/h1/text()'))
    
    # Serving Size:
    serve = listToString(tree.xpath('//*[@id="recipe-body"]/section[1]/div/div[2]/text()'))
    if not serve:
        serve = listToString(tree.xpath('/html/body/div[1]/div[2]/div/div[3]/section/section[1]/section/div[1]/text()'))
    
    # Total Time:
    t1 = listToString(tree.xpath('/html/body/div[1]/div/main/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div/aside/section/div[1]/div[3]/div[2]/text()'))
    time = "".join(t1.split())
    if not time: 
        time = listToString(tree.xpath('/html/body/div[1]/div[2]/div/div[3]/section/section[1]/span/span/span[1]/text()'))

    # Array of ingredients
    ingredients = []
    iList = soup.find_all(attrs={"class": "recipe-ingred_txt added"})
    for i in iList:
        element = i.string
        ingredients.append(element)
    if not ingredients:
        base = soup.findAll("li", {"class": "ingredients-item"})
        iterbase = iter(base)

        for base in iterbase:
            iList2 = base.find('span', {"class": "ingredients-item-name"}).get_text().strip(' \t\n\r')
            if iList2:
                ingredients.append(iList2)

    # Array of directions
    directions = []
    dList = soup.find_all(attrs={"class": "recipe-directions__list--item"})
    for i in dList:
        direc = i.string
        if(direc != None):
            if(direc.index('\n') != -1):
                directions.append(direc[:direc.index('\n')])
            else:
                directions.append(direc)
    if not directions:
        bse = soup.select('div[class= "section-body"]>p')

        for s in bse:
            step = s.get_text()
            if step:
                directions.append(step)
        
    # Concatenate the accumulated information
    text = {
        'Recipe Name':  name,
        'Rating': rating,
        'Serves': serve,
        'Total Time': time,
        'Ingredients': ingredients,
        'Directions': directions,
    } 

    return text


# Store will hold all the recipes(array of dictionaries)
store = list_allRecipes()

# Obtain url from each recipe in array store(extracting value of key 'url')
# Then use the url grabbed and fetch Recipe info using allRecipes_Info(url) function
link = []
for i in store: 
    temp = i.get('url')
    link.append(temp)
for j in link:
    output = allRecipes_Info(j)
    print(output, end='\n\n')
