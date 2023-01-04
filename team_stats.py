from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select, and_
from Team import Team
import numpy as np
import csv

db = create_engine('sqlite:///NBAPlayers.db', echo=False)
meta = MetaData()

# Table format from database
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

def get_stats(team):
    query = select([players.c.PLAYER_ID]).where(
            and_(players.c.YEAR == '2021', players.c.TEAM_ABR == team, players.c.GP > 30, players.c.INJ == 0)).order_by(
            players.c.MIN.desc()).limit(8)
    conn = db.connect()
    result = conn.execute(query)

    stats = []
    for player in result:
        query = select([players]).where(and_(players.c.YEAR == '2021', players.c.PLAYER_ID == player.PLAYER_ID))
        conn = db.connect()
        data = conn.execute(query)

        data = data.fetchone().values()
        delete_indexes = [13, 16, 19, 37, 38]
        for index in sorted(delete_indexes, reverse=True):
            del data[index]
        del data[:9]
        stats.append(data)

    return stats_mod(team, stats)


def stats_mod(team, players):
    game_data_array = [team]
    calc_stats(players, 240)
    game_data_array.extend(Team(players).export())
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


query = select([players.c.TEAM_ABR]).where(players.c.YEAR == '2021').distinct().order_by(players.c.TEAM_NAME)
conn = db.connect()
result = conn.execute(query)
stats_list = []
for team in result:
    stats_list.append(get_stats(team.TEAM_ABR))
filename = "Data/team_stats.csv"
print(stats_list)
with open(filename, 'a', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)  # creating a csv writer object
    csv_writer.writerows(stats_list)  # writing the data rows
