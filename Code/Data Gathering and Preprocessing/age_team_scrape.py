#import numpy as np  
def age_team_scrape(year_list):
        
    import requests
    from bs4 import BeautifulSoup 
    import pandas as pd
    import numpy as np  
    
    output_df = pd.DataFrame(columns=['Player','Team_Name','Pos','Age','Year'])
    
    
    for year in year_list:
    
    
        url = f'https://www.pro-football-reference.com/years/{year}/fantasy.htm'
        
        
        
        # Create object page
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        page = requests.get(url, headers=headers)
        
        
        # Obtain page's information
        soup = BeautifulSoup(page.text, 'lxml')
        
        
        table = soup.find_all('table')
        df = pd.read_html(str(table))[0]
        
        df = df.droplevel(level=0, axis=1)
        
        df_clean = df[['Player', 'Tm', 'FantPos','Age']]
        df_clean['Player'] = df_clean['Player'].str.replace(r'*', '')
        df_clean['Player'] = df_clean['Player'].str.replace(r'+', '')
        df_clean['Player'] = df_clean['Player'].str.strip()
        df_clean = df_clean.drop(df_clean[df_clean['Player'] == 'Player'].index )
        df_clean = df_clean.rename(columns={'Tm':'Team_Name', 'FantPos':'Pos'})
        
        df_clean['Year'] = str(year)
        
        output_df = pd.concat([output_df, df_clean])
        
    return output_df


#year_list = np.arange(2010, 2022, 1)
#test = team_scrape(year_list)