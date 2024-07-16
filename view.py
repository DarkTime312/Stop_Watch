# view.py
import customtkinter as ctk
from tkinter import Canvas
from PIL import Image, ImageTk
from settings import *

try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass


def format_time(total_seconds: float) -> tuple[str, int]:
    if total_seconds < SECONDS_IN_MINUTE:
        total_seconds, milliseconds = divmod(total_seconds, 1)
        output_text: str = f"{int(total_seconds):02}.{int(milliseconds * 100):02}"
        font_size: int = CLOCK_FONT_SIZE
    elif total_seconds < SECONDS_IN_HOUR:
        minutes, remainder = divmod(total_seconds, 60)
        total_seconds, milliseconds = divmod(remainder, 1)
        output_text: str = f"{int(minutes):02}:{int(total_seconds):02}.{int(milliseconds * 100):02}"
        font_size: int = CLOCK_FONT_SIZE - 4
    else:
        hours, remainder = divmod(total_seconds, 3600)
        minutes, remainder = divmod(remainder, 60)
        total_seconds, milliseconds = divmod(remainder, 1)
        output_text: str = f"{int(hours):02}:{int(minutes):02}:{int(total_seconds):02}.{int(milliseconds * 100):02}"
        font_size: int = CLOCK_FONT_SIZE - 7
    return output_text, font_size


class StopWatchView(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=BLACK)
        self.buttons_frame = None
        self.clock = None
        self.lap_frame = None
        ctk.set_appearance_mode('dark')
        # Window setup
        self.title('')
        self.geometry('300x600')
        self.iconbitmap('assets/empty.ico')
        self.resizable(False, False)

        self.change_title_bar_color()
        self.set_layout()
        self.create_widgets()

    def create_widgets(self):
        self.lap_frame = LapsFrame(self)
        self.clock = Clock(self)
        self.buttons_frame = ButtonsFrame(self)

    def change_title_bar_color(self):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = TITLE_HEX_COLOR
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass

    def set_layout(self):
        self.rowconfigure(0, weight=5, uniform='a')
        self.rowconfigure(1, weight=1, uniform='a')
        self.rowconfigure(2, weight=4, uniform='a')

        self.columnconfigure(0, weight=1, uniform='b')

    def reset_app(self):
        # Reset the clock handle
        self.clock.reset_clock_handle()
        # Reset the laps
        self.lap_frame.reset_lap_frame()
        # Reset the buttons state
        self.buttons_frame.reset()


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
        self.grid(row=0, column=0, sticky='nsew')
        self.text_id: None | int = None

        self.bind('<Configure>', self.get_dimensions)

    def get_dimensions(self, event):
        # Get the dimensions of the canvas
        self.canvas_width: int = event.width
        self.canvas_height: int = event.height
        # Find the center point of the canvas
        self.center_x: int = self.canvas_width // 2
        self.center_y: int = self.canvas_height // 2
        # add the clock and clock handle to the screen
        self.create_clock()

    def create_clock(self):
        # Resize the clock picture and convert it to ImageTk
        clock_img = Image.open('assets/clock_project.png').resize((self.canvas_width - 15, self.canvas_height - 15))
        self.clock_img_tk = ImageTk.PhotoImage(clock_img)
        # Resize the clock handle photo and then rotate it 90 degrees
        # To place it at 12 O'clock
        self.clock_handle = Image.open('assets/clock_handle.png')
        self.clock_handle = self.clock_handle.resize((self.canvas_width - 70, self.canvas_width - 70))
        self.clock_handle = self.clock_handle.rotate(90,
                                                     resample=Image.BICUBIC,
                                                     expand=True
                                                     )
        # Place the clock picture on the screen
        self.create_image(self.center_x, self.center_y, image=self.clock_img_tk, anchor='center')
        # Place the clock handle at start position
        self.reset_clock_handle()

    def update_clock(self, elapsed_seconds: float) -> None:
        # Rotate the handle image based on the elapsed time
        # Each second equals to 6 degrees
        # Had to be negative number to achieve the clockwise rotation
        rotation_degree: float = elapsed_seconds * -6
        rotated_img = self.clock_handle.rotate(rotation_degree,
                                               resample=Image.BICUBIC,
                                               expand=True)
        # Convert the image to ImageTk
        self.clock_handle_tk = ImageTk.PhotoImage(rotated_img)

        # Get the font size and formated text for the elapsed time label
        text, font_size = format_time(elapsed_seconds)
        # Delete the previous label
        self.delete(self.text_id)
        # Place the text on the screen
        self.text_id = self.create_text(self.center_x,
                                        self.center_y + 50,
                                        text=text,
                                        fill='red',
                                        font=(TEXT_FONT, font_size, 'bold'))
        # Update the clock handle position
        self.create_image(self.center_x, self.center_y, image=self.clock_handle_tk, anchor='center')

    def reset_clock_handle(self):
        # Reset the position of clock handle
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
        self.rowconfigure(0, weight=1, uniform='a')
        self.columnconfigure((0, 1), weight=1, uniform='b')

    def create_widgets(self) -> None:
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
        self.lap_button.grid(row=0, column=0, sticky='nsew', padx=10)
        self.start_button.grid(row=0, column=1, sticky='nsew', padx=10)

    def start(self) -> None:
        # When user pressed the start button
        # Remove the start and reset buttons from screen
        self.start_button.grid_forget()
        self.reset_button.grid_forget()
        # Add the stop and lap buttons
        self.stop_button.grid(row=0, column=1, sticky='nsew', padx=10)
        self.lap_button.grid(row=0, column=0, sticky='nsew', padx=10)
        # Change the state  and color of lap button
        self.lap_button.configure(state='normal', fg_color=ORANGE_DARK)

    #
    def stop(self) -> None:
        # When user pressed the stop button
        # Remove the stop and lap buttons from screen
        self.stop_button.grid_forget()
        self.lap_button.grid_forget()
        # Add the start and reset buttons
        self.start_button.grid(row=0, column=1, sticky='nsew', padx=10)
        self.reset_button.grid(row=0, column=0, sticky='nsew', padx=10)

    def reset(self) -> None:
        # When user pressed the stop button
        # Remove the reset button from screen
        self.reset_button.grid_forget()
        # Add the lap button
        self.lap_button.grid(row=0, column=0, sticky='nsew', padx=10)
        # Change the color and state of lap button
        self.lap_button.configure(state='disabled', fg_color=GREY)


class LapsFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent) -> None:
        super().__init__(master=parent, fg_color='transparent')
        self.lap_number = None
        self.grid(row=2, column=0, sticky='nsew')
        self.reset_lap_frame()

    def reset_lap_frame(self) -> None:
        # Set the number of laps to 0
        self.lap_number = 0
        # Hide the scrollbar until needed
        self._scrollbar.configure(width=0)
        # Remove the previous lap objects if they exist.
        for widget in self.winfo_children():
            widget.destroy()

    def create_lap_object(self, lap_time: float) -> None:
        # Increment the number of laps
        self.lap_number += 1
        # If frame is large enough, bring back the scrollbar
        if self.lap_number > 5:
            self._scrollbar.configure(width=16)

        # Get the formatted time 
        formatted_time: str = format_time(lap_time)[0]
        # Create the lap object
        LapObject(self, self.lap_number, formatted_time)


class LapObject(ctk.CTkFrame):
    def __init__(self, parent, lap_number: int, formatted_time: str) -> None:
        super().__init__(master=parent, fg_color='transparent')
        self.lap_number = lap_number
        self.formatted_time = formatted_time

        self.pack(expand=True, fill='both', padx=5, pady=5)
        self.set_layout()
        self.create_widgets()

    def set_layout(self) -> None:
        self.rowconfigure(0, weight=1, uniform='a')
        self.columnconfigure((0, 1), weight=1, uniform='b')

    def create_widgets(self) -> None:
        font: tuple[str, int] = (TEXT_FONT, CLOCK_FONT_SIZE)
        # A label that shows which lap we're on
        ctk.CTkLabel(self,
                     text=f'Lap {self.lap_number}',
                     text_color=WHITE, anchor='w',
                     font=font
                     ).grid(row=0, column=0, sticky='nsew')
        # A label that shows the lap time
        ctk.CTkLabel(self,
                     text=self.formatted_time,
                     text_color=WHITE,
                     anchor='e',
                     font=font
                     ).grid(row=0, column=1, sticky='nsew')
