# model.py
from time import time

import customtkinter as ctk


class StopWatchModel:
    def __init__(self):
        self.clock_is_active = ctk.BooleanVar(value=False)
        self.start_time: float = 0
        self.pause_time: None | float = None
        self.total_offset_time: float = 0
        self.previous_lap_elapsed_time: float = 0

    def get_elapsed_time(self) -> float:
        """
        Calculates elapsed time since user started timing.
        It will ignore any time spent in paused mode.

        :return: Total elapsed time as seconds
        """
        return time() - self.start_time - self.total_offset_time

    def start_timing(self) -> None:
        # If user already paused before
        if self.pause_time:
            # Calculate the current offset
            offset = time() - self.pause_time
            # And add it to the total offset
            self.total_offset_time += offset
        # If timing for the first time
        else:
            # Save the start time
            self.start_time = time()
        # Set the state of clock as active
        self.clock_is_active.set(True)

    def pause_timing(self) -> None:
        # Set the clock state to not active
        self.clock_is_active.set(False)
        # Storing the time which user paused
        # This will be used to calculate the offset when user resumes.
        self.pause_time = time()

    def reset(self) -> None:
        """
        Resets all the app data to original state.

        :return: None
        """
        self.total_offset_time = 0
        self.clock_is_active.set(False)
        self.pause_time: None | float = None
        self.start_time = 0
        self.previous_lap_elapsed_time = 0
