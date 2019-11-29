import requests
import time
from bs4 import BeautifulSoup
from lxml import html
import urllib.parse
import urllib.request
import re

# Obtain Top Loaded Results from Site in Search Page
def list_allRecipes(queryDetails):
    
    url = "https://allrecipes.com/search/results/?"
    qURL = urllib.parse.urlencode(queryDetails)
    newURL = url + qURL
    req = urllib.request.Request(newURL)
    content = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(content, 'lxml')    
    
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


# Extract Information from all the Recipes
def listToString(s):
    str1 = " " 
    return (str1.join(s)) 

def allRecipes_Info(url):
    
    pageContent = requests.get(url)
    tree = html.fromstring(pageContent.content)
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    
    # Ratings:
    try:
        rating = round(float(soup.find("div", {"class": "rating-stars"})["data-ratingstars"]),2)
    except TypeError:
        ratingT = listToString(tree.xpath('/html/body/div[1]/div/main/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/a[1]/span[1]/text()'))
        temp = ratingT.split()
        try:
            rating = float(temp[1])
        except IndexError:
            rating = float(temp[0])
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
    
    #Calories Per Serving Size:
    try:
        calories = listToString(tree.xpath('//*[@id="nutrition-button"]/span[1]/span[1]/text()'))+listToString(tree.xpath('//*[@id="nutrition-button"]/span[1]/span[2]/text()'))
        if not calories:
            c=listToString(tree.xpath('/html/body/div[1]/div/main/div[1]/div[2]/div[1]/div[2]/div[2]/section[2]/div/div[2]/text()'))
            calories = c.split()[0] + ' ' + c.split()[1].split(';',1)[0]            
    except IndexError:
        pass
    
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
        'Calories Per Serving': calories,
        'Total Time': time,
        'Ingredients': ingredients,
        'Directions': directions,
        'URL': url
    } 

    return text


'''
* Complexity is on a scale of 5 (type int)
    * Score is pre-determined based off of:
        * time it takes to make the meal  
            * >  4 Hours         (240+ mins)  = 5
            * >  2 Hours 30 Mins (150+ mins)  = 4
            * >  1 Hour 3 Mins   (90+ mins)   = 3
            * >  1 Hour          (60+ mins)   = 2
            * <= 1 Hour          (<= 60 mins) = 1
        * number of ingredients needed for the meal 
            * >  20 ingredients = 5
            * >  15 ingredients = 4
            * >  10 ingredients = 3
            * >  7  ingredients = 2
            * <= 7  ingredients = 1
        * number of steps in the recipe 
            * >  7 steps = 5
            * >  5 steps = 4
            * >  3 steps = 3
            * >  2 steps = 2
            * <= 2 steps = 1
* Give the values of each of the three categories, it will now add them all up and divide by 3. 
  The result will be the complexity of the recipe 
'''

class ComplexLevels:
    def complexity(dictionary):
        for k in dictionary:
            complexityTot = 0

            #Complexity Score for Time
            stringTime = k.get('Total Time')
            if not stringTime:
                pass
            else:
                timeArr = re.split('[H m hr min hrs mins]',stringTime)
                while('' in timeArr) : 
                    timeArr.remove('') 

            if len(timeArr) == 2:
                intTime = int(timeArr[1]) + (int(timeArr[0]) * 60) #convert dem to mins
            elif len(timeArr) == 1:
                #only min
                temp = int(timeArr[0])
                if temp < 9: # just incase a recipe takes exactly 10 hr
                    intTime = 9 * 60 
                else:
                    intTime = int(timeArr[0])

            if intTime > 240: # 4 Hours 
                complexityTot = complexityTot + 5
            elif intTime > 150: # 2 Hours 30 Mins 
                complexityTot = complexityTot + 4
            elif intTime > 90: # 1 Hour 30 Mins 
                complexityTot = complexityTot + 3
            elif intTime > 60: # 1 Hour
                complexityTot = complexityTot + 2
            else:
                complexityTot = complexityTot + 1

            # Complexity Score for Ingredients
            ingredientArr = k.get('Ingredients')
            if len(ingredientArr) > 20:
                complexityTot = complexityTot + 5
            elif len(ingredientArr) > 15:
                complexityTot = complexityTot + 4
            elif len(ingredientArr) > 10:
                complexityTot = complexityTot + 3
            elif len(ingredientArr) > 7:
                complexityTot = complexityTot + 2
            else:
                complexityTot = complexityTot + 1

            # Complexity Score for Steps 
            stepsArr = k.get('Directions')
            if len(stepsArr) == 0:
                url = k.get('URL')
                urlSearch = allRecipes_Info(url)
                stepsArr = urlSearch['Directions']

            if len(stepsArr) > 7:
                complexityTot = complexityTot + 5
            elif len(stepsArr) > 5:
                complexityTot = complexityTot + 4
            elif len(stepsArr) > 3:
                complexityTot = complexityTot + 3
            elif len(stepsArr) > 2:
                complexityTot = complexityTot + 2
            else:
                complexityTot = complexityTot + 1

            trueComplexity = round(complexityTot/3) #roundsUp
            k['Complexity'] = trueComplexity

        return dictionary

#Uses Class Complex Levels to allow users to search for recipes based on its complexity
def complexitySearch(D):
    x = ComplexLevels
    
    print("What complexity would you like your recipe to be?\nPress [1]Beginner [2]Intermediate [3]Advanced [4]Expert [5]Master")
    user = input("\nEnter a number from 1-5: ")
    level = int(user)
    
    lib = []
    if level == 1: 
        for i in x.complexity(D):
            a = i.get('Complexity')
            if a == 1:
                lib.append(i)
    elif level == 2:
        for i in x.complexity(D):
            a = i.get('Complexity')
            if a == 2:
                lib.append(i)
    elif level == 3:
        for i in x.complexity(D):
            a = i.get('Complexity')
            if a == 3:
                lib.append(i)
    elif level == 4:
        for i in x.complexity(D):
            a = i.get('Complexity')
            if a == 4:
                lib.append(i)
    elif level == 5:
        for i in x.complexity(D):
            a = i.get('Complexity')
            if a == 5:
                lib.append(i)  

    return lib

#Class for functions within the main menu
class MainMenu:
    def __init__(self):
        print("Enter the number of one of the menu choices:")
        print("  >>> 1: Search for recipes based on ingredients")
        print("  >>> 2. Search for recipes based on keywords(ie. Christmas, cake, Chinese)")
        print("  >>> 3. Search for recipes based on keywords and ingredients")
        print("  >>> 4. Search for recipes based on complexity")
        print("  >>> 5. Exit program\n")
        
        self.choice = input("Your choice: ")
    
    #Option One: "Search for a recipes based on ingredients"
    def optionOne(self):
        if self.choice != '1':
            return 0
        
        while True:
            print("Query:\nIf you wish to leave a specific section blank, press enter")

            include = input(" >> Enter your must be included ingredient(s): ")
            dontInclude = input(" >> Enter ingredient(s) you do not want to be included: ")
            sort = input(" >> Sorting options: 're' for relevance, 'ra' for rating, 'p' for popular\n\n")

            if not sort:
                sort = 're'

            specifics = {
              "wt": '',       # Query keywords
              "ingIncl": include,  # 'Must be included' ingredient(s) (optional)
              "ingExcl": dontInclude,  # 'Must not be included' ingredient(s) (optional)
              "sort": sort    # Sorting options : 're' for relevance, 'ra' for rating, 'p' for popular (optional)
            }

            fridge = list_allRecipes(specifics)
            for i in fridge:
                print(i,end='\n\n')
            
            print("Do you want to view a specific recipe?")
            response = int(input(" >> Enter [1] for Yes [2] for No: "))
            
            if response == 1:
                print("Of the list generated previously, copy the url you desire and enter that below")
                url = input(" >> Paste url please: ")
                print("\n")
                hp = allRecipes_Info(url)
                for j in hp:
                    hyperlink = print(j, hp[j], '\n')
            else:
                hyperlink = print("Goodbye. Happy Cooking.")
            
            return hyperlink
    
    #Option Two: "Search for a recipes based on keywords"
    def optionTwo(self):
        if self.choice != '2':
            return 0
        
        while True:
            print("Query:\nIf you wish to leave a specific section blank, press enter")

            keywords = input(" >> Enter keywords you want to search by: ")
            sort = input(" >> Sorting options: 're' for relevance, 'ra' for rating, 'p' for popular\n\n")

            if not sort:
                sort = 're'

            specs = {
              "wt": keywords,       # Query keywords
              "ingIncl": '',  # 'Must be included' ingredient(s) (optional)
              "ingExcl": '',  # 'Must not be included' ingredient(s) (optional)
              "sort": sort    # Sorting options : 're' for relevance, 'ra' for rating, 'p' for popular (optional)
            }

            allR = list_allRecipes(specs)
            for i in allR:
                print(i,end='\n\n')
            
            print("Do you want to view a specific recipe?")
            response = int(input(" >> Enter [1] for Yes [2] for No: "))
            
            if response == 1:
                print("Of the list generated previously, copy the url you desire and enter that below")
                url = input(" >> Paste url please: ")
                print("\n")
                hp = allRecipes_Info(url)
                for j in hp:
                    hyperlink = print(j, hp[j], '\n')
            else:
                hyperlink = print("Goodbye. Happy Cooking.")
            
            return hyperlink                
    
    #Option Three: "Search for a recipes based on keywords and ingredients"
    def optionThree(self):
        if self.choice != '3':
            return 0
        
        while True:
            print("Query:\nIf you wish to leave a specific section blank, press enter")
            
            keywords = input(" >> Enter keywords you want to search by:")
            include = input(" >> Enter your must be included ingredient(s): ")
            dontInclude = input(" >> Enter ingredient(s) you do not want to be included:")
            sort = input(" >> Sorting options: 're' for relevance, 'ra' for rating, 'p' for popular\n\n")

            if not sort:
                sort = 're'

            specD = {
              "wt": keywords,       # Query keywords
              "ingIncl": include,  # 'Must be included' ingredient(s) (optional)
              "ingExcl": dontInclude,  # 'Must not be included' ingredient(s) (optional)
              "sort": sort    # Sorting options : 're' for relevance, 'ra' for rating, 'p' for popular (optional)
            }

            fridgeR = list_allRecipes(specD)
            for i in fridgeR:
                print(i,end='\n\n')
            
            print("Do you want to view a specific recipe?")
            response = int(input(" >> Enter [1] for Yes [2] for No: "))
            
            if response == 1:
                print("Of the list generated previously, copy the url you desire and enter that below")
                url = input(" >> Paste url please: ")
                print("\n")
                hp = allRecipes_Info(url)
                for j in hp:
                    hyperlink = print(j, hp[j], '\n')
            else:
                hyperlink = print("Goodbye. Happy Cooking.")
            
            return hyperlink
    
    #Option Four: "Search for a recipes based on complexity level"
    def optionFour(self):
        if self.choice != '4':
            return 0
 
        while True:
                print("Query:\nIf you wish to leave a specific section blank, press enter")

                keywords = input(" >> Enter keywords you want to search by: ")
                include = input(" >> Enter your must be included ingredient(s): ")
                dontInclude = input(" >> Enter ingredient(s) you do not want to be included: ")
                sort = input(" >> Sorting options: 're' for relevance, 'ra' for rating, 'p' for popular\n\n")

                if not sort:
                    sort = 're'

                specDts = {
                  "wt": keywords,       # Query keywords
                  "ingIncl": include,  # 'Must be included' ingredient(s) (optional)
                  "ingExcl": dontInclude,  # 'Must not be included' ingredient(s) (optional)
                  "sort": sort    # Sorting options : 're' for relevance, 'ra' for rating, 'p' for popular (optional)
                }

                allRs = list_allRecipes(specDts)
                DoR = []
                Lt = []
                for i in allRs:
                    temp = i.get('url')
                    Lt.append(temp)

                for j in Lt:
                    temp2 = allRecipes_Info(j)
                    DoR.append(temp2)

                cS = complexitySearch(DoR)
                for k in cS:
                    cmplxS = print(k, '\n')
                
                return cmplxS

    #Option Five: "Exit Program"
    def optionFive(self):
        if self.choice != '5':
            return 0
        else: return 1
