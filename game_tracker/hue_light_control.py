import math
from time import sleep
from phue import Bridge

class HueLightControl(object):
    def __init__(self, ip_addr):
        self.bridge = Bridge(ip_addr)

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
        self.color_converter = {
            'blue': self.blue,
            'light blue': self.light_blue,
            'orange': self.orange,
            'red': self.red,
            'dark red': self.dark_red,
            'light green': self.light_green,
            'dark green': self.dark_green,
            'yellow': self.yellow,
            'silver': self.silver,
            'purple': self.purple,
            'gold': self.gold,
            'brown': self.brown,
            'black': self.black,
            'white': self.white,
            'dark blue': self.dark_blue,
        }

    def convert_color(self, color_name):
        return self.color_converter[color_name]

    def show_color(self, color_name):
        color = self.convert_color(color_name)
        color()

    def alternate_flashing_colors(self, color1_name, color2_name):
        color1 = self.convert_color(color1_name)
        color2 = self.convert_color(color2_name)
        for num in xrange(6):
            if num % 2 == 1:
                color1([1,3])
                color2([2,4])
            else:
                color2([1,3])
                color1([2,4])
            sleep(5)

    # This is based on original code from http://stackoverflow.com/a/22649803
    def EnhanceColor(self, normalized):
        if normalized > 0.04045:
            return math.pow((normalized + 0.055) / (1.0 + 0.055), 2.4)
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