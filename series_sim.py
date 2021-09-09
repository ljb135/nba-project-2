from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select, and_
from Team import Team
import pickle
import numpy as np
import random

db = create_engine('sqlite:///NBAPlayers.db', echo=False)
meta = MetaData()
Pkl_Filename = "NBA_LRModel2.pkl"
with open(Pkl_Filename, 'rb') as file:
    model = pickle.load(file)

# Table format from database
players = Table('v_players2', meta,
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
                Column('DFG3A', Integer),
                Column('INJ', Integer),
                Column('TEAM_NAME', String))


def get_stats(home_team, away_team):
    query = select([players.c.PLAYER_ID]).where(
            and_(players.c.YEAR == '2021', players.c.TEAM_ABR == home_team, players.c.GP > 30, players.c.INJ == 0)).order_by(
            players.c.MIN.desc()).limit(8)
    conn = db.connect()
    result = conn.execute(query)

    home_stats = []
    for player in result:
        query = select([players]).where(and_(players.c.YEAR == '2021', players.c.PLAYER_ID == player.PLAYER_ID))
        conn = db.connect()
        data = conn.execute(query)

        data = data.fetchone().values()
        delete_indexes = [13, 16, 19, 37, 38]
        for index in sorted(delete_indexes, reverse=True):
            del data[index]
        del data[:9]
        home_stats.append(data)

    query = select([players.c.PLAYER_ID]).where(
        and_(players.c.YEAR == '2021', players.c.TEAM_ABR == away_team, players.c.GP > 30,
             players.c.INJ == 0)).order_by(
        players.c.MIN.desc()).limit(8)
    conn = db.connect()
    result = conn.execute(query)

    away_stats = []
    for player in result:
        query = select([players]).where(and_(players.c.YEAR == '2021', players.c.PLAYER_ID == player.PLAYER_ID))
        conn = db.connect()
        data = conn.execute(query)

        data = data.fetchone().values()
        delete_indexes = [13, 16, 19, 37, 38]
        for index in sorted(delete_indexes, reverse=True):
            del data[index]
        del data[:9]
        away_stats.append(data)

    return np.array(stats_mod(home_stats, away_stats))


def stats_mod(home_players, away_players):
    game_data_array = []
    calc_stats(home_players, 240)
    calc_stats(away_players, 240)

    game_data_array.extend(Team(home_players).export())
    game_data_array.extend(Team(away_players).export())

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


def run_sim():
    high_seed_wins = 0
    low_seed_wins = 0
    for i in range(1, 8):
        rng = random.randint(1, 1000)
        if i in [1, 2, 5, 7]:
            if rng <= high_seed_cutoff:
                high_seed_wins += 1
            else:
                low_seed_wins += 1
        else:
            if rng <= low_seed_cutoff:
                low_seed_wins += 1
            else:
                high_seed_wins += 1
        if high_seed_wins >= 4:
            return high_seed, i
        if low_seed_wins >= 4:
            return low_seed, i


high_seed = "UTA"
low_seed = "BKN"

data_array = np.array([get_stats(high_seed, low_seed)])
high_seed_prediction = model.predict_proba(data_array)
high_seed_cutoff = high_seed_prediction[0][1] * 1000
data_array = np.array([get_stats(low_seed, high_seed)])
low_seed_prediction = model.predict_proba(data_array)
low_seed_cutoff = low_seed_prediction[0][1] * 1000

high_seed_total = 0
low_seed_total = 0
games_total = 0
for i in range(1000):
    winner, games = run_sim()
    games_total += games
    if winner == high_seed:
        high_seed_total += 1
    else:
        low_seed_total += 1
avg_games = round (games_total / 1000, 1)
if high_seed_total > low_seed_total:
    print(high_seed + " wins in " + str(avg_games) + " games!")
else:
    print(low_seed + " wins in " + str(avg_games) + " games!")


