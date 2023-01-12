# Web-Scraper-Government-Contracts
Takes link from defense.gov and scrapes the contract date, award amount, and company name then adds the information to a json file. 

Change the amount of names scraped by changing the two variables "pageNumber" and "end" to the desired range of pages, if pageNumber = 1 
then it will grab the first 10 links on the first page. It is possible to only grab a certain amount of links within the first page, but
would require editing the argument for the array that the links are added to. 
