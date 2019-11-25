# Only needs to be run once.
get_ipython().system('pip3 install beautifulsoup4')
get_ipython().system('pip3 install lxml')

import requests
import time
from bs4 import BeautifulSoup
from lxml import html

def generateRecipes_allR():
    # Retrieves the allrecipes.com website
    res = requests.get('https://www.allrecipes.com')

    # Makes the information retrieved readable
    soup = BeautifulSoup(res.text, 'lxml')

    # Select only the a tags that contain the hyperlinks and returns the selected list
    return(soup.select('div[id="insideScroll"] > ul > li > a'))

def generateRecipes_FDNTWK():
    # Retrieves the foodnetwork.com website
    res = requests.get('https://www.foodnetwork.com')

    # Makes the information retrieved readable
    soup = BeautifulSoup(res.text, 'lxml')

    find = soup.select('div[class="o-HeaderFresh__m-PromoList"] >  ul > li > a')[1]
    return find


def listToString(s):
    str1 = " " 
    return (str1.join(s)) 

def recipeInfo(url):

    # Retrive the url and convert to lxml BeautifulSoup
#     soup = BeautifulSoup(requests.get(url).text, "lxml")
    pageContent = requests.get(url)
    tree = html.fromstring(pageContent.content)
    
    name = listToString(tree.xpath('/html/body/div[1]/div[2]/div/div[3]/section/div[1]/div/section[2]/h1/text()'))
    serve = listToString(tree.xpath('/html/body/div[1]/div[2]/div/div[3]/section/section[1]/section/div[1]/text()'))
    time = listToString(tree.xpath('/html/body/div[1]/div[2]/div/div[3]/section/section[1]/span/span/span[1]/text()'))

    ingredients = ''
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    items = soup.find_all(attrs={"class": "recipe-ingred_txt added"})
    # For each element in the list iRaw:
    for i in items:
        # Concatenate newline character and string of i to ingredients
        ingredients += '\n' + i.string

#     Concatenate the accumulated information
    text = 'Recipe Name: ' + name + '\n' +             'Serves: ' + serve + '\n' +             'Time: ' + time + '\n' +             'Ingredients: ' + ingredients + '\n\n';
    print(text)
    return

# Testing:
# recipeInfo('https://www.allrecipes.com/recipe/162760/fluffy-pancakes/')
# recipeInfo('https://www.allrecipes.com/recipe/240702/pine-cone-cheese-ball/')
# recipeInfo('https://www.allrecipes.com/recipe/12682/apple-pie-by-grandma-ople/')





