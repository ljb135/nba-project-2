import urllib.request
from urllib.error import HTTPError
import gzip
import json
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey

db = create_engine('sqlite:///NBAPlayers.db', echo=True)
meta = MetaData()

players2 = Table('players2', meta,
                 Column('NAME', String),
                 Column('PLAYER_ID', String, primary_key=True),
                 Column('TEAM_ABR', String),
                 Column('TEAM_ID', String),
                 Column('YEAR', String, primary_key=True),
                 Column('AGE', Integer),
                 Column('HEIGHT', Integer),
                 Column('WEIGHT', Integer),
                 Column('GP', Integer),
                 Column('MIN', Integer),
                 Column('PTS', Integer),
                 Column('FTM', Integer),
                 Column('FTA', Integer),
                 Column('FT_PCT', Integer),
                 Column('FGM', Integer),
                 Column('FGA', Integer),
                 Column('FG_PCT', Integer),
                 Column('FG3M', Integer),
                 Column('FG3A', Integer),
                 Column('FG3_PCT', Integer),
                 Column('AST', Integer),
                 Column('TOV', Integer),
                 Column('STL', Integer),
                 Column('BLK', Integer),
                 Column('OREB', Integer),
                 Column('DREB', Integer),
                 Column('PF', Integer),
                 Column('OFF_RTG', Integer),
                 Column('DEF_RTG', Integer),
                 Column('DEFL', Integer),
                 Column('LB_REC', Integer),
                 Column('CONT_2P', Integer),
                 Column('CONT_3P', Integer),
                 Column('DFG2M', Integer),
                 Column('DFG2A', Integer),
                 Column('DFG3M', Integer),
                 Column('DFG3A', Integer))


# meta.create_all(db)

# teams = Table('teams', meta,
#                 Column('TEAM_ID', String),
#                 Column('TEAM_NAME', String),
#                 Column('FROM_YEAR', String),
#                 Column('TO_YEAR', String))
# meta.create_all(db)


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
        if player[stat_indexes["PLAYER_NAME"]] is None or player[stat_indexes["MIN"]] * player[stat_indexes["GP"]] < 100:
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
                   'DREB_PCT', 'REB_PCT', 'TM_TOV_PCT', 'EFG_PCT', 'TS_PCT', 'USG_PCT', 'PACE', 'PIE', 'POSS'}

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

    stat_fields = {'PLAYER_ID', 'PTS_OFF_TOV', 'PTS_2ND_CHANCE', 'PTS_FB', 'PTS_PAINT', 'OPP_PTS_OFF_TOV',
                   'OPP_PTS_2ND_CHANCE', 'OPP_PTS_FB', 'OPP_PTS_PAINT'}

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

    season_stats_url = f"https://stats.nba.com/stats/leagueplayerondetails?College=&Conference=&Country=&DateFrom" \
                       f"=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0" \
                       f"&LeagueID=00&Location=&MeasureType=Opponent&Month=0&OpponentTeamID=0&Outcome=&PORound=0" \
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

    stat_fields = {"VS_PLAYER_ID", 'OPP_FGM', 'OPP_FGA', 'OPP_FG_PCT', 'OPP_FG3M', 'OPP_FG3A', 'OPP_FG3_PCT'}

    headers = json_file["resultSets"][0]["headers"]
    stat_indexes = {stat: index for index, stat in enumerate(headers) if stat in stat_fields}

    for player in json_file["resultSets"][0]["rowSet"]:
        if player[stat_indexes['VS_PLAYER_ID']] is None:
            continue
        player_id = player[stat_indexes["VS_PLAYER_ID"]]
        try:
            season_stats[player_id].extend([player[i] for i in list(stat_indexes.values())[1:]])
        except Exception:
            if player_id in season_stats:
                del season_stats[player_id]

    return season_stats

test_keys = ['SEASON', 'PLAYER_ID', 'PLAYER_NAME', 'TEAM_ID', 'TEAM_ABBREVIATION', 'AGE', 'GP', 'MIN', 'FGM', 'FGA',
                   'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'TOV',
                   'STL', 'BLK', 'PF', 'PFD', 'PTS', 'PLUS_MINUS', 'PLAYER_HEIGHT_INCHES', 'PLAYER_WEIGHT', 'DRAFT_YEAR', 'DRAFT_ROUND', 'DRAFT_NUMBER',
             'OFF_RATING', 'DEF_RATING', 'NET_RATING', 'AST_PCT', 'AST_TO', 'AST_RATIO', 'OREB_PCT',
             'DREB_PCT', 'REB_PCT', 'TM_TOV_PCT', 'EFG_PCT', 'TS_PCT', 'USG_PCT', 'PACE', 'PIE', 'POSS',
             'DEFLECTIONS', 'CHARGES_DRAWN', 'SCREEN_ASSISTS', 'PTS_OFF_TOV', 'PTS_2ND_CHANCE', 'PTS_FB', 'PTS_PAINT', 'OPP_PTS_OFF_TOV',
                   'OPP_PTS_2ND_CHANCE', 'OPP_PTS_FB', 'OPP_PTS_PAINT', 'OPP_FGM', 'OPP_FGA', 'OPP_FG_PCT', 'OPP_FG3M', 'OPP_FG3A', 'OPP_FG3_PCT']

player_stats = get_seasonal_stats(2022)
print(len(player_stats[203932]))
print(dict(zip(test_keys, player_stats[203932])))

# for year in range(2022, 2023):
#     print(f"starting {year}")
#     player_stats = get_seasonal_stats(year)
#     for player in player_stats:
#         stats = player_stats[player]
#         if len(stats) == 37:
#             query = players2.insert().values(
#                 NAME=stats[2],
#                 PLAYER_ID=stats[1],
#                 TEAM_ABR=stats[4],
#                 TEAM_ID=stats[3],
#                 YEAR=stats[0],
#                 AGE=stats[5],
#                 HEIGHT=stats[25],
#                 WEIGHT=stats[26],
#                 GP=stats[6],
#                 MIN=stats[7],
#                 PTS=stats[24],
#                 FTM=stats[14],
#                 FTA=stats[15],
#                 FT_PCT=stats[16],
#                 FGM=stats[8],
#                 FGA=stats[9],
#                 FG_PCT=stats[10],
#                 FG3M=stats[11],
#                 FG3A=stats[12],
#                 FG3_PCT=stats[13],
#                 AST=stats[19],
#                 TOV=stats[20],
#                 STL=stats[21],
#                 BLK=stats[22],
#                 OREB=stats[17],
#                 DREB=stats[18],
#                 PF=stats[23],
#                 OFF_RTG=stats[27],
#                 DEF_RTG=stats[28],
#                 DEFL=stats[29],
#                 LB_REC=stats[30],
#                 CONT_2P=stats[31],
#                 CONT_3P=stats[32],
#                 DFG2M=stats[33],
#                 DFG2A=stats[34],
#                 DFG3M=stats[35],
#                 DFG3A=stats[36])
#             print("running query")
#             conn = db.connect()
#             result = conn.execute(query)
