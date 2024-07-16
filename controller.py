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
        self.model.start_timing()
        # Handle the UI elements in start mode
        self.view.buttons_frame.start()
        self.update_view()

    def update_view(self):
        # If clock as active get the current elapsed time and pass it to view
        # To show the updated time on the screen
        if self.model.clock_is_active.get():
            elapsed_time = self.model.get_elapsed_time()
            self.view.clock.update_clock(elapsed_time)
            self.view.after(REFRESH_RATE, self.update_view)

    def stop(self):
        self.model.clock_is_active.set(False)
        self.model.get_stop_time()
        self.view.buttons_frame.stop()

    def reset(self):
        self.model.reset()
        self.view.reset_app()

    def create_lap(self):
        elapsed_time: float = self.model.get_elapsed_time()
        lap_time = elapsed_time - self.model.latest_lap_elapsed_time
        self.view.lap_frame.create_lap_object(lap_time)
        self.model.latest_lap_elapsed_time = elapsed_time
