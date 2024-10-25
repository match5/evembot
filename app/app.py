import win32gui

class App:

    Name = "App"

    def __init__(self, cfg, hwnd):
        self.cfg = cfg
        self.hwnd = hwnd
        self.current_state = None


    def start(self):
        print(f"{self.Name} start {win32gui.GetWindowText(self.hwnd)} {self.hwnd}")


    def tick(self):
        pass


    def change_state(self, cls):
        if self.current_state is not None:
            self.current_state.exit()
        self.current_state = cls(self)
        self.current_state.enter()