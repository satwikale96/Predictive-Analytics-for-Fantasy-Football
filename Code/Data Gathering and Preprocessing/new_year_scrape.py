

def new_year_scrape(year):
    
    # Import libraries
    import requests
    from bs4 import BeautifulSoup 
    import pandas as pd
    import numpy as np  
    
    
    week_list= np.arange(1,19,1)
    position_list = ['QB','RB','WR','TE']
    year = year
    
    output_df = pd.DataFrame(columns=['PPRFantasyPoints', 'PassingAtt', 'Cmp', 'PassingYds', 'PassingTD',\
           'Int', 'RushingAtt', 'RushingYds', 'RushingTD', 'Rec', 'ReceivingYds',\
           'ReceivingTD', 'FL', 'Player', 'Team_Home', 'Team_Away','Year','Week','Pos'])
    
    for week in week_list:
        
        for position in position_list:
    
            # Create an URL object
            url = f"https://www.footballdb.com/fantasy-football/index.html?pos={position}&yr={year}&wk={week}&key=b6406b7aea3872d5bb677f064673c57f"
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            
            # Create object page
            page = requests.get(url, headers=headers)
            
            
            # Obtain page's information
            soup = BeautifulSoup(page.text, 'lxml')
            
            
            table = soup.find_all('table')
            df = pd.read_html(str(table))[0]
            
            df = df.droplevel(level=0, axis=1)
            df = df.drop(['2Pt'], axis=1)
            df = df.iloc[:, :-1]
            
            df.columns = ['Player', 'Game', 'PPRFantasyPoints', 'PassingAtt',  'Cmp', 'PassingYds', 'PassingTD', 'Int', 'RushingAtt', 'RushingYds', 'RushingTD', 'Rec',  'ReceivingYds', 'ReceivingTD', 'FL']
            
            # Fix Columns
            df[['P1','P2']] = df['Player'].str.rsplit('.', n=1, expand=True)
            df['Player_Clean'] = df['P1'].str[:-1]
            
            # Team
            df[['Team_Home','Team_Away']] = df['Game'].str.split('@', n=1, expand=True)
            
            
            # Drop and rename
            df = df.drop(['P1','P2','Player','Game'], axis=1)
            df = df.rename(columns={'Player_Clean':'Player'})
            df['Year'] = '2021'
            df['Week'] = str(week)
            df['Pos'] = str(position)
            
            output_df = pd.concat([output_df, df])
        
    return output_df

test_uno = new_year_scrape(2021)
