import requests
from bs4 import BeautifulSoup
import json

# must manually imput start page and end page using pageNumber and end
pageNumber = 1
end = 3
open(r"TesterIndent.json", "r")
dictionary = ''
json_object = ''
dictionaryArray = []
#creates a loop that allows for the scraper to crawl multiple webpages.
while pageNumber < end:
    s = requests.Session()
    # saves url as a variable then adds the page number to the end. 
    url = "https://www.defense.gov/News/Contracts/?Page=" + str(pageNumber)
    print(pageNumber)
    pageNumber = pageNumber + 1
    onlydate = ''
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'html5lib')
    links = []
    # for loop that grabs the 10 relevant links on the webpage and saves them to an array called links
    for i in range(len(soup.find_all('listing-titles-only', attrs={'article-url' : True}))):
        links.append(soup.find_all('listing-titles-only', attrs={'article-url' : True})[i]['article-url'])
    
    # loop that runs 10 times (only 10 links per page maximum)
    for i in range(10):
        #iterates until the end of the "links" array
        webpage = s.get(links[i])
        # creates a new object of just the html from one of the 10 links grabbed earlier.
        soup2 = BeautifulSoup(webpage.text, 'html5lib')
        data = ''
        #grabs the date from the webpage then cleans excess
        header = soup2.find('h1').get_text()
        onlyDate = str(header.replace("            Contracts For ", ''))
        onlyDate = onlyDate.strip()
        # grabs the "body" text from within the links.
        for data in soup2.find_all('p'):
            # converts the data variable into a string then searches each paragraph for the word "awarded", and if it it is included then 
            # it will grab all the characters until the first comma. 
            if 'awarded' in str(data):
                dataInText = data.get_text()
                (dataInText[:dataInText.index(",")])
                # grabs everything before the comma
                companyName = (dataInText[:dataInText.index(",")])
                if 'CORRECTION' in companyName:
                    break;
                try:
                    # finds the index of the first dollar sign 
                    indexOfDollarSign = dataInText.index("$")
                except:
                    break
                award = ''
                # loops and grabs each character.
                for i in range(19): 
                    character = dataInText[indexOfDollarSign + i]
                    # grabs the character then converts it into ASCII 
                    string = str(character)
                    charInt = ord(character)
                    
                    # checks each number one by one to verify they are numbers/commas/dollar sign
                    if ((charInt <= 57) & (charInt >= 48)):
                        award = award + character
                    elif (charInt == 36):
                        award = award + character
                    elif (charInt == 44):
                        award = award + character
                    else:
                        break
                
                # creates a json variable
                dictionary = { "Company Name": companyName }
                
                # creates object with the json variable
                json_object = json.dumps(dictionary, indent = 4)
                dictionaryArray.append(json_object)
                
                
                # writes into json file
listConverter = json.dumps(dictionaryArray, indent = 4)
with open("TesterIndent.json", "w") as outfile:
    outfile.write(listConverter)
