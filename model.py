# model.py
from time import time
import customtkinter as ctk


class StopWatchModel:
    def __init__(self):
        self.clock_is_active = ctk.BooleanVar(value=False)
        self.stop_time: None | float = None
        self.start_time = 0
        self.total_offset_time: float = 0
        self.latest_lap_elapsed_time = 0

    def get_elapsed_time(self) -> float:
        """
        Calculates elapsed time since user started timing.
        It will ignore any time spent in paused mode.

        :return: Total elapsed time as seconds
        """
        return time() - self.start_time - self.total_offset_time

    def start_timing(self):
        # If user already paused before
        if self.stop_time:
            # Update the offset time
            offset = time() - self.stop_time
            self.total_offset_time += offset
        # If timing for the first time
        else:
            # Update the start time
            self.get_start_time()
        # Set the state of clock as active
        self.clock_is_active.set(True)

    def get_start_time(self):
        self.start_time = time()

    def get_stop_time(self):
        self.stop_time = time()

    def reset(self):
        self.total_offset_time = 0
        self.clock_is_active = ctk.BooleanVar(value=False)
        self.stop_time: None | float = None
        self.start_time = 0
        self.latest_lap_elapsed_time = 0
