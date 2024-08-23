# view.py
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass
from tkinter import Canvas
from typing import Literal

import customtkinter as ctk
from PIL import Image, ImageTk

from settings import *


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


class StopWatchView(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=BLACK)
        self.buttons_frame = None
        self.clock = None
        self.lap_frame = None

        # Window setup
        ctk.set_appearance_mode('dark')
        self.title('')
        self.geometry('300x600')
        self.iconbitmap('assets/empty.ico')
        self.resizable(False, False)

        self.change_title_bar_color()
        self.set_layout()
        self.create_widgets()

    def set_layout(self) -> None:
        """
        Configure the layout of the widget's grid system.

        :return: None
        """
        self.rowconfigure(0, weight=5, uniform='a')
        self.rowconfigure(1, weight=1, uniform='a')
        self.rowconfigure(2, weight=4, uniform='a')

        self.columnconfigure(0, weight=1, uniform='b')

    def create_widgets(self) -> None:
        """
        Create the main widgets.

        :return: None
        """
        self.clock = Clock(self)
        self.buttons_frame = ButtonsFrame(self)
        self.lap_frame = LapsFrame(self)

    def change_title_bar_color(self) -> None:
        """
        Changes the color of the title bar to black.
        Only works for the windows.

        :return: None
        """
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = TITLE_HEX_COLOR
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass

    def reset_app(self) -> None:
        """
        Resets the app components to the original state.

        :return: None
        """
        # Reset the clock handle
        self.clock.reset_clock_handle()
        # Reset the buttons state
        self.buttons_frame.reset()
        # Reset the laps frame
        self.lap_frame.reset_lap_frame()


class Clock(Canvas):
    def __init__(self, parent):
        super().__init__(master=parent,
                         bg=BLACK,
                         highlightthickness=0,
                         bd=0,
                         )
        self.clock_handle_tk = None
        self.canvas_height = None
        self.canvas_width = None
        self.clock_handle = None
        self.clock_img_tk = None
        self.center_y = None
        self.center_x = None
        self.text_id: None | int = None
        self.grid(row=0, column=0, sticky='nsew')

        # Runs the get_dimensions function after canvas creation
        self.bind('<Configure>', self.get_dimensions)

    def get_dimensions(self, event) -> None:
        """
        Update the canvas dimensions and create the clock based on the new size.

        :param event: The event object containing information about the resize event.
               It includes attributes like width and height of the resized widget.

        :return: None
        """
        # Get the dimensions of the canvas
        self.canvas_width: int = event.width
        self.canvas_height: int = event.height
        # Find the center point of the canvas
        self.center_x: int = self.canvas_width // 2
        self.center_y: int = self.canvas_height // 2
        # Add the clock and clock handle to the screen
        self.create_clock()

    def create_clock(self) -> None:
        """
        Create and display the clock face and handle on the canvas.

        This method performs the following tasks:
        1. Loads and resizes the clock face image.
        2. Loads, resizes, and rotates the clock handle image.
        3. Places the clock face image on the canvas.
        4. Initializes the clock handle at the 12 o'clock position.

        The method uses the canvas dimensions (self.canvas_width and self.canvas_height)
        to properly size and position the clock elements.

        Returns:
            None
        """

        # Load and resize the clock face image
        clock_img = Image.open('assets/clock_project.png').resize((self.canvas_width - 15, self.canvas_height - 15))
        self.clock_img_tk = ImageTk.PhotoImage(clock_img)
        # Load, resize, and rotate the clock handle image
        self.clock_handle = Image.open('assets/clock_handle.png')
        self.clock_handle = self.clock_handle.resize((self.canvas_width - 70, self.canvas_width - 70))
        # Rotate by 90 degrees to place it at 12 o'clock position
        self.clock_handle = self.clock_handle.rotate(90,
                                                     resample=Image.BICUBIC,
                                                     expand=True
                                                     )
        # Place the clock face image on the canvas
        self.create_image(self.center_x, self.center_y, image=self.clock_img_tk, anchor='center')
        # Initialize the clock handle at the starting position (12 o'clock)
        self.reset_clock_handle()

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
        # Rotate the clock handle image
        rotated_img = self.clock_handle.rotate(rotation_degree,
                                               resample=Image.BICUBIC,
                                               expand=True)
        # Convert the rotated image to ImageTk format for display
        self.clock_handle_tk = ImageTk.PhotoImage(rotated_img)

        # Get the formatted time text and appropriate font size
        text, font_size = format_time(elapsed_seconds)
        # Remove the previous time text from the canvas
        self.delete(self.text_id)
        # Create new time text on the canvas
        self.text_id = self.create_text(self.center_x,
                                        self.center_y + 50,
                                        text=text,
                                        fill='red',
                                        font=(TEXT_FONT, font_size, 'bold'))
        # Update the clock handle position on the canvas
        self.create_image(self.center_x, self.center_y, image=self.clock_handle_tk, anchor='center')

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


class ButtonsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='transparent')
        self.reset_button = None
        self.stop_button = None
        self.start_button = None
        self.lap_button = None

        self.grid(row=1, column=0, sticky='nsew', padx=5)
        self.set_layout()
        self.create_widgets()

    def set_layout(self) -> None:
        """
        Configure the layout of the widget's grid system.

        :return: None
        """
        self.rowconfigure(0, weight=1, uniform='a')
        self.columnconfigure((0, 1), weight=1, uniform='b')

    def create_widgets(self) -> None:
        """
        Create the buttons widgets.

        :return: None
        """
        font: tuple[str, int, str] = (FONT, BUTTON_FONT_SIZE, 'bold')
        self.lap_button = ctk.CTkButton(self,
                                        text='Lap',
                                        fg_color=GREY,
                                        text_color=ORANGE_DARK_TEXT,
                                        hover_color=ORANGE_HIGHLIGHT,
                                        font=font,
                                        text_color_disabled='#bdbdbd',
                                        state='disabled',
                                        )

        self.start_button = ctk.CTkButton(self,
                                          text='Start',
                                          fg_color=GREEN,
                                          text_color=GREEN_TEXT,
                                          hover_color=GREEN_HIGHLIGHT,
                                          font=font,
                                          )

        self.stop_button = ctk.CTkButton(self,
                                         text='Stop',
                                         fg_color=RED,
                                         text_color=RED_TEXT,
                                         hover_color=RED_HIGHLIGHT,
                                         font=font,
                                         )

        self.reset_button = ctk.CTkButton(self,
                                          text='Reset',
                                          fg_color=ORANGE_DARK,
                                          text_color=ORANGE_DARK_TEXT,
                                          hover_color=ORANGE_HIGHLIGHT,
                                          font=font,
                                          )
        # Only add start and lap buttons to the screen
        self._button_layout(enable=['start', 'lap'])

    def start(self) -> None:
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
        self._button_layout(enable=['stop', 'lap'],
                            disable=['start', 'reset'])
        # Change the state  and color of lap button
        self.lap_button.configure(state='normal', fg_color=ORANGE_DARK)
        self.start_button.configure(text='Resume')

    def stop(self) -> None:
        # When user pressed the stop button
        # Remove the stop and lap buttons from screen
        # Add the start and reset buttons
        self._button_layout(enable=['start', 'reset'],
                            disable=['stop', 'lap'])

    def reset(self) -> None:
        # When user pressed the stop button
        # Remove the reset button from screen
        # And add the lap button
        self._button_layout(enable=['lap'],
                            disable=['reset'])

        # Change the color and state of lap button
        self.lap_button.configure(state='disabled', fg_color=GREY)
        self.start_button.configure(text='Start')

    def _button_layout(self,
                       *,
                       enable: list[Literal['start', 'stop', 'lap', 'reset']] | None = None,
                       disable: list[Literal['start', 'stop', 'lap', 'reset']] | None = None
                       ) -> None:
        """
        Manage the visibility and placement of buttons.

        :param enable: List of buttons to enable and show
        :param disable: List of buttons to hide
        """

        buttons = {
            # 'button_name': (Button_object, row, column)
            'start': (self.start_button, 0, 1),
            'stop': (self.stop_button, 0, 1),
            'lap': (self.lap_button, 0, 0),
            'reset': (self.reset_button, 0, 0)
        }
        if enable:
            for button in enable:
                obj, row, col = buttons[button.lower()]
                obj.grid(row=row, column=col, sticky='nsew', padx=10)
        if disable:
            for button in disable:
                obj, _, _ = buttons[button.lower()]
                obj.grid_forget()


class LapsFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent) -> None:
        super().__init__(master=parent, fg_color='transparent')
        self.lap_number = None
        self.grid(row=2, column=0, sticky='nsew')
        self.reset_lap_frame()

    def reset_lap_frame(self) -> None:
        """
        Brings back the lap frames to its original state.
        :return: None
        """
        # Set the number of laps to 0
        self.lap_number = 0
        # Hide the scrollbar until needed
        self._scrollbar.configure(width=0)
        # Remove the previous lap objects if they exist.
        for widget in self.winfo_children():
            widget.destroy()

    def create_lap_object(self, lap_time: float) -> None:
        """
        Create a new lap object and update the lap display.

        Args:
            lap_time: The time for the current lap in seconds.
        """

        # Increment the number of laps
        self.lap_number += 1
        # If frame is large enough, bring back the scrollbar
        if self.lap_number > 4:
            self._scrollbar.configure(width=SCROLL_BAR_WIDTH)

        # Get the formatted time 
        formatted_time: str = format_time(lap_time)[0]
        # Create the lap object
        LapObject(self, self.lap_number, formatted_time)
        # Scroll to bottom after each lap is added
        self.scroll_to_bottom()

    def scroll_to_bottom(self) -> None:
        """
        Scrolls to the bottom of scrollable frame by using the
         methods of underlying canvas widget.

        :return: None
        """
        self._parent_canvas.update_idletasks()
        self._parent_canvas.yview_moveto(1)


class LapObject(ctk.CTkFrame):
    def __init__(self, parent, lap_number: int, formatted_time: str) -> None:
        super().__init__(master=parent, fg_color='transparent')
        self.lap_number = lap_number
        self.formatted_time = formatted_time

        self.pack(expand=True, fill='both', padx=5, pady=5)
        self.set_layout()
        self.create_widgets()

    def set_layout(self) -> None:
        """
        Configure the layout of the widget's grid system.

        :return: None
        """

        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure((0, 1), weight=1)

    def create_widgets(self) -> None:
        font: tuple[str, int] = (TEXT_FONT, CLOCK_FONT_SIZE_MEDIUM)
        # Add a custom frame as a separator (Only between the laps)
        if self.lap_number > 1:
            separator = ctk.CTkFrame(self, height=3, fg_color=DARK_GREY)
            separator.grid(row=0, column=0, columnspan=2, sticky='ew', pady=5, padx=5)

        # A label that shows which lap we're on
        ctk.CTkLabel(self,
                     text=f'Lap {self.lap_number}',
                     text_color=WHITE, anchor='w',
                     font=font
                     ).grid(row=1, column=0, sticky='nsew')
        # A label that shows the lap time
        ctk.CTkLabel(self,
                     text=self.formatted_time,
                     text_color=WHITE,
                     anchor='e',
                     font=font
                     ).grid(row=1, column=1, sticky='nsew')
