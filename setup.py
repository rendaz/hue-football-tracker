""" Handle setting up a game tracker """

from setuptools import setup

setup(name='footballgametracker',
      version='0.1',
      description=open('README.md').read(),
      url='https://github.com/rendaz/hue-football-tracker',
      author='Xander Dale',
      author_email='rendaz@gmail.com',
      license='MIT',
      packages=['game_tracker'],
      install_requires=[
          'nflgame',
          'httplib2',
          'phue',
          'colour',
      ],
      zip_safe=False)
