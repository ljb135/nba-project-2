import numpy as np


# converts a list of players stats into team stats
class Team:
    def __init__(self, players_stats):
        self.players_stats = players_stats

        self.pts = None
        self.ts_pct = None
        self.fta = None
        self.ft_pct = None
        self.fg3a = None
        self.fg3_pct = None
        self.ast = None
        self.tov = None
        self.oreb = None
        self.dreb = None
        self.stl = None
        self.blk = None
        self.pf = None

        self.__calculate()

    # calculates team stats using the player stats
    def __calculate(self):
        sum_stats = np.array(self.players_stats).sum(axis=0)

        total_pts = sum_stats[2]
        total_ftm = sum_stats[3]
        total_fta = sum_stats[4]
        total_fga = sum_stats[7]
        total_3pm = sum_stats[9]
        total_3pa = sum_stats[10]
        total_ast = sum_stats[12]
        total_tov = sum_stats[13]
        total_stl = sum_stats[14]
        total_blk = sum_stats[15]
        total_oreb = sum_stats[16]
        total_dreb = sum_stats[17]
        total_pf = sum_stats[18]

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

        # calculate total personal fouls
        self.pf = round(total_pf, 2)

    def export(self):
        return [self.pts, self.ts_pct, self.fta, self.ft_pct, self.fg3a, self.fg3_pct, self.ast, self.tov, self.oreb,
                self.dreb, self.stl, self.blk, self.defl, self.lb_rec, self.cont_2, self.cont_3, self.defg_pct,
                self.off_rtg, self.def_rtg, self.pf]
