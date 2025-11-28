# Get Strength of Schedule
def sos_scrape(year):

    # Import libraries
    import requests
    from bs4 import BeautifulSoup 
    import pandas as pd
    
    
    # Create an URL object
    url = f"https://www.teamrankings.com/nfl/ranking/schedule-strength-by-other?date={year}-02-01"
    
    # Create object page
    page = requests.get(url)
    
    
    # Obtain page's information
    soup = BeautifulSoup(page.text, 'lxml')
    
    
    table = soup.find_all('table')
    df = pd.read_html(str(table))[0]
    df['Year'] = str(year)
    
    
    return df
    
    
    



############
