# model.py
from time import time
import customtkinter as ctk


class StopWatchModel:
    def __init__(self):
        self.offset = 0
        self.clock_is_active = ctk.BooleanVar(value=False)
        self.time_stopped: None | float = None
        self.offsets: list[float] = []
        self.start_time = 0

    def get_elapsed_time(self):
        return time() - self.start_time - self.offset

    def check_for_offset(self):
        if self.time_stopped:
            now: float = time()
            self.offsets.append(now - self.time_stopped)
            self.offset = sum(self.offsets)
        else:
            self.get_start_time()

    def get_start_time(self):
        self.start_time = time()

    def get_stop_time(self):
        self.time_stopped = time()

    def reset(self):
        self.offset = 0
        self.clock_is_active = ctk.BooleanVar(value=False)
        self.time_stopped: None | float = None
        self.offsets: list[float] = []
        self.start_time = 0
