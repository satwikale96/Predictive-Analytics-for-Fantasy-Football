# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 20:01:38 2022

@author: ahaan
"""
###################### TO DO LIST


######################




import pandas as pd
import numpy as np
from adp_scrape import adp_scrape
from sos_scrape import sos_scrape
from new_year_scrape import new_year_scrape
from target_scrape import target_scrape
from age_team_scrape import age_team_scrape

################## Create player stats dataframe of 2020-2019 Data

import glob

# Extract first dataframe to get columns

cols = ['Player', 'Pos', 'Tm', 'PassingYds', 'PassingTD', 'Int', 'PassingAtt', \
       'Cmp', 'RushingAtt', 'RushingYds', 'RushingTD', 'Rec', 'Tgt', \
       'ReceivingYds', 'ReceivingTD', 'FL', 'PPRFantasyPoints',\
       'StandardFantasyPoints', 'HalfPPRFantasyPoints', 'Year', 'Week']

# Year list
year_list = np.arange(2010, 2021, 1)

stats_data = pd.DataFrame(columns=cols)

for year in year_list:
    path = f"fantasy\weekly\{year}\*.csv"
    #print(path)

    for fname in glob.glob(path):        
       # print(fname)
        week = fname.split("week")[2].split('.csv')[0]
        temp_df = pd.read_csv(fname)
        temp_df['Week'] = int(week)
        temp_df['Year'] = int(year)
        
        stats_data = pd.concat([stats_data, temp_df])
        
        
stats_data['Pos'] = stats_data.Pos.str.replace(r'(^.*RB.*$)', 'RB', regex=True)
stats_data['Pos'] = stats_data.Pos.str.replace(r'(^.*HB.*$)', 'RB', regex=True)
stats_data['Pos'] = stats_data.Pos.str.replace(r'(^.*FB.*$)', 'RB', regex=True)
stats_data['Pos'] = stats_data.Pos.str.replace(r'(^.*WR.*$)', 'WR', regex=True)
stats_data['Pos'] = stats_data.Pos.str.replace(r'(^.*TE.*$)', 'TE', regex=True)
stats_data['Pos'] = stats_data.Pos.str.replace(r'(^.*QB.*$)', 'QB', regex=True)

stats_data['Player'] = stats_data['Player'].astype('str')
stats_data['Year'] = stats_data['Year'].astype('str')

def clean_player_name(dataframe, col):
        
    dataframe[col] = dataframe[col].str.replace(' Jr.', '')
    dataframe[col] = dataframe[col].str.replace(' IV', '')
    dataframe[col] = dataframe[col].str.replace(' IIII', '')
    dataframe[col] = dataframe[col].str.replace(' III', '')
    dataframe[col] = dataframe[col].str.replace(' II', '')
    dataframe[col] = dataframe[col].str.replace('A.Â S', '')
    dataframe[col] = dataframe[col].str.replace('E.Â S', '')
    dataframe[col] = dataframe[col].str.replace('St. BrownA. S', 'St. Brown')
    dataframe[col] = dataframe[col].str.replace('St. BrownE. S', 'St. Brown')
    dataframe[col] = dataframe[col].str.replace('Kenny Gainwell','Kenneth Gainwell')
    dataframe[col] = dataframe[col].str.replace('JaMycal Hasty','Jamycal Hasty')
    dataframe[col] = dataframe[col].str.replace('D.J. Chark','DJ Chark')
    dataframe[col] = dataframe[col].str.replace('Nick Westbrook','Nick Westbrook-Ikhine')
    dataframe[col] = dataframe[col].str.replace('Benjamin Snell','Benny Snell')
    dataframe[col] = dataframe[col].str.replace('Ray Ray McCloud','Ray-Ray McCloud')
    dataframe[col] = dataframe[col].str.replace('Khadarel Hodge','KhaDarel Hodge')
    dataframe[col] = dataframe[col].str.replace('John Mundt','Johnny Mundt')
    dataframe[col] = dataframe[col].str.replace('Greg Howell','Buddy Howell')
    dataframe[col] = dataframe[col].str.replace('Lamical Perine',"La'Mical Perine")
    dataframe[col] = dataframe[col].str.replace('Bennett Skowronek','Ben Skowronek')
    dataframe[col] = dataframe[col].str.replace('Jeffery Wilson','Jeff Wilson')
    dataframe[col] = dataframe[col].str.replace('J.J. Arcega-Whiteside','JJ Arcega-Whiteside')
    dataframe[col] = dataframe[col].str.replace('Nate Cottrell','Nathan Cottrell')



    return dataframe


stats_data = clean_player_name(stats_data, 'Player')

original = stats_data.copy()
        
########### Run ADP Scrape for all years

year_list = np.arange(2010, 2022, 1)
        
# Create DF
adp_cols = ['Pick_Number','Name','Team','Year']
adp_data = pd.DataFrame(columns=adp_cols)

# Loop through years
for year in year_list:
    
    temp_df = adp_scrape(year)
    temp_df['Pick_Number'] = temp_df.iloc[:, 0]
    temp_df = temp_df[adp_cols]
    #temp_df = temp_df.rename(columns={'#':'Pick_Number'})
    adp_data = pd.concat([adp_data, temp_df])

    
adp_data = clean_player_name(adp_data, 'Name')
########### Run SOS Scrape for all years
    
# Create DF
sos_cols = ['SOS_Rank', 'Team_short','Year']
sos_data = pd.DataFrame(columns=sos_cols)

# Loop through years
for year in year_list:
    
    temp_df = sos_scrape(year)
    temp_df[['Team_short','Record']] = temp_df['Team'].str.split(' \(', n=1, expand=True)
    temp_df['SOS_Rank'] = temp_df['Rank']
    temp_df = temp_df[sos_cols]
    sos_data = pd.concat([sos_data, temp_df])

    
########## Run New Year's Scape (in this case, 2021)
new_year = 2021
new_year_data = new_year_scrape(new_year)
new_year_data = clean_player_name(new_year_data, 'Player')
#test = new_year_data[new_year_data['Player'].str.contains('Mark Ingram')]
#test = age_team_data[age_team_data['Player'].str.contains('Derek Carr')]
#test = updated_stats_data[updated_stats_data['Player'].str.contains('Derek Carr')]

# Get all teams for mapping
#updated_stats_data['Team_Name'].unique()







########## Run Target Scrape
target_data = target_scrape()
target_data = clean_player_name(target_data, 'Player')



# Merge data together
new_year_full_data = new_year_data.merge(target_data, left_on=['Player','Pos','Week'], right_on=['Player','Pos','Week'], how='left', suffixes=('', '_DROP')).filter(regex='^(?!.*_DROP)')
new_year_full_data = new_year_full_data.drop(['Team_Home', 'Team_Away', 'Team'], axis=1)
new_year_full_data['Tgt'] = new_year_full_data['Tgt'].fillna(value=0)




########### Run age_team_scrape
year_list = np.arange(2010, 2022, 1)
age_team_data = age_team_scrape(year_list)
age_team_data = clean_player_name(age_team_data, 'Player')



######### Update Team Mapping
stats_teams = pd.read_excel('Team_name_mapping.xlsx', sheet_name='STATS')
adp_teams = pd.read_excel('Team_name_mapping.xlsx', sheet_name='ADP')
sos_teams = pd.read_excel('Team_name_mapping.xlsx', sheet_name='SOS')
age_teams = pd.read_excel('Team_name_mapping.xlsx', sheet_name='AGE')


# Fix Mapping
# Stats
#stats_data = stats_data.merge(stats_teams, left_on='Tm', right_on='Old_Team', how='left')
#stats_data = stats_data.drop(columns={'Tm','Old_Team'})

# ADP
adp_data = adp_data.merge(adp_teams, left_on='Team', right_on='Old_Team', how='left')
adp_data = adp_data.drop(columns={'Team','Old_Team'})
adp_data['Name'] = adp_data['Name'].astype('str')
adp_data['Year'] = adp_data['Year'].astype('str')

# SOS
sos_data = sos_data.merge(sos_teams, left_on='Team_short', right_on='Old_Team', how='left')
sos_data = sos_data.drop(columns={'Team_short','Old_Team'})



########## Join Dataframes Together

# Use age_team data to get Team for new_year_data_full
new_year = new_year_full_data.merge(age_team_data, left_on=['Player','Year','Pos'], right_on=['Player','Year','Pos'], how='left', suffixes=('', '_DROP')).filter(regex='^(?!.*_DROP)')

# Rename New Year teams
new_year = new_year.merge(age_teams, left_on='Team_Name', right_on='Old_Team', how='left')
new_year = new_year.drop(columns={'Team_Name_x','Old_Team'})
new_year = new_year.rename(columns={'Team_Name_y':'Team_Name'})

# Use age_team data to get Team for regular stats_data
updated_stats_data = stats_data.merge(age_team_data, left_on=['Player','Year','Pos'], right_on=['Player','Year','Pos'], how='left', suffixes=('', '_DROP')).filter(regex='^(?!.*_DROP)')
updated_stats_data = updated_stats_data.drop('Tm', axis=1)

# Rename New Year teams
updated_stats_data = updated_stats_data.merge(age_teams, left_on='Team_Name', right_on='Old_Team', how='left')
updated_stats_data = updated_stats_data.drop(columns={'Team_Name_x','Old_Team'})
updated_stats_data = updated_stats_data.rename(columns={'Team_Name_y':'Team_Name'})

# Concatenate Updated Stats Data and New Year
all_years_data = pd.concat([updated_stats_data, new_year])

#test = all_years_data[all_years_data['Player'] == 'Derrick Henry']
#test1 = stats_data[stats_data['Player'] == 'Derrick Henry']



##### PLAYERS THAT NEED FIXING NAMING
need_fix = new_year[new_year['Team_Name'].isnull()]['Player'].unique()


##### Clean data
    



# Add Age to Stats_data
#stats_data = stats_data.merge(age_team_data, left_on=['Player','Year','Pos'], right_on=['Player','Year','Pos'], how='left', suffixes=('', '_DROP')).filter(regex='^(?!.*_DROP)')
#test = pd.concat([stats_data, new_year])
#tester = original[original['Player'] == 'Derrick Henry']

####### Join with ADP and SOS data

full_data = all_years_data.merge(adp_data, left_on=['Player','Year','Team_Name'], right_on=['Name','Year','Team_Name'], how='left', suffixes=('', '_DROP')).filter(regex='^(?!.*_DROP)')
full_data = full_data.merge(sos_data, left_on=['Year','Team_Name'], right_on=['Year','Team_Name'], how='left', suffixes=('', '_DROP')).filter(regex='^(?!.*_DROP)')
full_data = full_data.drop('Name', axis=1)

# Group into season_section

full_data['Week'] = full_data['Week'].astype(int)

def f(row):
    if ((row['Week'] >= 1) & (row['Week'] <= 6)):
        return 1
    elif ((row['Week'] >= 7) & (row['Week'] <= 12)):
        return 2
    else:
        return 3


full_data['Season_section'] = full_data.apply(f, axis=1)

# Filter data to only include QB, WR, RB, TE
position_list = ['QB','RB','WR','TE']
full_data = full_data[full_data['Pos'].isin(position_list)]
full_data = full_data.drop(['Unnamed: 0','StandardFantasyPoints','HalfPPRFantasyPoints'], axis=1)


# Save to CSV
full_data.to_csv('fantasy_data.csv')


### Testing
#need_fix.to_csv('fix_names.csv')

#test = stats_data[stats_data['Player'].str.contains('Ronald')]
#last_year = full_data[full_data['Year'] == '2020']
#players_list = stats_data['Player'].unique()
#need_fix_list = [name for name in need_fix if name not in players_list]
# See if in list
#test_name = 'Cottrell'

#stats_data[stats_data['Player'].str.contains(test_name)]['Player'].unique()
#age_team_data[age_team_data['Player'].str.contains(test_name)]['Player'].unique()


















