import sys
import json
import win32gui
from time import sleep

# from app.bot import bot
from app.watchdog import watchdog

config_path = 'config.json'
config = dict()


def load_config():
    print ('load config form %s' % config_path)
    with open(config_path, 'r', encoding='utf-8') as file:
        config.update(json.load(file))


def find_windows(titles):
    hwnds = set()
    for title in titles:
        hwnd = None
        while(True):
            hwnd = win32gui.FindWindowEx(None, hwnd, None, title)
            if hwnd == 0 or hwnd in hwnds:
                break
            hwnds.add(hwnd)
    return hwnds
    


if __name__ == '__main__':
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    load_config()
    
    hwnds = find_windows(config.get("window_titles", list))

    if (len(hwnds) > 0):
        apps = []
        for hwnd in hwnds:
            # app = bot.Bot(config, hwnd)
            app = watchdog.Watchdog(config, hwnd)
            app.start()
            apps.append(app)

        frame_interval = config.get('frame_interval', float)
        tick_interval = frame_interval / len(apps)
        while(True):
            for app in apps:
                sleep(tick_interval)
                app.tick()
