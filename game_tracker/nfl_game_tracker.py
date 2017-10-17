""" Track NFL games and adjust lights to follow in-game events """

import datetime
from datetime import date
from time import sleep
import nflgame
from game_tracker import GameTracker
from nfl_team_colors import NFLTeamColors

class NFLGameTracker(GameTracker):
    NFL_START_DATE = datetime.date(2017, 9, 3)

    def __init__(self, game_id, light_control, verbose=True):
        GameTracker.__init__(self, game_id, light_control, verbose)
        self.week = self.get_curr_week()

    @staticmethod
    def get_curr_week():
        """ Get the current week of the NFL calendar """
        week = date.today().isocalendar()[1] - NFLGameTracker.NFL_START_DATE.isocalendar()[1]

	    # if this is a monday then we are still in the previous week :(
        if datetime.datetime.today().weekday() == 0:
            week = week - 1
        return week

    def is_end_of_game(self):
        return self.end_of_game

    @staticmethod
    def list_games(conference=None):
        games = NFLGameTracker.get_game_list()

        print "========== Welcome to week " + str(NFLGameTracker.get_curr_week()) + " ============"

        for i, game in enumerate(games):
            print "%d) %s" % (i, game)

    @staticmethod
    def get_game_list():
        return nflgame.games(NFLGameTracker.NFL_START_DATE.year,
                             week=NFLGameTracker.get_curr_week())

    def track_game(self):

        all_games = NFLGameTracker.get_game_list()

        game = all_games[self.game_id]
        away_team = NFLTeamColors(game.away, self.light_controller)
        home_team = NFLTeamColors(game.home, self.light_controller)

        for drive in game.drives.__reversed__():
            if game.game_over():
                cur_team = game.winner
                self.end_of_game = True
            else:
                cur_team = drive.team

            field_end = drive.field_end.__str__().split()
            is_red_zone = True if field_end[0] == "OPP" and int(field_end[1]) <= 20 else False

            if is_red_zone:
                if self.verbose:
                    print "Inside Red Zone"
                self.light_controller.show_color('red')

            if drive.result:
                if drive.result.lower() == 'touchdown':
                    if cur_team == game.home:
                        self.light_controller.touchdown(home_team)
                else:
                    self.light_controller.touchdown(away_team)
                    if drive.result.lower() in ['field goal', 'safety']:
                        self.light_controller.field_goal()

                is_turnover = self.turnover(drive.result)

                if cur_team == game.home and not is_turnover or cur_team == game.away and is_turnover:
                    home_team.show_team_color()
                    if self.verbose:
                        print "%s possession" % game.home
                        if drive.result:
                            print drive.result
                else:
                    use_secondary_colors = True if away_team.team_color['primary'] == home_team.team_color['primary'] else False

                    away_team.show_team_color(not use_secondary_colors)
                    if self.verbose:
                        print "%s possession" % game.away
                        if drive.result:
                            print drive.result

                if drive.result and drive.result.lower() in ['touchdown', 'field goal']:
                    sleep(15)
                break

    @staticmethod
    def turnover(result):
        """ determine if a turnover has occurred in the game """
        if result.lower() in ['punt', 'interception', 'fumble', 'turnover', 'downs']:
            return True
        return False
