from datetime import date
from game_tracker import GameTracker
import httplib2
import json
from colour import Color

class CFBGameTracker(GameTracker):
    def __init__(self, game_id, light_control, verbose=True):
        GameTracker.__init__(self, game_id, light_control, verbose)
        self.home_score = None
        self.away_score = None

        self.curr_date = date.today().strftime('%Y%m%d') # "20170930"
        self.cfb_date_api_url = "https://cfb-scoreboard-api.herokuapp.com/v1/date/%s" % (
            self.curr_date)

    @staticmethod
    def get_game_list():
        curr_date = date.today().strftime('%Y%m%d')  # "20170930"
        cfb_api_url = "https://cfb-scoreboard-api.herokuapp.com/v1/date/%s" % (
            curr_date)
        __resp, content = httplib2.Http().request(cfb_api_url)

        req_json = json.loads(content)
        return req_json[u'games']

    @staticmethod
    def list_games(conference=None):
        all_games = CFBGameTracker.get_game_list()
        for game in all_games:
            if conference and (conference != game['homeTeam'][u'conference'][u'abbreviation'] or \
               conference != game['awayTeam'][u'conference'][u'abbreviation']):
                continue
            home_rank = '(' + str(game['homeTeam']['rank']) + \
                ') ' if game['homeTeam']['rank'] <= 25 else ''
            away_rank = '(' + str(game['awayTeam']['rank']) + \
                ') ' if game['awayTeam']['rank'] <= 25 else ''
            # print game
            print "%d) %s%s vs %s%s" % (x, home_rank, game[u'homeTeam'][u'displayName'], away_rank, game[u'awayTeam'][u'displayName'])

    def change_lights_based_on_score_type(self, score_type, color, which_lights):
        """ Change the lighting based on what is happening in the football game """
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

    def track_game(self):
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
        self.change_lights_based_on_score_type(
            home_score_type, Color('#' + game['homeTeam']['color']), [1, 3])
        self.change_lights_based_on_score_type(
            away_score_type, Color('#' + game['awayTeam']['color']), [2, 4])

    def is_end_of_game(self):
        return self.end_of_game
