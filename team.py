import numpy as np

# converts a list of players stats into team stats
class Team:
    def __init__(self, players_stats):
        self.players_stats = players_stats

        self.ts_pct = None
        self.fta = None
        self.freq_3p = None
        self.ast = None
        self.tov = None
        self.oreb = None
        self.dreb = None
        self.stl = None
        self.blk = None
        self.defl = None
        self.defg_pct = None
        self.pf = None
        self.off_rtg = None
        self.def_rtg = None

        self.__calculate()

    # calculates team stats using the player stats
    def __calculate(self):
        # TODO: Account for pace
        sum_stats = np.array(self.players_stats).sum(axis=0)

        relevant_stats = ['MIN', 'PTS', 'FGA', 'FG3A', 'FTM', 'FTA', 'OREB', 'DREB', 'AST', 'TOV', 'STL', 'BLK',
                          'PF', 'OFF_RATING', 'DEF_RATING', 'PACE', 'DEFLECTIONS', 'DFG3M', 'DFG3A', 'DFG2M', 'DFG2A']

        total_pts = sum_stats[relevant_stats.index('PTS')]
        total_fta = sum_stats[relevant_stats.index('FTA')]
        total_fga = sum_stats[relevant_stats.index('FGA')]
        total_3pa = sum_stats[relevant_stats.index('FG3A')]
        total_ast = sum_stats[relevant_stats.index('AST')]
        total_tov = sum_stats[relevant_stats.index('TOV')]
        total_stl = sum_stats[relevant_stats.index('STL')]
        total_blk = sum_stats[relevant_stats.index('BLK')]
        total_oreb = sum_stats[relevant_stats.index('OREB')]
        total_dreb = sum_stats[relevant_stats.index('DREB')]
        total_defl = sum_stats[relevant_stats.index('DEFLECTIONS')]
        total_dfg2m = sum_stats[relevant_stats.index('DFG2M')]
        total_dfg3m = sum_stats[relevant_stats.index('DFG3M')]
        total_dfga = sum_stats[relevant_stats.index('DFG2A')] + sum_stats[relevant_stats.index('DFG3A')]
        total_pf = sum_stats[relevant_stats.index('PF')]

        # calculate true shooting percentage
        self.ts_pct = round(total_pts / (2 * (total_fga + (0.44 * total_fta))), 3)

        # calculate total free throw attempts
        self.fta = round(total_fta, 2)

        # calculate the frequency of 3P attempts
        self.freq_3p = round(total_3pa / total_fga, 2)

        # calculate total assists
        self.ast = round(total_ast, 2)

        # calculate total turnovers
        self.tov = round(total_tov, 2)

        # calculate total offensive rebounds
        self.oreb = round(total_oreb, 2)

        # calculate total defensive rebounds
        self.dreb = round(total_dreb, 2)

        # calculate total steals
        self.stl = round(total_stl, 2)

        # calculate total blocks
        self.blk = round(total_blk, 2)

        # calculate total deflections
        self.defl = round(total_defl, 2)

        # calculate defensive effective field goal percentage
        self.defg_pct = round((total_dfg2m + 1.5 * total_dfg3m) / total_dfga, 3)

        # calculate total personal fouls
        self.pf = round(total_pf, 2)

        # calculate offensive/defensive rating
        min_weights = [player[relevant_stats.index('MIN')] for player in self.players_stats]
        off_rtg = [player[relevant_stats.index('OFF_RATING')] for player in self.players_stats]
        def_rtg = [player[relevant_stats.index('DEF_RATING')] for player in self.players_stats]
        self.off_rtg = round(np.average(off_rtg, weights=min_weights), 2)
        self.def_rtg = round(np.average(def_rtg, weights=min_weights), 2)

    def export(self):
        return [self.ts_pct, self.fta, self.freq_3p, self.ast, self.tov, self.oreb, self.dreb, self.stl, self.blk, self.defl, self.defg_pct, self.pf, self.off_rtg, self.def_rtg]
