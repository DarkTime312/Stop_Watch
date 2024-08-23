# controller.py
from PySide6.QtCore import QTimer

from model import StopWatchModel
from view import StopWatchView
from settings import *


class StopWatchController:
    def __init__(self):
        self.view = StopWatchView()
        self.model = StopWatchModel()
        self.add_functionality()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_view)
        self.timer.setInterval(REFRESH_RATE)


    def add_functionality(self) -> None:
        """
        Adds the responsible functions to the buttons.

        :return: None
        """
        self.view.ui.btn_start.clicked.connect(self.start)
        self.view.ui.btn_stop.clicked.connect(self.stop)
        self.view.ui.btn_resume.clicked.connect(self.start)
        self.view.ui.btn_reset.clicked.connect(self.reset)
        # self.view.buttons_frame.lap_button.configure(command=self.create_lap)

    def start(self) -> None:
        self.model.start_timing()
        # Handle the UI elements in start mode
        self.view.start_clicked()
        # Run the function responsible for UI updates of our clock handle.
        self.timer.start()

    def stop(self) -> None:
        self.model.pause_timing()
        self.view.stop_clicked()

    def reset(self) -> None:
        self.model.reset()
        self.view.reset_app()



    def update_view(self) -> None:
        # If clock is active get the current elapsed time and pass it to view
        # To show the updated time on the screen
        if self.model.clock_is_active:
            elapsed_time = self.model.get_elapsed_time()
            self.view.update_clock(elapsed_time)
        else:
            self.timer.stop()
