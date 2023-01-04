import numpy as np

# converts a list of players stats into team stats
class Team:
    def __init__(self, players_stats):
        self.players_stats = players_stats

        # self.pts = None
        # self.ts_pct = None
        self.fta = None
        self.ft_pct = None
        self.fg2a = None
        self.fg3a = None
        self.fg3a = None
        self.fg3_pct = None
        self.ast = None
        self.tov = None
        self.oreb = None
        self.dreb = None
        self.stl = None
        self.blk = None
        # self.defl = None
        # self.lb_rec = None
        self.cont_2 = None
        self.cont_3 = None
        self.defg_pct = None
        self.pf = None
        self.off_rtg = None
        self.def_rtg = None

        self.__calculate()

    # calculates team stats using the player stats
    def __calculate(self):
        sum_stats = np.array(self.players_stats).sum(axis=0)

        total_pts = sum_stats[1]
        total_ftm = sum_stats[2]
        total_fta = sum_stats[3]
        total_fga = sum_stats[5]
        total_3pm = sum_stats[6]
        total_3pa = sum_stats[7]
        total_ast = sum_stats[8]
        total_tov = sum_stats[9]
        total_stl = sum_stats[10]
        total_blk = sum_stats[11]
        total_oreb = sum_stats[12]
        total_dreb = sum_stats[13]
        total_defl = sum_stats[17]
        total_lb_rec = sum_stats[18]
        total_cont_2 = sum_stats[19]
        total_cont_3 = sum_stats[20]
        total_dfg2m = sum_stats[21]
        total_dfg3m = sum_stats[23]
        total_dfga = sum_stats[22] + sum_stats[24]
        total_pf = sum_stats[14]

        # calculate total points
        self.pts = round(total_pts, 2)

        # calculate true shooting percentage
        self.ts_pct = round(total_pts / (2 * (total_fga + (0.44 * total_fta))), 3)

        # calculate total free throw attempts
        self.fta = round(total_fta, 2)

        # calculate free throw percentage
        self.ft_pct = round(total_ftm / total_fta, 3)

        # calculate total three point attempts
        self.fg3a = round(total_3pa, 2)

        # calculate three point percentage
        self.fg3_pct = round(total_3pm / total_3pa, 3)

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

        # calculate total loose ball recovered
        self.lb_rec = round(total_lb_rec, 2)

        # calculate total contested twos
        self.cont_2 = round(total_cont_2, 2)

        # calculate total contested threes
        self.cont_3 = round(total_cont_3, 2)

        # calculate defensive effective field goal percentage
        self.defg_pct = round((total_dfg2m + 1.5 * total_dfg3m) / total_dfga, 3)

        # calculate total personal fouls
        self.pf = round(total_pf, 2)

        # calculate offensive/defensive rating
        min_weights = [row[0] for row in self.players_stats]
        off_rtg = [row[15] for row in self.players_stats]
        def_rtg = [row[16] for row in self.players_stats]
        self.off_rtg = round(np.average(off_rtg, weights=min_weights), 2)
        self.def_rtg = round(np.average(def_rtg, weights=min_weights), 2)

    def export(self):
        return [self.pts, self.ts_pct, self.fta, self.ft_pct, self.fg3a, self.fg3_pct, self.ast, self.tov, self.oreb,
                self.dreb, self.stl, self.blk, self.defl, self.lb_rec, self.cont_2, self.cont_3, self.defg_pct,
                self.off_rtg, self.def_rtg, self.pf]
