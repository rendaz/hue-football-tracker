from time import sleep

NFL_TEAM_COLOR_DICT = {
    'ARI': {'primary': 'red', 'secondary': 'white'},
    'ATL': {'primary': 'red', 'secondary': 'white'},
    'BAL': {'primary': 'purple', 'secondary': 'black'},
    'BUF': {'primary': 'red', 'secondary': 'blue'},
    'CAR': {'primary': 'light blue', 'secondary': 'silver'},
    'CIN': {'primary': 'orange', 'secondary': 'black'},
    'CLE': {'primary': 'orange', 'secondary': 'brown'},
    'DEN': {'primary': 'orange', 'secondary': 'black'},
    'DET': {'primary': 'light blue', 'secondary': 'white'},
    'KC':  {'primary': 'red', 'secondary': 'white'},
    'TB':  {'primary': 'red', 'secondary': 'black'},
    'IND': {'primary': 'blue', 'secondary': 'white'},
    'SF':  {'primary': 'dark red', 'secondary': 'gold'},
    'SEA': {'primary': 'light green', 'secondary': 'dark blue'},
    'MIA': {'primary': 'light green', 'secondary': 'white'},
    'JAX': {'primary': 'dark green', 'secondary': 'yellow'},
    'PHI': {'primary': 'dark green', 'secondary': 'white'},
    'GB':  {'primary': 'dark green', 'secondary': 'yellow'},
    'NYJ': {'primary': 'dark green', 'secondary': 'white'},
    'NO':  {'primary': 'yellow', 'secondary': 'black'},
    'PIT': {'primary': 'yellow', 'secondary': 'black'},
    'SD':  {'primary': 'yellow', 'secondary': 'blue'},
    'CHI':  {'primary': 'blue', 'secondary': 'orange'},
    'NE':  {'primary': 'blue', 'secondary': 'silver'},
    'NYG': {'primary': 'blue', 'secondary': 'white'},
    'LA':  {'primary': 'blue', 'secondary': 'gold'},
    'TEN': {'primary': 'light blue', 'secondary': 'white'},
    'OAK': {'primary': 'silver', 'secondary': 'black'},
    'DAL': {'primary': 'silver', 'secondary': 'blue'},
    'WAS': {'primary': 'red', 'secondary': 'white'},
    'MIN': {'primary': 'purple', 'secondary': 'white'},
}

class NFLTeamColors(object):
    def __init__(self, team_name, light_controller):
        self.team_name = team_name
        self.team_color = NFL_TEAM_COLOR_DICT[self.team_name]
        self.light_controller = light_controller

    def show_team_color(self, use_primary_team_color=True):
        if use_primary_team_color:
            self.light_controller.show_color(self.team_color['primary'])
        else:
            self.light_controller.show_color(self.team_color['secondary'])
