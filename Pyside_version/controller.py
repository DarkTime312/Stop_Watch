# controller.py
from model import StopWatchModel
from view import StopWatchView
from settings import *


class StopWatchController:
    def __init__(self):
        self.view = StopWatchView()
