import urllib.request
from urllib.error import HTTPError
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select, and_, text
import datetime
import gzip
import json
import csv
from team import Team
import re
import pandas as pd

db = create_engine('sqlite:///NBAPlayers.db', echo=False)
meta = MetaData()
conn = db.connect()

players = Table('v_players3', meta,
                 Column('PLAYER_NAME', String),
                 Column('PLAYER_ID', String, primary_key=True),
                 Column('TEAM_ID', String),
                 Column('TEAM_ABBREVIATION', String),
                 Column('SEASON', String, primary_key=True),
                 Column('AGE', Integer),
                 Column('PLAYER_HEIGHT_INCHES', Integer),
                 Column('PLAYER_WEIGHT', Integer),
                 Column('DRAFT_YEAR', String),
                 Column('DRAFT_ROUND', Integer),
                 Column('DRAFT_NUMBER', Integer),
                 Column('GP', Integer),
                 Column('MIN', Integer),
                 Column('PTS', Integer),
                 Column('EFG_PCT', Integer),
                 Column('TS_PCT', Integer),
                 Column('FGM', Integer),
                 Column('FGA', Integer),
                 Column('FG_PCT', Integer),
                 Column('FG3M', Integer),
                 Column('FG3A', Integer),
                 Column('FG3_PCT', Integer),
                 Column('FTM', Integer),
                 Column('FTA', Integer),
                 Column('FT_PCT', Integer),
                 Column('OREB', Integer),
                 Column('DREB', Integer),
                 Column('REB', Integer),
                 Column('AST', Integer),
                 Column('TOV', Integer),
                 Column('STL', Integer),
                 Column('BLK', Integer),
                 Column('PF', Integer),
                 Column('PFD', Integer),
                 Column('PLUS_MINUS', Integer),
                 Column('OFF_RATING', Integer),
                 Column('DEF_RATING', Integer),
                 Column('NET_RATING', Integer),
                 Column('AST_PCT', Integer),
                 Column('AST_TO', Integer),
                 Column('AST_RATIO', Integer),
                 Column('OREB_PCT', Integer),
                 Column('DREB_PCT', Integer),
                 Column('REB_PCT', Integer),
                 Column('USG_PCT', Integer),
                 Column('PACE', Integer),
                 Column('PIE', Integer),
                 Column('POSS', Integer),
                 Column('DEFLECTIONS', Integer),
                 Column('CHARGES_DRAWN', Integer),
                 Column('SCREEN_ASSISTS', Integer),
                 Column('PTS_OFF_TOV', Integer),
                 Column('PTS_2ND_CHANCE', Integer),
                 Column('PTS_FB', Integer),
                 Column('PTS_PAINT', Integer),
                 Column('OPP_PTS_OFF_TOV', Integer),
                 Column('OPP_PTS_2ND_CHANCE', Integer),
                 Column('OPP_PTS_FB', Integer),
                 Column('OPP_PTS_PAINT', Integer),
                 Column('OPP_FGM', Integer),
                 Column('OPP_FGA', Integer),
                 Column('OPP_FG_PCT', Integer),
                 Column('OPP_FG3M', Integer),
                 Column('OPP_FG3A', Integer),
                 Column('OPP_FG3_PCT', Integer),
                 Column('TEAM_NAME', String))

# used to store information regarding a single NBA Game
class NBAGame:
    def __init__(self, game_id, daily_games_json, season):
        self.game_id = game_id
        self.daily_games_json = daily_games_json
        self.season = season

        self.home_id = None
        self.away_id = None
        self.home_points = None
        self.away_points = None
        self.home_players = []
        self.away_players = []
        self.home_win = None

        self.__set_team_ids()
        self.__set_points()
        self.__set_seasonal_stats()
        self.__set_result()

    # finds the match lineup in "Series Standings" and sets the appropriate values
    def __set_team_ids(self):
        for i in range(len(self.daily_games_json["resultSets"][2]["rowSet"])):  # increment through all games
            if self.daily_games_json["resultSets"][2]["rowSet"][i][0] == self.game_id:  # find matching game
                self.home_id = self.daily_games_json["resultSets"][2]["rowSet"][i][1]
                self.away_id = self.daily_games_json["resultSets"][2]["rowSet"][i][2]
                return

    # finds the points for each team in "Line Score" and sets the appropriate values
    def __set_points(self):
        for i in range(len(self.daily_games_json["resultSets"][1]["rowSet"])):  # increment through all teams
            if self.daily_games_json["resultSets"][1]["rowSet"][i][3] == self.home_id:  # match home id
                self.home_points = self.daily_games_json["resultSets"][1]["rowSet"][i][22]
            if self.daily_games_json["resultSets"][1]["rowSet"][i][3] == self.away_id:  # match away id
                self.away_points = self.daily_games_json["resultSets"][1]["rowSet"][i][22]
            if self.home_points is not None and self.away_points is not None:  # stops when both are filled
                return

    # finds player stats in "PlayerStats" and sets the appropriate values
    def __set_seasonal_stats(self):
        game_stats_json = stats_in_game(self.game_id)  # uses game-specific box score JSON

        home_player_ids = []
        away_player_ids = []

        for player in game_stats_json["resultSets"][0]["rowSet"]:  # increment through all players
            try:
                mins_played = player[8]
                if mins_played is not None:
                    if player[1] == self.home_id:
                        home_player_ids.append(str(player[4]))
                    else:
                        away_player_ids.append(str(player[4]))
            except AttributeError:
                continue
            except Exception as e:
                print(e)

        # queries the stats for all of the players who played in the game
        query = select([players]).where(and_(players.c.YEAR == self.season, players.c.PLAYER_ID.in_(home_player_ids)))
        result = conn.execute(query).fetchall()
        for player in result:
            player_stats = player.values()
            delete_indexes = [13, 16, 19, 37, 38]
            for index in sorted(delete_indexes, reverse=True):
                del player_stats[index]
            del player_stats[:9]
            self.home_players.append(player_stats)

        query = select([players]).where(and_(players.c.YEAR == self.season, players.c.PLAYER_ID.in_(away_player_ids)))
        result = conn.execute(query).fetchall()
        for player in result:
            player_stats = player.values()
            delete_indexes = [13, 16, 19, 37, 38]
            for index in sorted(delete_indexes, reverse=True):
                del player_stats[index]
            del player_stats[:9]
            self.away_players.append(player_stats)

        # filter home and away players to the eight with the most minutes
        self.home_players.sort(key=lambda x: x[0], reverse=True)
        del self.home_players[8:]
        self.away_players.sort(key=lambda x: x[0], reverse=True)
        del self.away_players[8:]

    # compares scores and determines which team won
    def __set_result(self):
        if self.home_points > self.away_points:
            self.home_win = True
        else:
            self.home_win = False

    # prints all variables
    def print_vars(self):
        attrs = vars(self)
        print('\n'.join("%s: %s" % item for item in attrs.items()))

    # inserts seasonal data into an array
    def compile_data(self):
        game_data_array = [int(self.game_id), int(self.home_win)]  # array that stores the stats --> corresponds to a single row in the CSV file

        calc_stats(self.home_players, 240)
        calc_stats(self.away_players, 240)

        game_data_array.extend(Team(self.home_players).export())
        game_data_array.extend(Team(self.away_players).export())

        return game_data_array


def calc_stats(players, rem_min):
    overflow = False
    edit_stat_indexes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20, 21, 22, 23, 24]

    total_min = 0
    for player in players:
        total_min += player[0]
    min_ratio = rem_min / total_min

    adj_players = []
    not_adj_players = []
    for player in players:
        if player[0] * min_ratio > 40:
            min_ratio = 40 / player[0]
            for index in edit_stat_indexes:
                player[index] = player[index] * min_ratio
            overflow = True
            adj_players.append(player)
        else:
            not_adj_players.append(player)

    if not overflow:
        for player in players:
            for index in edit_stat_indexes:
                player[index] = player[index] * min_ratio
    else:
        adj_min = 0
        for player in adj_players:
            adj_min += player[0]
        calc_stats(not_adj_players, rem_min - adj_min)


# finds all games on a specific day and returns a JSON containing info of all games on that day
def games_on_date(month, day, year):
    day = f"{month}%2F{day}%2F{year}"
    game_id_url = f"https://stats.nba.com/stats/scoreboardV2?DayOffset=0&LeagueID=00&gameDate={day}"
    game_id_headers = {"Host": "stats.nba.com", "Connection": "keep-alive",
                       "Accept": "application/json, text/plain, */*", "x-nba-stats-origin": "stats",
                       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
                       "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9"}

    req = urllib.request.Request(url=game_id_url, headers=game_id_headers)
    response = urllib.request.urlopen(req)
    data = response.read()
    data = str(gzip.decompress(data), 'utf-8')
    gameday_json = json.loads(data)
    return gameday_json


# returns all the games played on a specific day
def get_game_ids(gameday_json):
    game_list = gameday_json["resultSets"][0]["rowSet"]
    game_ids = []
    for game in game_list:
        game_ids.append(game[2])
    return game_ids


# finds box score information of a specific game and a JSON containing detailed stats of players in the game
def stats_in_game(game_id):
    game_stats_url = f"https://stats.nba.com/stats/boxscoretraditionalv2?EndPeriod=10&EndRange=28800&GameID={game_id}&RangeType=0&StartPeriod=1&StartRange=0"
    game_stats_headers = {"Host": "stats.nba.com", "Connection": "keep-alive",
                          "Accept": "application/json, text/plain, */*", "x-nba-stats-origin": "stats",
                          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
                          "Referer": f"https://stats.nba.com/game/{game_id}/", "Accept-Encoding": "gzip, deflate, br",
                          "Accept-Language": "en-US,en;q=0.9"}

    req = urllib.request.Request(url=game_stats_url, headers=game_stats_headers)
    response = urllib.request.urlopen(req)
    data = response.read()
    data = str(gzip.decompress(data), 'utf-8')
    json_file = json.loads(data)
    return json_file


# converts data into a csv file
def export_data(game_day_matrix, filename):
    with open(filename, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)  # creating a csv writer object
        csv_writer.writerows(game_day_matrix)  # writing the data rows


def collect_data(date_range, filename):
    try:

        start_month = date_range[0].month
        start_year = date_range[0].year
        changed_season = True

        if start_month > 5:
            season = start_year + 1
        else:
            season = start_year

        for date in date_range:
            year = date.year
            month = date.month
            day = date.day

            if month in range(6, 10):
                continue

            if month == 10 and changed_season is False:
                season += 1
                changed_season = True
            elif month != 10:
                changed_season = False

            try:
                games = games_on_date(str(month).zfill(2), str(day).zfill(2), year)
                game_id_list = get_game_ids(games)
                game_day_matrix = []
                games_skipped = 0

                for game_id in game_id_list:
                    if str(game_id)[2] != "2":
                        games_skipped += 1
                        continue
                    target_game = NBAGame(game_id, games, season)
                    game_data = target_game.compile_data()
                    game_day_matrix.append(game_data)

                time = datetime.datetime.now().strftime("%I:%M:%S %p")
                games_added = len(game_id_list) - games_skipped

                export_data(game_day_matrix, filename)
                print(str(month).zfill(2), str(day).zfill(2), year, f": {games_added} games added\t({time})")

            except HTTPError as ex:
                if ex.code == 400:
                    break
                else:
                    raise
    except KeyboardInterrupt:
        exit()


csv_filename = "Data/16-17.csv"
start_date = datetime.datetime(2016, 10, 25)
end_date = datetime.datetime(2017, 4, 15)
date_list = pd.date_range(start_date, end_date)
collect_data(date_list, csv_filename)
