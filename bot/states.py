from hashlib import new
from time import time as now
from time import sleep
import re

from . import detector
from . import input

class BotState:


    def __init__(self, bot):
        self.bot = bot


    def enter(self):
        print('%s enter' % self.__class__.__name__)


    def exit(self):
        pass


    def update(self):
        pass



class FindEnemy(BotState):


    def enter(self):
        super().enter()
        self.exit_time = self.bot.cfg.get('find_enemy_time', float) + now()


    def update(self):
        if self.bot.check_avoid_players():
            self.bot.change_state(Escape)
            return
        if self.bot.check_enemy():
            self.bot.change_state(Fight)
            return
        elif now() > self.exit_time:
            self.bot.change_state(WarpToSpot)
            return
        self.bot.refresh_ship_status()
        self.bot.active_equipments()



class WarpToSpot(BotState):


    def __init__(self, bot):
        super().__init__(bot)
        self.exit_time = None


    def enter(self):
        super().enter()
        if self.warp_to_spot():
            self.exit_time = self.bot.cfg.get('warp_time', float) + now()


    def update(self):
        if self.exit_time and now() > self.exit_time:
            self.bot.change_state(FindEnemy)
        if self.exit_time is None:
            if self.warp_to_spot():
                self.exit_time = self.bot.cfg.get('warp_time', float) + now()


    def warp_to_spot(self):
        if self.bot.switch_overview('spot'):
            self.bot.refresh_screen()
            items = self.bot.read_overview_items()
            filters = self.bot.cfg.get('spot_filter', None)
            if filters is not None:
                new_items = []
                for filter in filters:
                    new_items += [it for it in items if it[0].find(filter) >= 0]
                new_items.sort(key=lambda a : a[1][1])
                items = new_items
            if items:
                it = items[len(items) - 1]
                input.mouse_click_left(self.bot.hwnd, it[1][0], it[1][1])
                sleep(self.bot.cfg.get('ui_sleep_time', float))
                pos = detector.locate_image(
                    detector.capture_window(self.bot.hwnd),
                    detector.get_template('btn_warp'),
                    0.8
                )
                if pos is not None:
                    input.mouse_click_left(self.bot.hwnd, pos[0], pos[1])
                    return True
        return False



class Fight(BotState):


    def __init__(self, bot):
        super().__init__(bot)
        self.exit_time = None


    def update(self):
        if self.bot.check_avoid_players():
            self.bot.change_state(Escape)
            return
        if not self.lock_on_all() and not self.bot.check_enemy():
            if self.exit_time is None:
                self.exit_time = self.bot.cfg.get('fight_wait_time', float) + now()
        else:
            self.exit_time = None

        if self.exit_time and now() > self.exit_time:
                self.bot.change_state(FindEnemy)
                return
        self.bot.refresh_ship_status()
        self.bot.active_equipments()


    def lock_on_all(self):
        pos = detector.locate_image(
            self.bot.screen,
            detector.get_template('btn_lock_on'),
            0.7
        )
        if pos is not None:
            input.mouse_click_left(self.bot.hwnd, pos[0], pos[1])
            sleep(self.bot.cfg.get('ui_sleep_time', float))
            return True
        return False





class Escape(BotState):


    def __init__(self, bot):
        super().__init__(bot)
        self.exit_time = None


    def enter(self):
        super().enter()
        self.approach_to_station()


    def update(self):
        if self.exit_time and now() > self.exit_time:
            self.bot.change_state(FindEnemy)
            return
        self.bot.refresh_ship_status()
        self.bot.active_equipments()
        if self.exit_time is None:
            if self.warp_to_station():
                self.exit_time = self.bot.cfg.get('escape_wait_time', float) + now()
        elif self.bot.check_avoid_players():
            self.exit_time = self.bot.cfg.get('escape_wait_time', float) + now()


    def approach_to_station(self):
        if self.bot.switch_overview('station') or self.bot.switch_overview('fortress') or self.bot.switch_overview('gate'):
            self.bot.refresh_screen()
            items = self.bot.read_overview_items(1)
            if items:
                it = items[0]
                input.mouse_click_left(self.bot.hwnd, it[1][0], it[1][1])
                sleep(self.bot.cfg.get('ui_sleep_time', float))
                pos = detector.locate_image(
                    detector.capture_window(self.bot.hwnd),
                    detector.get_template('btn_approach'),
                    0.8
                )
                if pos is not None:
                    input.mouse_click_left(self.bot.hwnd, pos[0], pos[1])
                    return True
        return False


    def warp_to_station(self):
        if self.bot.switch_overview('station') or self.bot.switch_overview('fortress') or self.bot.switch_overview('gate'):
            self.bot.refresh_screen()
            items = self.bot.read_overview_items(1)
            if items:
                it = items[0]
                input.mouse_click_left(self.bot.hwnd, it[1][0], it[1][1])
                sleep(self.bot.cfg.get('ui_sleep_time', float))
                pos = detector.locate_image(
                    detector.capture_window(self.bot.hwnd),
                    detector.get_template('btn_warp'),
                    0.8
                )
                if pos is not None:
                    input.mouse_click_left(self.bot.hwnd, pos[0], pos[1])
                    return True
        return False