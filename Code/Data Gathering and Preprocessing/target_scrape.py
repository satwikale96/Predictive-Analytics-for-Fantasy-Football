
def target_scrape():

    import requests
    from bs4 import BeautifulSoup 
    import pandas as pd
    import numpy as np  
    
    url = 'https://www.fantasypros.com/nfl/reports/targets/'
    
    
    
    # Create object page
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    page = requests.get(url, headers=headers)
    
    
    # Obtain page's information
    soup = BeautifulSoup(page.text, 'lxml')
    
    
    table = soup.find_all('table')
    df = pd.read_html(str(table))[0]
    
    df = df.drop(['TTL','AVG'], axis=1)
    
    
    df_clean = pd.melt(df, id_vars=['Player','Pos','Team'], var_name=['Week'])
    df_clean = df_clean.rename(columns={'value':'Tgt'})
    df_clean['Year'] = '2021'
    
    df_clean = df_clean.drop(df_clean[df_clean['Tgt'] == 'bye'].index )
    
    df_clean['Tgt'] = df_clean.Tgt.str.replace(r'(^.*-.*$)', '0', regex=True)
    
    targets_data = df_clean.copy()
    
    return targets_data
