# Recipe-Book
This is my EE551 Engineering Python final project.

## Introduction
The purpose of this project is to have users experience new foods by allowing them to quickly search through a recipe book. The three situations where this program might come useful are: 

1. You open your fridge and you see a few ingredients but you have no idea what to make with them. With this program, the user is able to input their ingredients and have a couple recipes pop up containing these ingredients (and more that may need to be purchased).
    - Search functionality based on ingredients
      - Must include & Must not include(in case of dietary restrictions) options
2. You are invited to a potluck and there is a specific theme (specific culture or holiday) and you don't know what to make. With this program, the user is able to search for recipes based on specific keywords (the holiday or culture).
    - Search functionality based on holiday, culture, type of food (ie. pie, cake, cookies, etc.)
3. You might be adventerous one day and want to test your culinary skills and make something of a specific complexity level. With this program, the user is able to select recipes based on its complexity. 
    - Complexity is calculated based on: 
       - How long it takes to make the dish
       - Number of ingredients needed
       - Number of steps in the recipe
    - Different complexity levels are:
      - Beginner [1]
      - Intermediate [2]
      - Advanced [3]
      - Expert [4]
      - Master [5]

The recipes used will be generated by allrecipes.com


## Requirements: 
`pip3 install beautifulsoup4`
`pip3 install lxml`


### Future Goals
* Populate from foodnetwork.com as well to expand recipe collection
