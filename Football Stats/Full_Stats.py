from email.mime import base
from numpy import full
import pandas as pd
from pyparsing import col
import requests
import json
from bs4 import BeautifulSoup

base_url = 'https://understat.com/league'
leagues = ['EPL', 'La Liga', 'Bundesliga', 'Serie A', 'Ligue 1', 'RFPL']
seasons = ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021']

full_stats = {}
for l in leagues:
    season_stats = {}
    for s in seasons:
        url = base_url + '/' + l + '/' + s
        res = requests.get(url)
        soup = BeautifulSoup(res.content, "lxml")
        scripts = soup.find_all('script')

        json_obj = ''
        for x in scripts:
            if 'teamsData' in x.text:
                json_obj = x.text.strip()

        istart = json_obj.index("('") + 2
        iend = json_obj.index("')")
        json_data = json_obj[istart:iend].encode('utf8').decode('unicode_escape')

        data = json.loads(json_data)

        teams = {}
        for id in data.keys():
            teams[id] = data[id]['title']

        columns = []
        for id in data.keys():
            columns = list(data[id]['history'][0].keys())
            break

        dataframes = {}
        for id, team in teams.items():
            teams_data = []
            for row in data[id]['history']:
                teams_data.append(list(row.values()))

            df = pd.DataFrame(teams_data, columns=columns)
            dataframes[team] = df

        for team, df in dataframes.items():
            dataframes[team]['ppda_coef'] = dataframes[team]['ppda'].apply(lambda x: x['att']/x['def'] if x['def'] != 0 else 0)
            dataframes[team]['oppda_coef'] = dataframes[team]['ppda_allowed'].apply(lambda x: x['att']/x['def'] if x['def'] != 0 else 0)

        csum = ['xG', 'xGA', 'npxG', 'npxGA', 'deep', 'deep_allowed', 'scored', 'missed', 'xpts', 'wins', 'draws', 'loses', 'pts', 'npxGD']
        cmean = ['ppda_coef', 'oppda_coef']

        frames = []
        for team, df in dataframes.items():
            sum_data = pd.DataFrame(df[csum].sum()).transpose()
            mean_data = pd.DataFrame(df[cmean].mean()).transpose()
            new_df = sum_data.join(mean_data)
            new_df['team'] = team
            new_df['matches'] = len(df)
            frames.append(new_df)
        
        stats = pd.concat(frames)

        stats = stats[['team', 'matches', 'wins', 'draws', 'loses', 'scored', 'missed', 'pts', 'xG', 'npxG', 'xGA', 'npxGA', 'npxGD', 'ppda_coef', 'oppda_coef', 'deep', 'deep_allowed', 'xpts']]
        
        stats.sort_values('pts', ascending=False, inplace=True)
        stats.reset_index(inplace=True, drop=True)
        stats['position'] = range(1, len(stats) + 1)
        stats['xG_diff'] = stats['xG'] - stats['scored']
        stats['xGA_diff'] = stats['xGA'] - stats['missed']
        stats['xpts_diff'] = stats['xpts'] - stats['pts']

        cint = ['wins', 'draws', 'loses', 'scored', 'missed', 'pts', 'deep', 'deep_allowed']
        stats[cint] = stats[cint].astype(int)
        
        col_order = ['position','team', 'matches', 'wins', 'draws', 'loses', 'scored', 'missed', 'pts', 'xG', 'xG_diff', 'npxG', 'xGA', 'xGA_diff', 'npxGA', 'npxGD', 'ppda_coef', 'oppda_coef', 'deep', 'deep_allowed', 'xpts', 'xpts_diff']
        stats = stats[col_order]
        stats = stats.set_index('position')

        season_stats[s] = stats
    
    df_season = pd.concat(season_stats)
    full_stats[l] = df_season

data = pd.concat(full_stats)

data.to_csv('Understat Data.csv')

df = pd.read_csv('Understat Data.csv')
df.rename(columns={'Unnamed: 0': 'league', 'Unnamed: 1': 'season'}, inplace=True)
df.to_csv('Understat Data.csv')