import urllib.request
import gzip
import json

def get_seasonal_stats(season):
    param = f"{season - 1}-{str((season) % 100).zfill(2)}"

    season_stats_url = f"https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season={param}&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision=&Weight="
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

    season_stats = {}
    headers = json_file["resultSets"][0]["headers"]
    del headers[35:]
    for player in json_file["resultSets"][0]["rowSet"]:
        if player[1] is None:
            continue
        player_name = str(player[1])
        player_stats = {}
        for i in range(len(headers)):
            player_stats[headers[i]] = player[i]
        season_stats[player_name] = player_stats
    print(season_stats)
    # for player in json_file["resultSets"][0]["rowSet"]:
    #     if player[1] is None or player[5] <= 5:
    #         continue
    #     player_name = str(player[1])
    #     del player[30:]
    #     delete_indexes = [6, 7, 8, 21, 26, 28]
    #     for index in sorted(delete_indexes, reverse=True):
    #         del player[index]
    #     player[0] = str(player[0])
    #     player[2] = str(player[2])
    #     season_stats[player_name] = [str(season)] + player
    #
    # season_stats_url = f"https://stats.nba.com/stats/leaguedashplayerbiostats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&Season={param}&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="
    # season_stats_headers = {"Host": "stats.nba.com", "Connection": "keep-alive",
    #                         "Accept": "application/json, text/plain, */*", "x-nba-stats-origin": "stats",
    #                         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
    #                         "Referer": "https://stats.nba.com/players/traditional/?sort=PTS&dir=-1",
    #                         "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9"}
    #
    # req = urllib.request.Request(url=season_stats_url, headers=season_stats_headers)
    # response = urllib.request.urlopen(req)
    # data = response.read()
    # data = str(gzip.decompress(data), 'utf-8')
    # json_file = json.loads(data)
    #
    # for player in json_file["resultSets"][0]["rowSet"]:
    #     if player[1] is None:
    #         continue
    #     player_name = str(player[1])
    #     del player[8:]
    #     del player[0: 6]
    #     try:
    #         player[1] = int(player[1])
    #         season_stats[player_name] = season_stats[player_name] + player
    #     except Exception:
    #         if player_name in season_stats:
    #             del season_stats[player_name]
    #         continue
    #
    # season_stats_url = f"https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season={param}&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision=&Weight="
    # season_stats_headers = {"Host": "stats.nba.com", "Connection": "keep-alive",
    #                         "Accept": "application/json, text/plain, */*", "x-nba-stats-origin": "stats",
    #                         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
    #                         "Referer": "https://stats.nba.com/players/traditional/?sort=PTS&dir=-1",
    #                         "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9"}
    #
    # req = urllib.request.Request(url=season_stats_url, headers=season_stats_headers)
    # response = urllib.request.urlopen(req)
    # data = response.read()
    # data = str(gzip.decompress(data), 'utf-8')
    # json_file = json.loads(data)
    #
    # for player in json_file["resultSets"][0]["rowSet"]:
    #     if player[1] is None:
    #         continue
    #     player_name = str(player[1])
    #     player = [player[11], player[14]]
    #     try:
    #         season_stats[player_name] = season_stats[player_name] + player
    #     except Exception:
    #         if player_name in season_stats:
    #             del season_stats[player_name]
    #         continue
    #
    # season_stats_url = f"https://stats.nba.com/stats/leaguehustlestatsplayer?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season={param}&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision=&Weight="
    # season_stats_headers = {"Host": "stats.nba.com", "Connection": "keep-alive",
    #                         "Accept": "application/json, text/plain, */*", "x-nba-stats-origin": "stats",
    #                         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
    #                         "Referer": "https://stats.nba.com/players/traditional/?sort=PTS&dir=-1",
    #                         "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9"}
    #
    # req = urllib.request.Request(url=season_stats_url, headers=season_stats_headers)
    # response = urllib.request.urlopen(req)
    # data = response.read()
    # data = str(gzip.decompress(data), 'utf-8')
    # json_file = json.loads(data)
    #
    # for player in json_file["resultSets"][0]["rowSet"]:
    #     if player[1] is None:
    #         continue
    #     player_name = str(player[1])
    #     player = [player[10], player[16], player[8], player[9]]
    #     try:
    #         season_stats[player_name] = season_stats[player_name] + player
    #     except Exception:
    #         if player_name in season_stats:
    #             del season_stats[player_name]
    #         continue
    #
    # season_stats_url = f"https://stats.nba.com/stats/leaguedashptdefend?College=&Conference=&Country=&DateFrom=&DateTo=&DefenseCategory=2+Pointers&Division=&DraftPick=&DraftYear=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&Season={param}&SeasonSegment=&SeasonType=Regular+Season&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="
    # season_stats_headers = {"Host": "stats.nba.com", "Connection": "keep-alive",
    #                         "Accept": "application/json, text/plain, */*", "x-nba-stats-origin": "stats",
    #                         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
    #                         "Referer": "https://stats.nba.com/players/traditional/?sort=PTS&dir=-1",
    #                         "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9"}
    #
    # req = urllib.request.Request(url=season_stats_url, headers=season_stats_headers)
    # response = urllib.request.urlopen(req)
    # data = response.read()
    # data = str(gzip.decompress(data), 'utf-8')
    # json_file = json.loads(data)
    #
    # for player in json_file["resultSets"][0]["rowSet"]:
    #     if player[1] is None:
    #         continue
    #     player_name = str(player[1])
    #     player = [player[9], player[10]]
    #     try:
    #         season_stats[player_name] = season_stats[player_name] + player
    #     except Exception:
    #         if player_name in season_stats:
    #             del season_stats[player_name]
    #         continue
    #
    # season_stats_url = f"https://stats.nba.com/stats/leaguedashptdefend?College=&Conference=&Country=&DateFrom=&DateTo=&DefenseCategory=3+Pointers&Division=&DraftPick=&DraftYear=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&Season={param}&SeasonSegment=&SeasonType=Regular+Season&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="
    # season_stats_headers = {"Host": "stats.nba.com", "Connection": "keep-alive",
    #                         "Accept": "application/json, text/plain, */*", "x-nba-stats-origin": "stats",
    #                         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
    #                         "Referer": "https://stats.nba.com/players/traditional/?sort=PTS&dir=-1",
    #                         "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9"}
    #
    # req = urllib.request.Request(url=season_stats_url, headers=season_stats_headers)
    # response = urllib.request.urlopen(req)
    # data = response.read()
    # data = str(gzip.decompress(data), 'utf-8')
    # json_file = json.loads(data)
    #
    # for player in json_file["resultSets"][0]["rowSet"]:
    #     if player[1] is None:
    #         continue
    #     player_name = str(player[1])
    #     player = [player[9], player[10]]
    #     try:
    #         season_stats[player_name] = season_stats[player_name] + player
    #     except Exception:
    #         if player_name in season_stats:
    #             del season_stats[player_name]
    #         continue

    return season_stats
