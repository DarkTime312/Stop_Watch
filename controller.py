# controller.py
from model import StopWatchModel
from view import StopWatchView
from settings import *


class StopWatchController:
    def __init__(self):
        self.view = StopWatchView()
        self.model = StopWatchModel()
        self.add_functionality()
        self.view.mainloop()

    def add_functionality(self):
        self.view.buttons_frame.start_button.configure(command=self.start)
        self.view.buttons_frame.stop_button.configure(command=self.stop)
        self.view.buttons_frame.reset_button.configure(command=self.reset)
        self.view.buttons_frame.lap_button.configure(command=self.create_lap)

    def start(self):
        self.model.clock_is_active.set(True)
        self.view.buttons_frame.start()
        self.model.check_for_offset()
        # self.model.get_start_time()
        self.update_view()
        print('start pressed')

    def update_view(self):
        if self.model.clock_is_active.get():
            elapsed_time = self.model.get_elapsed_time()
            self.view.clock.update_clock(elapsed_time)
            self.view.after(REFRESH_RATE, self.update_view)

    def stop(self):
        print('stopped')
        self.model.clock_is_active.set(False)
        self.model.get_stop_time()
        self.view.buttons_frame.stop()

    def reset(self):
        print('reset')
        self.model.reset()
        # self.view.initialize()
        self.view.reset()
        # self.add_functionality()

    def create_lap(self):
        elapsed_time = self.model.get_elapsed_time()
        self.view.lap_frame.create_lap_object(elapsed_time)


if __name__ == '__main__':
    StopWatchController()
