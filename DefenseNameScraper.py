import requests
from bs4 import BeautifulSoup
import json

pageNumber = 1
end = 1000
json_object = open(r"Company Name List.json", "a")

while pageNumber < end:
    s = requests.Session()
    url = "https://www.defense.gov/News/Contracts/?Page=" + str(pageNumber)
    pageNumber = pageNumber + 1
    onlydate = ''
    print(url)
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'html5lib')
    links = []
    for i in range(len(soup.find_all('listing-titles-only', attrs={'article-url' : True}))):
        links.append(soup.find_all('listing-titles-only', attrs={'article-url' : True})[i]['article-url'])
        print(links)

    for i in range(10):
        webpage = s.get(links[i])
        soup2 = BeautifulSoup(webpage.text, 'html5lib')
        data = ''
        header = soup2.find('h1').get_text()
        onlyDate = str(header.replace("            Contracts For ", ''))
        onlyDate = onlyDate.strip()
        for data in soup2.find_all('p'):
            if 'awarded' in str(data):
                dataInText = data.get_text()
                (dataInText[:dataInText.index(",")])
                companyName = (dataInText[:dataInText.index(",")])
                if 'CORRECTION' in companyName:
                    break;
                try:
                    indexOfDollarSign = dataInText.index("$")
                except:
                    break
                award = ''
                for i in range(19): 
                    character = dataInText[indexOfDollarSign + i]
                    string = str(character)
                    charInt = ord(character)

                    if ((charInt <= 57) & (charInt >= 48)):
                        award = award + character
                    elif (charInt == 36):
                        award = award + character
                    elif (charInt == 44):
                        award = award + character
                    else:
                        break
                
                dictionary = {
                    "Date": onlyDate,
                    "Company Name": companyName,
                    "Award Amount": award
                }

                json_object = json.dumps(dictionary, indent = 4)

                with open("Company Name List.json", "a") as outfile:
                    outfile.write(json_object)
