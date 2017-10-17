from time import sleep

NFL_TEAM_COLOR_DICT = {
    'ARI': {'primary': 'red', 'secondary': 'white'},
    'ATL': {'primary': 'red', 'secondary': 'white'},
    'BAL': {'primary': 'purple', 'secondary': 'black'},
    'BUF': {'primary': 'red', 'secondary': 'blue'},
    'CAR': {'primary': 'light blue', 'secondary': 'silver'},
    'CHI': {'primary': 'blue', 'secondary': 'orange'},
    'CIN': {'primary': 'orange', 'secondary': 'black'},
    'CLE': {'primary': 'orange', 'secondary': 'brown'},
    'DAL': {'primary': 'silver', 'secondary': 'blue'},
    'DEN': {'primary': 'orange', 'secondary': 'black'},
    'DET': {'primary': 'light blue', 'secondary': 'white'},
    'GB':  {'primary': 'dark green', 'secondary': 'yellow'},
    'HOU': {'primary': 'blue', 'secondary': 'red'},
    'IND': {'primary': 'blue', 'secondary': 'white'},
    'JAX': {'primary': 'dark green', 'secondary': 'yellow'},
    'KC':  {'primary': 'red', 'secondary': 'white'},
    'LA':  {'primary': 'blue', 'secondary': 'gold'},
    'MIA': {'primary': 'light green', 'secondary': 'white'},
    'MIN': {'primary': 'purple', 'secondary': 'white'},
    'NE':  {'primary': 'blue', 'secondary': 'silver'},
    'NO':  {'primary': 'yellow', 'secondary': 'black'},
    'NYG': {'primary': 'blue', 'secondary': 'white'},
    'NYJ': {'primary': 'dark green', 'secondary': 'white'},
    'OAK': {'primary': 'silver', 'secondary': 'black'},
    'PHI': {'primary': 'dark green', 'secondary': 'white'},
    'PIT': {'primary': 'yellow', 'secondary': 'black'},
    'SD':  {'primary': 'yellow', 'secondary': 'blue'},
    'SEA': {'primary': 'light green', 'secondary': 'dark blue'},
    'SF':  {'primary': 'dark red', 'secondary': 'gold'},
    'TB':  {'primary': 'red', 'secondary': 'black'},
    'TEN': {'primary': 'light blue', 'secondary': 'white'},
    'WAS': {'primary': 'red', 'secondary': 'white'},
}

class NFLTeamColors(object):
    """ Handle conversion from team name to the teams primary/secondary colors """
    def __init__(self, team_name, light_controller):
        self.team_name = team_name
        self.team_color = NFL_TEAM_COLOR_DICT[self.team_name]
        self.light_controller = light_controller

    def show_team_color(self, use_primary_team_color=True):
        if use_primary_team_color:
            self.light_controller.show_color(self.team_color['primary'])
        else:
            self.light_controller.show_color(self.team_color['secondary'])
