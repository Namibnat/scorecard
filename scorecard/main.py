"""Manage My Scorecards"""

import yaml

def read_config():
    with open('settings/config.yml') as config_fp:
        config = yaml.safe_load(config_fp)
        return config


def main():
    config = read_config()
    items = config['items']
    for item in items:
        print(f"*** {item} ***")
        print(f"book: {items[item]['book']}")
        print(items[item]['goal'])
        print()


if __name__ == '__main__':
    main()