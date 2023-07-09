import urllib.request
import gzip
import json
from sqlalchemy import create_engine
from players_schema import Players_Table
from sqlalchemy.ext.declarative import declarative_base

db = create_engine('sqlite:///NBAPlayers.db', echo=True)
players_table = Players_Table.__table__
# players_table.create(db)

def get_seasonal_stats(season):
    season_stats = {}

    param = f"{season - 1}-{str((season) % 100).zfill(2)}"
    season_stats_url = f"https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom" \
                       f"=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0" \
                       f"&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0" \
                       f"&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N" \
                       f"&Season={param}&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench" \
                       f"=&TeamID=0&TwoWay=0&VsConference=&VsDivision=&Weight="
    season_stats_headers = {"Host": "stats.nba.com", "Connection": "keep-alive",
                            "Accept": "application/json, text/plain, */*", "x-nba-stats-origin": "stats",
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
                            "Referer": "https://stats.nba.com/players/traditional/?sort=PTS&dir=-1",
                            "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9"}

    req = urllib.request.Request(url=season_stats_url, headers=season_stats_headers)
    response = urllib.request.urlopen(req)
    data = response.read()
    data = str(gzip.decompress(data), 'utf-8')
    json_file = json.loads(data)

    stat_fields = {'PLAYER_ID', 'PLAYER_NAME', 'TEAM_ID', 'TEAM_ABBREVIATION', 'AGE', 'GP', 'MIN', 'FGM', 'FGA',
                   'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'TOV',
                   'STL', 'BLK', 'PF', 'PFD', 'PTS', 'PLUS_MINUS'}

    headers = json_file["resultSets"][0]["headers"]
    stat_indexes = {stat: index for index, stat in enumerate(headers) if stat in stat_fields}

    for player in json_file["resultSets"][0]["rowSet"]:
        if player[stat_indexes["PLAYER_NAME"]] is None or player[stat_indexes["MIN"]] < 8 or player[stat_indexes["MIN"]] * player[stat_indexes["GP"]] < 100:
            continue
        player_id = player[stat_indexes["PLAYER_ID"]]
        season_stats[player_id] = [str(season)] + [player[i] for i in list(stat_indexes.values())]

    season_stats_url = f"https://stats.nba.com/stats/leaguedashplayerbiostats?College=&Conference=&Country=&DateFrom" \
                       f"=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0" \
                       f"&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PerMode=PerGame&Period=0" \
                       f"&PlayerExperience=&PlayerPosition=&Season=" \
                       f"{param}&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0" \
                       f"&VsConference=&VsDivision=&Weight="
    season_stats_headers = {"Host": "stats.nba.com", "Connection": "keep-alive",
                            "Accept": "application/json, text/plain, */*", "x-nba-stats-origin": "stats",
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
                            "Referer": "https://stats.nba.com/players/traditional/?sort=PTS&dir=-1",
                            "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9"}

    req = urllib.request.Request(url=season_stats_url, headers=season_stats_headers)
    response = urllib.request.urlopen(req)
    data = response.read()
    data = str(gzip.decompress(data), 'utf-8')
    json_file = json.loads(data)

    stat_fields = {'PLAYER_ID', 'PLAYER_HEIGHT_INCHES', 'PLAYER_WEIGHT', 'DRAFT_YEAR', 'DRAFT_ROUND', 'DRAFT_NUMBER'}

    headers = json_file["resultSets"][0]["headers"]
    stat_indexes = {stat: index for index, stat in enumerate(headers) if stat in stat_fields}

    for player in json_file["resultSets"][0]["rowSet"]:
        if player[stat_indexes['PLAYER_ID']] is None:
            continue
        player_id = player[stat_indexes["PLAYER_ID"]]
        try:
            season_stats[player_id].extend([player[i] for i in list(stat_indexes.values())[1:]])
        except Exception:
            if player_id in season_stats:
                del season_stats[player_id]

    season_stats_url = f"https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom" \
                       f"=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0" \
                       f"&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0" \
                       f"&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N" \
                       f"&Season={param}&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench" \
                       f"=&TeamID=0&TwoWay=0&VsConference=&VsDivision=&Weight="
    season_stats_headers = {"Host": "stats.nba.com", "Connection": "keep-alive",
                            "Accept": "application/json, text/plain, */*", "x-nba-stats-origin": "stats",
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
                            "Referer": "https://stats.nba.com/players/traditional/?sort=PTS&dir=-1",
                            "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9"}

    req = urllib.request.Request(url=season_stats_url, headers=season_stats_headers)
    response = urllib.request.urlopen(req)
    data = response.read()
    data = str(gzip.decompress(data), 'utf-8')
    json_file = json.loads(data)

    stat_fields = {'PLAYER_ID', 'OFF_RATING', 'DEF_RATING', 'NET_RATING', 'AST_PCT', 'AST_TO', 'AST_RATIO', 'OREB_PCT',
                   'DREB_PCT', 'REB_PCT', 'EFG_PCT', 'TS_PCT', 'USG_PCT', 'PACE', 'PIE', 'POSS'}

    headers = json_file["resultSets"][0]["headers"]
    stat_indexes = {stat: index for index, stat in enumerate(headers) if stat in stat_fields}

    for player in json_file["resultSets"][0]["rowSet"]:
        if player[stat_indexes['PLAYER_ID']] is None:
            continue
        player_id = player[stat_indexes["PLAYER_ID"]]
        try:
            season_stats[player_id].extend([player[i] for i in list(stat_indexes.values())[1:]])
        except Exception:
            if player_id in season_stats:
                del season_stats[player_id]

    season_stats_url = f"https://stats.nba.com/stats/leaguehustlestatsplayer?College=&Conference=&Country=&DateFrom" \
                       f"=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0" \
                       f"&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0" \
                       f"&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N" \
                       f"&Season={param}&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench" \
                       f"=&TeamID=0&TwoWay=0&VsConference=&VsDivision=&Weight="
    season_stats_headers = {"Host": "stats.nba.com", "Connection": "keep-alive",
                            "Accept": "application/json, text/plain, */*", "x-nba-stats-origin": "stats",
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
                            "Referer": "https://stats.nba.com/players/traditional/?sort=PTS&dir=-1",
                            "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9"}

    req = urllib.request.Request(url=season_stats_url, headers=season_stats_headers)
    response = urllib.request.urlopen(req)
    data = response.read()
    data = str(gzip.decompress(data), 'utf-8')
    json_file = json.loads(data)

    stat_fields = {'PLAYER_ID', 'DEFLECTIONS', 'CHARGES_DRAWN', 'SCREEN_ASSISTS'}

    headers = json_file["resultSets"][0]["headers"]
    stat_indexes = {stat: index for index, stat in enumerate(headers) if stat in stat_fields}

    for player in json_file["resultSets"][0]["rowSet"]:
        if player[stat_indexes['PLAYER_ID']] is None:
            continue
        player_id = player[stat_indexes["PLAYER_ID"]]
        try:
            season_stats[player_id].extend([player[i] for i in list(stat_indexes.values())[1:]])
        except Exception:
            if player_id in season_stats:
                del season_stats[player_id]

    season_stats_url = f"https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom" \
                       f"=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0" \
                       f"&LeagueID=00&Location=&MeasureType=Misc&Month=0&OpponentTeamID=0&Outcome=&PORound=0" \
                       f"&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N" \
                       f"&Season={param}&SeasonSegment=&SeasonType=Regular%20Season&ShotClockRange=&StarterBench" \
                       f"=&TeamID=0&VsConference=&VsDivision=&Weight="
    season_stats_headers = {"Host": "stats.nba.com", "Connection": "keep-alive",
                            "Accept": "application/json, text/plain, */*", "x-nba-stats-origin": "stats",
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
                            "Referer": "https://stats.nba.com/players/traditional/?sort=PTS&dir=-1",
                            "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9"}

    req = urllib.request.Request(url=season_stats_url, headers=season_stats_headers)
    response = urllib.request.urlopen(req)
    data = response.read()
    data = str(gzip.decompress(data), 'utf-8')
    json_file = json.loads(data)

    stat_fields = {'PLAYER_ID', 'PTS_OFF_TOV', 'PTS_2ND_CHANCE', 'PTS_FB', 'PTS_PAINT'}

    headers = json_file["resultSets"][0]["headers"]
    stat_indexes = {stat: index for index, stat in enumerate(headers) if stat in stat_fields}

    for player in json_file["resultSets"][0]["rowSet"]:
        if player[stat_indexes['PLAYER_ID']] is None:
            continue
        player_id = player[stat_indexes["PLAYER_ID"]]
        try:
            season_stats[player_id].extend([player[i] for i in list(stat_indexes.values())[1:]])
        except Exception:
            if player_id in season_stats:
                del season_stats[player_id]

    season_stats_url = f"https://stats.nba.com/stats/leaguedashptdefend?College=&Conference=&Country=&DateFrom" \
                       f"=&DateTo=&DefenseCategory=3%20Pointers&Division=&DraftPick=&DraftYear=&GameSegment=&Height" \
                       f"=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PerMode" \
                       f"=PerGame&Period=0&PlayerExperience=&PlayerPosition=&Season=" \
                       f"{param}&SeasonSegment=&SeasonType=Regular%20Season&StarterBench=&TeamID=0&VsConference" \
                       f"=&VsDivision=&Weight="
    season_stats_headers = {"Host": "stats.nba.com", "Connection": "keep-alive",
                            "Accept": "application/json, text/plain, */*", "x-nba-stats-origin": "stats",
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
                            "Referer": "https://stats.nba.com/players/traditional/?sort=PTS&dir=-1",
                            "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9"}

    req = urllib.request.Request(url=season_stats_url, headers=season_stats_headers)
    response = urllib.request.urlopen(req)
    data = response.read()
    data = str(gzip.decompress(data), 'utf-8')
    json_file = json.loads(data)

    stat_fields = {"CLOSE_DEF_PERSON_ID", 'FG3M', 'FG3A', 'FG3_PCT'}

    headers = json_file["resultSets"][0]["headers"]
    stat_indexes = {"D"+stat: index for index, stat in enumerate(headers) if stat in stat_fields}

    for player in json_file["resultSets"][0]["rowSet"]:
        if player[stat_indexes['DCLOSE_DEF_PERSON_ID']] is None:
            continue
        player_id = player[stat_indexes["DCLOSE_DEF_PERSON_ID"]]
        try:
            season_stats[player_id].extend([player[i] for i in list(stat_indexes.values())[1:]])
        except Exception:
            if player_id in season_stats:
                del season_stats[player_id]

    season_stats_url = f"https://stats.nba.com/stats/leaguedashptdefend?College=&Conference=&Country=&DateFrom" \
                       f"=&DateTo=&DefenseCategory=2%20Pointers&Division=&DraftPick=&DraftYear=&GameSegment=&Height" \
                       f"=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PerMode" \
                       f"=PerGame&Period=0&PlayerExperience=&PlayerPosition=&Season=" \
                       f"{param}&SeasonSegment=&SeasonType=Regular%20Season&StarterBench=&TeamID=0&VsConference" \
                       f"=&VsDivision=&Weight="
    season_stats_headers = {"Host": "stats.nba.com", "Connection": "keep-alive",
                            "Accept": "application/json, text/plain, */*", "x-nba-stats-origin": "stats",
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
                            "Referer": "https://stats.nba.com/players/traditional/?sort=PTS&dir=-1",
                            "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9"}

    req = urllib.request.Request(url=season_stats_url, headers=season_stats_headers)
    response = urllib.request.urlopen(req)
    data = response.read()
    data = str(gzip.decompress(data), 'utf-8')
    json_file = json.loads(data)

    stat_fields = {"CLOSE_DEF_PERSON_ID", 'FG2M', 'FG2A', 'FG2_PCT'}

    headers = json_file["resultSets"][0]["headers"]
    stat_indexes = {"D" + stat: index for index, stat in enumerate(headers) if stat in stat_fields}

    for player in json_file["resultSets"][0]["rowSet"]:
        if player[stat_indexes['DCLOSE_DEF_PERSON_ID']] is None:
            continue
        player_id = player[stat_indexes["DCLOSE_DEF_PERSON_ID"]]
        try:
            season_stats[player_id].extend([player[i] for i in list(stat_indexes.values())[1:]])
        except Exception:
            if player_id in season_stats:
                del season_stats[player_id]

    return season_stats


stat_names = ['SEASON', 'PLAYER_ID', 'PLAYER_NAME', 'TEAM_ID', 'TEAM_ABBREVIATION', 'AGE', 'GP', 'MIN', 'FGM', 'FGA',
              'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'TOV',
              'STL', 'BLK', 'PF', 'PFD', 'PTS', 'PLUS_MINUS', 'PLAYER_HEIGHT_INCHES', 'PLAYER_WEIGHT', 'DRAFT_YEAR',
              'DRAFT_ROUND', 'DRAFT_NUMBER',
              'OFF_RATING', 'DEF_RATING', 'NET_RATING', 'AST_PCT', 'AST_TO', 'AST_RATIO', 'OREB_PCT',
              'DREB_PCT', 'REB_PCT', 'EFG_PCT', 'TS_PCT', 'USG_PCT', 'PACE', 'PIE', 'POSS',
              'DEFLECTIONS', 'CHARGES_DRAWN', 'SCREEN_ASSISTS', 'PTS_OFF_TOV', 'PTS_2ND_CHANCE', 'PTS_FB', 'PTS_PAINT',
              'DFG3M', 'DFG3A', 'DFG3_PCT', 'DFG2M', 'DFG2A', 'DFG2_PCT']

# player_stats = get_seasonal_stats(2023)
# print(len(player_stats[203932]))
# print(dict(zip(stat_names, player_stats[203932])))

for year in range(2023, 2024):
    print(f"starting {year}")
    player_stats = get_seasonal_stats(year)
    for player in player_stats:
        stats = dict(zip(stat_names, player_stats[player]))
        if len(stats) == 61:
            query = players_table.insert().values(
            # query = players_table.update().where(
            #     (players_table.c.PLAYER_ID == stats['PLAYER_ID']) &
            #     (players_table.c.SEASON == stats['SEASON'])
            # ).values(
                PLAYER_NAME=stats['PLAYER_NAME'],
                PLAYER_ID=stats['PLAYER_ID'],
                TEAM_ID=stats['TEAM_ID'],
                TEAM_ABBREVIATION=stats['TEAM_ABBREVIATION'],
                SEASON=stats['SEASON'],
                AGE=stats['AGE'],
                PLAYER_HEIGHT_INCHES=stats['PLAYER_HEIGHT_INCHES'],
                PLAYER_WEIGHT=stats['PLAYER_WEIGHT'],
                DRAFT_YEAR=stats['DRAFT_YEAR'],
                DRAFT_ROUND=stats['DRAFT_ROUND'],
                DRAFT_NUMBER=stats['DRAFT_NUMBER'],
                GP=stats['GP'],
                MIN=stats['MIN'],
                PTS=stats['PTS'],
                EFG_PCT=stats['EFG_PCT'],
                TS_PCT=stats['TS_PCT'],
                FGM=stats['FGM'],
                FGA=stats['FGA'],
                FG_PCT=stats['FG_PCT'],
                FG3M=stats['FG3M'],
                FG3A=stats['FG3A'],
                FG3_PCT=stats['FG3_PCT'],
                FTM=stats['FTM'],
                FTA=stats['FTA'],
                FT_PCT=stats['FT_PCT'],
                OREB=stats['OREB'],
                DREB=stats['DREB'],
                REB=stats['REB'],
                AST=stats['AST'],
                TOV=stats['TOV'],
                STL=stats['STL'],
                BLK=stats['BLK'],
                PF=stats['PF'],
                PFD=stats['PFD'],
                PLUS_MINUS=stats['PLUS_MINUS'],
                OFF_RATING=stats['OFF_RATING'],
                DEF_RATING=stats['DEF_RATING'],
                NET_RATING=stats['NET_RATING'],
                AST_PCT=stats['AST_PCT'],
                AST_TO=stats['AST_TO'],
                AST_RATIO=stats['AST_RATIO'],
                OREB_PCT=stats['OREB_PCT'],
                DREB_PCT=stats['DREB_PCT'],
                REB_PCT=stats['REB_PCT'],
                USG_PCT=stats['USG_PCT'],
                PACE=stats['PACE'],
                PIE=stats['PIE'],
                POSS=stats['POSS'],
                DEFLECTIONS=stats['DEFLECTIONS'],
                CHARGES_DRAWN=stats['CHARGES_DRAWN'],
                SCREEN_ASSISTS=stats['SCREEN_ASSISTS'],
                PTS_OFF_TOV=stats['PTS_OFF_TOV'],
                PTS_2ND_CHANCE=stats['PTS_2ND_CHANCE'],
                PTS_FB=stats['PTS_FB'],
                PTS_PAINT=stats['PTS_PAINT'],
                DFG3M=stats['DFG3M'],
                DFG3A=stats['DFG3A'],
                DFG3_PCT=stats['DFG3_PCT'],
                DFG2M=stats['DFG2M'],
                DFG2A=stats['DFG2A'],
                DFG2_PCT=stats['DFG2_PCT']
            )
            print("running query")
            conn = db.connect()
            result = conn.execute(query)
