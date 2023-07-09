from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select, and_
from team import Team
import numpy as np
import csv
from v_players_schema import Players_Table

db = create_engine('sqlite:///NBAPlayers.db', echo=False)
players_table = Players_Table.__table__

# Processes information entered into form - returns an array of stats to be analyzed by our model
def stats_mod(team_id):
    # TODO: Account for pace
    team_stats = get_stats(team_id)

    relevant_stats = ['MIN', 'PTS', 'FGA', 'FG3A', 'FTA', 'OREB', 'DREB', 'AST', 'TOV', 'STL', 'BLK',
                      'PF', 'OFF_RATING', 'DEF_RATING', 'PACE', 'DEFLECTIONS', 'DFG3M', 'DFG3A', 'DFG2M', 'DFG2A']
    team_stats = [{key: player[key] for key in relevant_stats} for player in team_stats]

    game_data_array = []
    adjust_for_minutes(team_stats, 240)

    game_data_array.extend(Team([list(stats.values()) for stats in team_stats]).export())

    return np.array(game_data_array)

# Executes queries - returns dictionaries of home and away player stats
def get_stats(team_id):
    query = select([players_table.c.PLAYER_ID]).where(
        and_(players_table.c.SEASON == '2023', players_table.c.TEAM_ID == team_id)).order_by(
            players_table.c.MIN.desc()).limit(8)
    conn = db.connect()
    result = conn.execute(query)
    player_ids = [str(r[0]) for r in result]

    query = select([players_table]).where(and_(players_table.c.SEASON == '2023', players_table.c.PLAYER_ID.in_(player_ids)))
    conn = db.connect()
    result = conn.execute(query)
    stats = [dict(r) for r in result]

    return stats

# Adjusts the player stats to account for their selected teammates
def adjust_for_minutes(players, rem_min):
    overflow = False
    scaled_stats = ['MIN', 'PTS', 'FGA', 'FG3A', 'FTA', 'OREB', 'DREB', 'AST', 'TOV', 'STL', 'BLK',
                    'PF', 'DEFLECTIONS', 'DFG3M', 'DFG3A', 'DFG2M', 'DFG2A']

    total_min = 0
    for player in players:
        total_min += player['MIN']
    min_ratio = rem_min / total_min

    adj_players = []
    not_adj_players = []
    for player in players:
        if player['MIN'] * min_ratio > 42:
            min_ratio = 42 / player['MIN']
            for stat in scaled_stats:
                player[stat] = player[stat] * min_ratio
            overflow = True
            adj_players.append(player)
        else:
            not_adj_players.append(player)

    if not overflow:
        for player in players:
            for stat in scaled_stats:
                player[stat] = player[stat] * min_ratio
    else:
        adj_min = 0
        for player in adj_players:
            adj_min += player['MIN']
        adjust_for_minutes(not_adj_players, rem_min - adj_min)


query = select([players_table.c.TEAM_NAME, players_table.c.TEAM_ID]).where(players_table.c.SEASON == '2023').distinct().order_by(players_table.c.TEAM_NAME)
conn = db.connect()
result = conn.execute(query)
output = [dict(r) for r in result]

stats_list = []
for team in output:
    team_stats = [team['TEAM_NAME']]
    team_stats.extend(stats_mod(team['TEAM_ID']))
    stats_list.append(team_stats)
# print(stats_list)

filename = "team_stats2.csv"
with open(filename, 'a', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)  # creating a csv writer object
    csv_writer.writerows(stats_list)  # writing the data rows
