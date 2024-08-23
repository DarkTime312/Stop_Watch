# view.py
from PySide6.QtCore import QFile, Qt, QSize, QTimer
from PySide6.QtGui import QImage, QTransform, QPixmap, QColor, QPalette, QFont
from PySide6.QtWidgets import QWidget
from typing import Literal
import time
from PIL import Image, ImageTk
from datetime import datetime
from settings import *
from ui_ui import Ui_mainwindow
from hPyT import *


def format_time(total_seconds: float) -> tuple[str, int]:
    """
    Format the given time in seconds into a human-readable string and determine the appropriate font size.

    This function takes a time duration in seconds and formats it into a string representation
    with different levels of precision based on the magnitude of the time. It also returns
    an appropriate font size for displaying the formatted time.

    Args:
        total_seconds (float): The total number of seconds to be formatted.

    Returns:
        tuple[str, int]: A tuple containing two elements:
            - str: The formatted time string.
            - int: The recommended font size for displaying the time.

    The function handles three different time ranges:
    1. Less than 1 minute: Format as "SS.ss" (seconds with centiseconds)
    2. 1 minute to 1 hour: Format as "MM:SS.ss" (minutes, seconds, and centiseconds)
    3. 1 hour or more: Format as "HH:MM:SS.ss" (hours, minutes, seconds, and centiseconds)
    """
    # For times less than 1 minute
    if total_seconds < SECONDS_IN_MINUTE:
        # Split the time into seconds and milliseconds
        total_seconds, milliseconds = divmod(total_seconds, 1)
        # Format as "SS.ss"
        output_text: str = f"{int(total_seconds):02}.{int(milliseconds * 100):02}"
        font_size: int = CLOCK_FONT_SIZE_LARGE
    # For times between 1 minute and 1 hour
    elif total_seconds < SECONDS_IN_HOUR:
        # Calculate minutes and remaining seconds
        minutes, remainder = divmod(total_seconds, 60)
        total_seconds, milliseconds = divmod(remainder, 1)
        # Format as "MM:SS.ss"
        output_text: str = f"{int(minutes):02}:{int(total_seconds):02}.{int(milliseconds * 100):02}"
        font_size: int = CLOCK_FONT_SIZE_MEDIUM
    # For times of 1 hour or more
    else:
        # Calculate hours, minutes, and remaining seconds
        hours, remainder = divmod(total_seconds, 3600)
        minutes, remainder = divmod(remainder, 60)
        total_seconds, milliseconds = divmod(remainder, 1)
        # Format as "HH:MM:SS.ss"
        output_text: str = f"{int(hours):02}:{int(minutes):02}:{int(total_seconds):02}.{int(milliseconds * 100):02}"
        font_size: int = CLOCK_FONT_SIZE_SMALL
    return output_text, font_size


class StopWatchView(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = Ui_mainwindow()
        self.ui.setupUi(self)
        self.load_image()

        # self.timer.start()
        self.update_clock(0)
        self.activate_buttons(['start', 'lap'], lap_disabled=True)

        # Window setup
        self.setWindowTitle(' ')
        self.change_title_bar_color()

    def load_image(self):
        # Load the image from QRC
        self.clock_handle_pillow = Image.fromqimage(QImage(':assets/clock_handle.png')).resize((200, 200)).rotate(90)

    def run_test(self):
        self.update_clock(time.time())

    def change_title_bar_color(self) -> None:
        """
        Changes the color of the title bar to black.
        Only works for the windows.

        :return: None
        """
        window_palette = self.palette()
        window_palette.setColor(QPalette.ColorRole.Window, QColor('#000000'))
        self.setPalette(window_palette)
        title_bar_color.set(self, '#000000')  # sets the titlebar color to white

    def reset_app(self) -> None:
        """
        Resets the app components to the original state.

        :return: None
        """
        # Reset the clock handle
        self.reset_clock_handle()
        self.reset_clicked()

    def update_clock(self, elapsed_seconds: float) -> None:
        """
        Update the clock display based on the elapsed time.

        This method performs the following tasks:
        1. Rotates the clock handle based on the elapsed time.
        2. Updates the digital time display.
        3. Redraws the clock handle on the canvas.

        Args:
            elapsed_seconds (float): The total number of seconds elapsed since the timer started.

        Returns:
            None

        Note:
            - The clock handle rotates clockwise, with each second corresponding to 6 degrees of rotation.
            - The digital time display format and font size are determined by the format_time function.
            - This method should be called periodically to update the clock display.
        """

        # Calculate the rotation angle for the clock handle
        # Negative value ensures clockwise rotation
        rotation_degree: float = elapsed_seconds * -6

        self.ui.lbl_clock_handle.setPixmap(
            self.clock_handle_pillow.rotate(rotation_degree, resample=Image.BICUBIC).toqpixmap())

        # Get the formatted time text and appropriate font size
        text, font_size = format_time(elapsed_seconds)
        self.ui.lbl_time.setText(text)
        self.ui.lbl_time.setFont(QFont(FONT, font_size, QFont.Weight.Bold))

    def reset_clock_handle(self) -> None:
        """
        Reset the clock handle to its initial position.

        This method resets the clock display to show 0 seconds elapsed. It performs the following actions:
        1. Calls the update_clock method with 0 seconds as the argument.
        2. This effectively rotates the clock handle back to the 12 o'clock position.
        3. Resets the digital time display to show 00.00.

        This method is typically called when:
        - The stopwatch is reset to zero.
        - The clock is initially created and needs to be set to its starting position.

        Returns:
            None

        Note:
            This method relies on the update_clock method to perform the actual update of the clock display.
        """
        # Reset the position of clock handle to 0 seconds
        self.update_clock(0)

    def activate_buttons(self,
                         button_list: list[Literal['start', 'resume', 'stop', 'lap', 'reset']],
                         *,
                         lap_disabled: bool | None = None
                         ) -> None:
        """
        Manage the visibility and placement of buttons.

        :param button_list: List of buttons to enable and show
        :param lap_disabled: state of lap button
        """

        buttons = {
            # 'button_name': (Button_object, stacked_widget, index)
            'start': (self.ui.btn_start, self.ui.stacked_widget_right, 0),
            'resume': (self.ui.btn_resume, self.ui.stacked_widget_right, 1),
            'stop': (self.ui.btn_stop, self.ui.stacked_widget_right, 2),
            'lap': (self.ui.btn_lap, self.ui.stacked_widget_left, 0),
            'reset': (self.ui.btn_reset, self.ui.stacked_widget_left, 1)
        }
        for button in button_list:
            obj, stacked_widget, idx = buttons[button.lower()]
            stacked_widget.setCurrentIndex(idx)

        if lap_disabled is not None:
            self.ui.btn_lap.setDisabled(True if lap_disabled else False)

    def start_clicked(self) -> None:
        """
        Initiate or resume the stopwatch.

        Updates UI for running state:
        - Enables 'stop' and 'lap' buttons
        - Disables 'start' and 'reset' buttons
        - Activates lap button
        - Changes start button text to 'Resume'
        """

        # When user pressed the start button
        # Remove the start and reset buttons from screen
        # And add the stop and lap buttons
        self.activate_buttons(['stop', 'lap'], lap_disabled=False)

    def stop_clicked(self) -> None:
        # When user pressed the stop button
        # Remove the stop and lap buttons from screen
        # Add the start and reset buttons
        self.activate_buttons(['resume', 'reset'])

    def reset_clicked(self) -> None:
        # When user pressed the stop button
        # Remove the reset button from screen
        # And add the lap button
        self.activate_buttons(['start', 'lap'], lap_disabled=True)
