"""Manage My Scorecards"""

import datetime
from typing import List

import yaml


def read_config():
    with open('settings/config.yml') as config_fp:
        config = yaml.safe_load(config_fp)
        return config


def write_config(config):
    with open('settings/config.yml', 'w') as config_fp:
        yaml.safe_dump(config, config_fp)


def do_action(action):
    if action == 'new':
        build_new_scorecard()


def build_new_scorecard():
    scorecard = Scorecard()
    scorecard.build_new()


class Scorecard:
    """Working with scorecards

    Create, add config, delete
    """

    def __init__(self):
        self.today = datetime.datetime.now()
        self.config = read_config()

    def build_new(self):
        config = {}
        print("Type the reference name (no spaces) for this item")
        config['item'] = input('-> ')
        print("Type the goal, then hit enter")
        config['goal'] = input('-> ')
        print("Type the name of the book")
        config['book'] = input('-> ')
        print("Type the name of the data file (no spaces)")
        config['data'] = f"{input('-> ')}.csv"
        print('Type the name of the authors, and q when done')
        config['authors'] = []
        while True:
            val = input('-> ')
            if val == 'q':
                break
            config['authors'].append(val)
        self.write_config(**config)

    def write_config(self, item: str, book: str, goal: str, data: str, authors:  List[str]):
        content = self.config['items'][item] = {
            'book': book,
            'goal': goal,
            'data': data,
            'authors': authors
        }
        write_config(self.config)
        # print(yaml.dump(self.config))

    def write_csv(self):
        pass


def main():

    while True:
        print("Action....")
        action = input("-> ")
        if action.startswith('q'):
            break
        else:
            do_action(action)
    print("Goodbye")


if __name__ == '__main__':
    main()
