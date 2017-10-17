""" Handle Game tracker CLI input """

import argparse
import logging
from game_tracker_factory import FootballTrackerFactory
from hue_light_control import HueLightControl
logging.basicConfig()

def main():
    """ Handle CLI requests to track lights"""
    parser = argparse.ArgumentParser(description='Use Hue lights in coordination with an NFL game')

    parser.add_argument('--cfb', dest='cfb', action='store_true',
                        help='specify if you wanted to track a college footbal game')
    parser.add_argument('--conf', dest='conf', help='Conference of the team')
    parser.add_argument('--gameId', dest='gameId', help='ID of the NFL game to track')
    parser.add_argument('--quiet', dest='quiet', action='store_true', help='quiet the debug output')
    args = parser.parse_args()

    game_tracker_type = 'cfb' if args.cfb else 'nfl'
    game_tracker = FootballTrackerFactory.factory(game_tracker_type)

    ip_addr = '172.16.1.41'

    if not args.gameId:
        print 'Please select a game to track:'
        game_tracker.list_games(args.conf)
        return

    light_controller = HueLightControl(ip_addr)

    game = game_tracker(int(args.gameId), light_controller, args.quiet != True)
    game.track_game()

if __name__ == "__main__":
    main()
