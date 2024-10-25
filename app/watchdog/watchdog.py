import re

from .. app import App
from . import states as states
from . import detector
from . import input

from PIL import Image
from time import sleep
import win32gui

class Watchdog(App):

    Name = "Watchdog"

    def __init__(self, cfg, hwnd):
        super().__init__(cfg, hwnd)
        self.number_pattern = re.compile('\s*(\d+)\s*')
        self.local_players = {
            'red': 0,
            'criminal': 0,
            'white': 0,
        }


    def start(self):
        super().start()


    def tick(self):
        super().tick()
        self.refresh_screen()
        self.read_local_players()
        try:
            if self.current_state is not None:
                self.current_state.update()
        except Exception as e:
            print(e)


    def refresh_screen(self):
        self.screen = detector.capture_window(self.hwnd, f"screen_{self.hwnd}.png")
        # self.screen = Image.open(f"screen_{self.hwnd}.png")


    def read_local_players(self):
        screen = self.screen
        img = detector.get_template('local_window')
        rect = detector.locate_image_rect(screen, img, 0.8)
        if rect is not None:
            rect = (rect[0], rect[1] + 300, rect[2], rect[3] + 300)
            local = screen.crop(rect)
            lp = {}
            for key in self.local_players.keys():
                rect = self.cfg['local_player_rects'].get(key)
                if rect is not None:
                    txt = detector.read_image_num(local, rect)
                    match = self.number_pattern.match(txt)
                    if match is not None:
                        lp[key] = int(match.group(1))
            self.local_players.update(lp)


    def check_avoid_players(self):
        avoid_players = self.cfg.get('avoid_players', dict)
        for key, num in self.local_players.items():
            if num > 0 and avoid_players.get(key, False):
                print(self.local_players)
                return True
        return False