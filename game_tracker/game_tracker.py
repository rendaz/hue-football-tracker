""" Generic Game Tracker to be inherited by each game tracker type """
from time import sleep

class GameTracker(object):
    """ Generic Game Tracker Object """
    def __init__(self, game_id, light_control, verbose=True):
        self.game_id = game_id
        self.verbose = verbose
        self.end_of_game = False
        self.light_controller = light_control

    def start_game_tracker(self):
        """ Begin Tracking the game """
        while True:
            self.update_lights()
            if self.is_end_of_game():
                break
            sleep(10)

    def is_end_of_game(self):
        """ Has the game ended """
        pass

    def track_game(self):
        """ Update the lights """
        pass

    @staticmethod
    def get_game_list():
        """ Get a list of games being played """
        pass

    @staticmethod
    def list_games(conference=None):
        """ Print a list of games being played """
        pass
