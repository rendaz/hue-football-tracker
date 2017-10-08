import datetime
from datetime import date
from time import sleep
import nflgame
from phue import Bridge
import argparse
import logging
import random
import math
import json
import httplib2
from colour import Color

logging.basicConfig()

TeamColorDict = {
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


class TeamColors:
    def __init__(self, team_name, hue_controller):
        self.team_name = team_name
        self.team_color = TeamColorDict[self.team_name]
        self.hue_controller = hue_controller

        self.color_converter = {
            'blue': self.hue_controller.blue,
	    'light blue': self.hue_controller.light_blue,
	    'orange': self.hue_controller.orange,
	    'red': self.hue_controller.red,
	    'dark red': self.hue_controller.dark_red,
            'light green': self.hue_controller.light_green,
	    'dark green': self.hue_controller.dark_green,
	    'yellow': self.hue_controller.yellow,
	    'silver': self.hue_controller.silver,
	    'purple': self.hue_controller.purple,
	    'gold': self.hue_controller.gold,
	    'brown': self.hue_controller.brown,
	    'black': self.hue_controller.black,
	    'white': self.hue_controller.white,
	    'dark blue': self.hue_controller.dark_blue,
	}

    def show_team_color(self, use_primary_team_color=True):
        primary_color = self.color_converter[self.team_color['primary']]
        secondary_color = self.color_converter[self.team_color['secondary']]

        if use_primary_team_color:
            color = primary_color
	else:
            color = secondary_color

        # self.alternate_flashing_colors(primary_color, secondary_color)
	color()

    def alternate_flashing_colors(self, color1, color2):
        for num in xrange(6):
            if num % 2 == 1:
                color1([1,3])
                color2([2,4])
            else:
                color2([1,3])
                color1([2,4])
            sleep(5)

class CFBGameTracker():
    def __init__(self, game_id, verbose=True):
        self.game_id = game_id
	self.verbose = verbose
        self.end_of_game = False
        self.house_lights = LightControl()
        self.home_score = None
        self.away_score = None

        self.curr_date = "20170930" # date.today().strftime('%Y%m%d')
        self.cfb_date_api_url = "https://cfb-scoreboard-api.herokuapp.com/v1/date/%s" % (self.curr_date)

    @staticmethod
    def get_game_list():
        curr_date = date.today().strftime('%Y%m%d') # "20170930"
        cfb_api_url = "https://cfb-scoreboard-api.herokuapp.com/v1/date/%s" % (curr_date)
        __resp, content = httplib2.Http().request(cfb_api_url)

        req_json = json.loads(content)
        return req_json[u'games']

    @staticmethod
    def list_games(conference=None):
        all_games = CFBGameTracker.get_game_list()
        for x, game in enumerate(all_games):
            if conference and (conference != game['homeTeam'][u'conference'][u'abbreviation'] or conference != game['awayTeam'][u'conference'][u'abbreviation']):
                continue
            home_rank = '(' + str(game['homeTeam']['rank']) + ') ' if game['homeTeam']['rank'] <= 25 else ''
            away_rank = '(' + str(game['awayTeam']['rank']) + ') ' if game['awayTeam']['rank'] <= 25 else ''
	    # print game
            print "%d) %s%s vs %s%s" % (x, home_rank, game[u'homeTeam'][u'displayName'], away_rank, game[u'awayTeam'][u'displayName'])

    def change_lights_based_on_score_type(self, score_type, color, which_lights):
        if not score_type:
            self.house_lights.custom_color(which_lights, color)
        if score_type == "safty" or score_type == "field goal":
            self.house_lights.field_goal()
        if score_type == "touchdown":
            self.house_lights.touchdown()

    def get_score_type(self, prev_score, curr_score):
        delta = curr_score - prev_score
        if delta == 0:
            return None
        if delta == 2:
           return "safty"
        if delta == 3:
           return "field goal"
        if delta == 6 or delta == 7 or delta == 8:
            return "touchdown"

    def update_lights(self):
        # cfb_api_url = "https://cfb-scoreboard-api.herokuapp.com/v1/game/%s" % (self.game_id)
        # __resp, content = httplib2.Http().request(self.cfb_date_api_url)

        #req_json = json.loads(content)
        game = self.get_game_list()[self.game_id]
        # print game['status']['type']

        cur_home_score = int(game['scores']['home'])
        cur_away_score = int(game['scores']['away'])

        self.home_score = cur_home_score if self.home_score is None else self.home_score
        self.away_score = cur_away_score if self.away_score is None else self.away_score

        home_score_type = self.get_score_type(self.home_score, cur_home_score)
        away_score_type = self.get_score_type(self.away_score, cur_away_score)

        print "Home color: " + Color('#' + game['homeTeam']['color']).get_hex()
        print "Away color: " + Color('#' + game['awayTeam']['color']).get_hex()
        self.change_lights_based_on_score_type(home_score_type, Color('#' + game['homeTeam']['color']), [1,3])
        self.change_lights_based_on_score_type(away_score_type, Color('#' + game['awayTeam']['color']), [2,4])

    def is_end_of_game(self):
        return self.end_of_game

class NFLGameTracker():
    NFL_START_DATE = datetime.date(2017, 9, 3)

    def __init__(self, game_id, verbose=True):
        self.game_id = game_id
        self.end_of_game = False
        self.verbose = verbose
        self.house_lights = LightControl()
        self.week = self.get_curr_week()

    @staticmethod
    def get_curr_week():
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

        print NFLGameTracker.get_curr_week()

        for x, game in enumerate(games):
            print "%d) %s" % (x, game)

    @staticmethod
    def get_game_list():
        return nflgame.games(NFLGameTracker.NFL_START_DATE.year, week=NFLGameTracker.get_curr_week())

    def update_lights(self):

	all_games = NFLGameTracker.get_game_list()

        game = all_games[self.game_id]
        away_team = TeamColors(game.away, self.house_lights)
        home_team = TeamColors(game.home, self.house_lights)

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
                home_team.color_converter['red']()

	    if drive.result:
	        if drive.result.lower() == 'touchdown':
                    if cur_team == game.home:
                        self.house_lights.touchdown(home_team)
		    else:
			self.house_lights.touchdown(away_team)
                if drive.result.lower() == 'field goal' or drive.result.lower() == 'safety':
                    self.house_lights.field_goal()

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

            if drive.result and (drive.result.lower() == 'touchdown' or drive.result.lower() == 'field goal'):
                sleep(15)
            break

    @staticmethod
    def turnover(result):
        if result.lower() == 'punt' or result.lower() == 'interception' or result.lower() == 'fumble' or result.lower() == 'turnover'  or result.lower() == 'downs':
            return True;
        return False


class LightControl():
    def __init__(self):
        self.bridge = Bridge('172.16.1.41')

        # If the app is not registered and the button is not pressed,
        # press the button and call connect() (this only needs to be run a single time)
        self.bridge.connect()

        # Setup colors
        self.colors = {
            "blue": [0.1393, 0.0813],
            "white": [0.3062, 0.3151],
            "red": [0.674, 0.322]
        }
        self.colorKeys = self.colors.keys()

    # This is based on original code from http://stackoverflow.com/a/22649803
    def EnhanceColor(self, normalized):
        if normalized > 0.04045:
            return math.pow( (normalized + 0.055) / (1.0 + 0.055), 2.4)
        else:
            return normalized / 12.92

    def RGBtoXY(self, color):
        rNorm = color.get_red() # / 255.0
        gNorm = color.get_green() # / 255.0
        bNorm = color.get_blue() # / 255.0

        rFinal = self.EnhanceColor(rNorm)
        gFinal = self.EnhanceColor(gNorm)
        bFinal = self.EnhanceColor(bNorm)

        X = rFinal * 0.649926 + gFinal * 0.103455 + bFinal * 0.197109
        Y = rFinal * 0.234327 + gFinal * 0.743075 + bFinal * 0.022598
        Z = rFinal * 0.000000 + gFinal * 0.053077 + bFinal * 1.035763

        if X + Y + Z == 0:
            return (0,0)
        else:
            xFinal = X / (X + Y + Z)
            yFinal = Y / (X + Y + Z)

            return (xFinal, yFinal)

    def custom_color(self, which_lights, color):
        print "red: " + str(color.get_red()) + " green: " + str(color.get_green()) + " blue: " + str(color.get_blue())
	hue = int(round(color.hue * 65535))
	sat = int(round(color.saturation * 254))
	bri = int(round(color.luminance * 254))
        xy = self.RGBtoXY(color)
	command2 = {'on': True, 'xy': xy}
	command = {'on': True, 'hue': hue, 'sat': sat, 'bri': bri}
	print command
        self.bridge.set_light(which_lights, command)
        sleep(1)
        self.bridge.set_light(which_lights, command2)


    def print_api(self):
        print self.bridge.get_api()

    def all_lights_on(self):
        # You can also control multiple lamps by sending a list as lamp_id
        self.bridge.set_light([1, 2, 3, 4], 'on', True)

    def black(self, which_lights=[1,2,3,4]):
        # You can also control multiple lamps by sending a list as lamp_id
        self.bridge.set_light(which_lights, 'on', False)

    def all_white(self):
        command = {'transitiontime': 100, 'sat': 1, 'bri': 254}
        self.bridge.set_light([1, 2, 3, 4], command)

    def blue(self, which_lights=[1,2,3,4]):
        command = {'on': True, 'hue': 46260, 'sat': 254, 'bri': 254}
        self.bridge.set_light(which_lights, command)

    def light_blue(self, which_lights=[1,2,3,4]):
        command = {'on': True, 'hue': 45296, 'sat': 254, 'bri': 254}
        self.bridge.set_light(which_lights, command)

    def red(self, which_lights=[1,2,3,4]):
        command = {'on': True, 'hue': 65535, 'sat': 254, 'bri': 254}
        self.bridge.set_light(which_lights, command)

    def dark_red(self, which_lights=[1,2,3,4]):
        command = {'on': True, 'hue': 65535, 'sat': 254, 'bri': 164}
        self.bridge.set_light(which_lights, command)

    def purple(self, which_lights=[1,2,3,4]):
        command = {'on': True, 'hue': 49151, 'sat': 254, 'bri': 157}
        self.bridge.set_light(which_lights, command)

    def light_green(self, which_lights=[1,2,3,4]):
        command = {'on': True, 'hue': 24094, 'sat': 254, 'bri': 168}
        self.bridge.set_light(which_lights, command)

    def silver(self, which_lights=[1,2,3,4]):
        command = {'on': True, 'hue': 34695, 'sat': 108, 'bri': 78}
        self.bridge.set_light(which_lights, command)

    def gold(self, which_lights=[1,2,3,4]):
        command = {'on': True, 'hue': 10601, 'sat': 254, 'bri': 254}
        self.bridge.set_light(which_lights, command)

    def brown(self, which_lights=[1,2,3,4]):
        command = {'on': True, 'hue': 10601, 'sat': 254, 'bri': 86}
        self.bridge.set_light(which_lights, command)

    def dark_blue(self, which_lights=[1,2,3,4]):
        command = {'on': True, 'hue': 47224, 'sat': 254, 'bri': 200}
        self.bridge.set_light(which_lights, command)

    def white(self, which_lights=[1,2,3,4]):
        command = {'on': True, 'hue': 5000, 'sat': 1, 'bri': 254}
        self.bridge.set_light(which_lights, command)

    def dark_green(self, which_lights=[1,2,3,4]):
        command = {'on': True, 'hue': 25058, 'sat': 254, 'bri': 93}
        self.bridge.set_light(which_lights, command)

    def yellow(self, which_lights=[1,2,3,4]):
        command = {'on': True, 'hue': 19275, 'sat': 254, 'bri': 254}
        self.bridge.set_light(which_lights, command)

    def orange(self, which_lights=[1,2,3,4]):
        command = {'on': True, 'hue': 5783, 'sat': 254, 'bri': 254}
        self.bridge.set_light(which_lights, command)


    def field_goal(self):
        for cycle in xrange(20):
            next_color = self.colors[self.colorKeys[cycle % 2]]
            self.bridge.set_light([1, 2, 3, 4], 'xy', next_color, transitiontime=2.5)

    def touchdown(self, team):
        for cycle in xrange(40):
            # on each cycle, each light goes to the next color, which is
            # either bleu, white or red.
	    team.show_team_color(cycle % 2 == 1)
            # self.bridge.set_light((cycle + 1) % 4 + 1, 'on', False)
	    # self.bridge.set_light(cycle % 4 + 1, 'on', True)
            next_color = self.colors[self.colorKeys[cycle % 3]]
            self.bridge.set_light([1, 2, 3, 4], 'xy', next_color, transitiontime=2.5)
            sleep(1)


def main():
    parser = argparse.ArgumentParser(description='Use Hue lights in coordination with an NFL game')

    parser.add_argument('--cfb', dest='cfb', action='store_true', help='specify if you wanted to track a college footbal game')
    parser.add_argument('--conf', dest='conf', help='Conference of the team')
    parser.add_argument('--gameId', dest='gameId', help='ID of the NFL game to track')
    parser.add_argument('--quiet', dest='quiet', action='store_true', help='quiet the debug output')
    args = parser.parse_args()

    game_tracker = NFLGameTracker
    if args.cfb:
        game_tracker = CFBGameTracker

    if not args.gameId:
        print 'Please select a game to track:'
        game_tracker.list_games(args.conf)
        return

    game = game_tracker(int(args.gameId), args.quiet != True)

    while True:
        game.update_lights()
        if game.is_end_of_game():
            break
        sleep(10)

if __name__ == "__main__":
    main()

