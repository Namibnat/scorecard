"""Manage My Scorecards"""

import csv
import datetime
import os
import sys
from typing import List

import pandas as pd
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
        csv_data = {}
        print("Type the reference name (no spaces) for this item")
        reference_name = input('-> ')
        config['item'] = reference_name
        print("Type the goal, then hit enter")
        config['goal'] = input('-> ')
        print("Type the name of the book")
        config['book'] = input('-> ')
        print("Type the name of the data file (no spaces)")
        config['data'] = f"{input('-> ')}.csv"
        if " " in config['data']:
            raise ValueError("Error: space in filename")
        print('Type the name of the authors, and q when done')
        config['authors'] = []
        while True:
            val = input('-> ')
            if val == 'q':
                break
            config['authors'].append(val)
        self.write_config(**config)
        print("Config file written")
        print("Type the start date, in the format dd/mm/yyyy")
        csv_data['date'] = datetime.datetime.strptime(
            input('-> '), "%d/%m/%Y")
        print("Type the end date")
        csv_data['end_date'] = datetime.datetime.strptime(
            input('-> '), "%d/%m/%Y")
        print("Type the start page or chunk")
        csv_data['page'] = int(input('-> '))
        print("Type the end page or chunk")
        csv_data['end_page'] = int(input('-> '))
        if csv_data['end_page'] <= csv_data['page']:
            raise ValueError("Error: end page must be greater than start page")
        self.write_csv(reference_name=reference_name, **csv_data)
        print("Done!")

    def write_config(self, item: str, book: str, goal: str, data: str, authors:  List[str]):
        if self.config['spaced'] is None:
            self.config['spaced'] = {}
        self.config['spaced'][item] = {
            'book': book,
            'goal': goal,
            'data': data,
            'authors': authors
        }
        write_config(self.config)

    def write_csv(self, reference_name: str, date: datetime, end_date: datetime, page: int, end_page: int):
        df = pd.DataFrame(columns=['line', 'date', 'achieved', 'target'])
        line = 1
        # pages = (end_page - page)/(end_date-date).days
        while True:
            end = (date.year == end_date.year) and (date.month == end_date.month) and (date.day == end_date.day)
            df.loc[line] = [line, date.strftime("%d/%m/%Y"), 0, page]
            line += 1
            if end:
                page = end_page
            else:
                page += (end_page - page)/(end_date-date).days
            page = int(round(page, 0))
            date += datetime.timedelta(days=1)
            if end:
                break
        df.to_csv(f"data/{reference_name}.csv", index=False, sep='|')


def main():

    while True:
        print("Action....")
        action = input("-> ")
        if action.startswith('q'):
            break
        else:
            do_action(action)
    print("Goodbye")


def clear_console():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)


if __name__ == '__main__':
    clear_console()
    main()
