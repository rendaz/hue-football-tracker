""" A factory for all game trackers """

from nfl_game_tracker import NFLGameTracker
from cfb_game_tracker import CFBGameTracker

class FootballTrackerFactory(object):
    """ Game tracker factory """
    @staticmethod
    def factory(game_type):
        """ Game tracker factory """
        if game_type == "cfb":
            return CFBGameTracker
        if game_type == "nfl":
            return NFLGameTracker
        assert 0, "Bad football game tracker type: " + type
#    factory = factory
