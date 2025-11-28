
def adp_scrape(year):

    # Import libraries
    import requests
    from bs4 import BeautifulSoup 
    import pandas as pd
    
    
    # Create an URL object
    url = f'https://fantasyfootballcalculator.com/adp/ppr/12-team/all/{str(year)}'
    
    # Create object page
    page = requests.get(url)
    
    
    # Obtain page's information
    soup = BeautifulSoup(page.text, 'lxml')
    
    table = soup.find("table", {"class": "table adp"})
    
    
    # Obtain every title of columns with tag <th>
    headers = []
    for i in table.find_all('th'):
     title = i.text
     headers.append(title)
     
    # Create Base DF
     
    mydata = pd.DataFrame(columns = headers)
    
    # Fill Dataframe with Data
    for j in table.find_all('tr')[1:]:
     row_data = j.find_all('td')
     row = [i.text for i in row_data]
     length = len(mydata)
     mydata.loc[length] = row
     
    # Append year to dataframe
    mydata['Year'] = str(url[-4:])
    
    return mydata    




############


