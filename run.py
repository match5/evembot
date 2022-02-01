import sys
import json

from bot import bot, detector

config_path = 'config.json'
config = dict()


def load_config():
    print ('load config form %s' % config_path)
    with open(config_path, 'r', encoding='utf-8') as file:
        config.update(json.load(file))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    load_config()
    bot.Bot(config).run()