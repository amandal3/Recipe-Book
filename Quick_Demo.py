import RecipeInit
from RecipeInit import *


'''
TESTING
'''

'''1. Search functionality based on ingredients'''
specifics = {
  "wt": "",       # Query keywords
  "ingIncl": "",  # 'Must be included' ingredient(s) (optional)
  "ingExcl": "",  # 'Must not be included' ingredient(s) (optional)
  "sort": "re"    # Sorting options : 're' for relevance, 'ra' for rating, 'p' for popular (optional)
}
fridge = list_allRecipes(specifics)

for i in fridge:
    print(i, end='\n\n')

'''
2. Search functionality based on holiday, culture, type of food (holiday, culture, type of food).
    If no specifications, it will return standard search/results page
'''
ptlck = {
  "wt": "Christmas",  # Query keywords (optional) 
  "ingIncl": "chicken",  # 'Must be included' ingrdients (optional)
  "ingExcl": "",  # 'Must not be included' ingredients (optional)
  "sort": "re"    # Sorting options : 're' for relevance, 'ra' for rating, 'p' for popular (optional)
}

potluck = list_allRecipes(ptlck)
for i in potluck:
    print(i, end='\n\n')

# Now grab all recipe info from potluck list
link = []
for i in potluck: 
    temp = i.get('url')
    link.append(temp)

for j in link:
    output = allRecipes_Info(j)
    print(output, end='\n\n')


'''
3. More filtering tests:
    * There are two different search constraints and the output will be a compliation of recipes that fall into either search.
    * Will take a while to process bc theres so much information
'''

#Search 1:
qD = {
  "wt": "",  # Query keywords (optional) 
  "ingIncl": "chicken",  # 'Must be included' ingrdients (optional)
  "ingExcl": "pork, ginger",  # 'Must not be included' ingredients (optional)
  "sort": "re"    # Sorting options : 're' for relevance, 'ra' for rating, 'p' for popular (optional)
}

#Search 2:
qD2 = {
  "wt": "cake",  # Query keywords (optional) 
  "ingIncl": "chocolate",  # 'Must be included' ingrdients (optional)
  "ingExcl": "nuts",  # 'Must not be included' ingredients (optional)
  "sort": "re"    # Sorting options : 're' for relevance, 'ra' for rating, 'p' for popular (optional)
}

fullList = list_allRecipes(qD) + list_allRecipes(qD2)
D = []
lst = []

# To obtain all the basic information about the recipes: name, description and URL
for i in fullList:
    Tmp = i.get('url')
    lst.append(Tmp)

# To display details of all the URLs that were detected    
for j in lst:
    Tmp2 = allRecipes_Info(j)
    D.append(Tmp2)

D


'''4. Search for recipes based on complexity'''
specDts = {
    "wt": 'cookie',       # Query keywords
    "ingIncl": 'lemon',  # 'Must be included' ingredient(s) (optional)
    "ingExcl": 'nuts',  # 'Must not be included' ingredient(s) (optional)
    "sort": 're'    # Sorting options : 're' for relevance, 'ra' for rating, 'p' for popular (optional)
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
