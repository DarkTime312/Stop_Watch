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
    if total_seconds < 60:
        total_seconds, milliseconds = divmod(total_seconds, 1)
        output_text: str = f"{int(total_seconds):02}.{int(milliseconds * 100):02}"
        font_size: int = CLOCK_FONT_SIZE
    elif total_seconds < 3600:
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

    def reset(self):
        self.clock.update_clock(0)
        self.lap_frame.destroy()
        self.lap_frame = LapsFrame(self)
        self.buttons_frame.reset()


class Clock(Canvas):
    def __init__(self, parent):
        super().__init__(master=parent,
                         bg=BLACK,
                         highlightthickness=0,
                         bd=0,
                         )
        self.grid(row=0, column=0, sticky='nsew')
        self.text_id: None | int = None

        self.bind('<Configure>', self.configure_window)

    def configure_window(self, event):
        canvas_width: int = event.width
        canvas_height: int = event.height

        self.center_x: int = canvas_width // 2
        self.center_y: int = canvas_height // 2
        self.create_clock()

    def create_clock(self):
        self.clock_img = ImageTk.PhotoImage(Image.open('assets/clock_project.png').resize((285, 285)))
        self.clock_handle = Image.open('assets/clock_handle.png')
        self.clock_handle = self.clock_handle.resize((230, 230))
        self.clock_handle = self.clock_handle.rotate(90,
                                                     resample=Image.BICUBIC,
                                                     expand=True
                                                     )
        self.create_image(self.center_x, self.center_y, image=self.clock_img, anchor='center')
        self.clock_handle_tk = ImageTk.PhotoImage(self.clock_handle)
        self.create_image(self.center_x, self.center_y, image=self.clock_handle_tk, anchor='center')

    def update_clock(self, elapsed_seconds):
        second: float = elapsed_seconds * -6
        rotated_img = self.clock_handle.rotate(second,
                                               resample=Image.BICUBIC,
                                               expand=True)
        text, font_size = format_time(elapsed_seconds)
        self.clock_handle_tk = ImageTk.PhotoImage(rotated_img)
        self.delete(self.text_id)
        self.text_id = self.create_text(self.center_x, self.center_y + 50, text=text, fill='red',
                                        font=(TEXT_FONT, font_size, 'bold'))

        self.create_image(self.center_x, self.center_y, image=self.clock_handle_tk, anchor='center')


class ButtonsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='transparent')
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

        self.lap_button.grid(row=0, column=0, sticky='nsew', padx=10)
        self.start_button.grid(row=0, column=1, sticky='nsew', padx=10)

    def start(self) -> None:
        self.start_button.grid_forget()
        self.reset_button.grid_forget()
        self.stop_button.grid(row=0, column=1, sticky='nsew', padx=10)
        self.lap_button.grid(row=0, column=0, sticky='nsew', padx=10)
        self.lap_button.configure(state='normal', fg_color=ORANGE_DARK)

    #
    def stop(self) -> None:
        self.stop_button.grid_forget()
        self.lap_button.grid_forget()
        self.start_button.grid(row=0, column=1, sticky='nsew', padx=10)
        self.reset_button.grid(row=0, column=0, sticky='nsew', padx=10)

    def reset(self):
        self.reset_button.grid_forget()
        self.lap_button.grid(row=0, column=0, sticky='nsew', padx=10)
        self.lap_button.configure(state='disabled', fg_color=GREY)


class LapsFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='transparent')
        self.grid(row=2, column=0, sticky='nsew')
        # Hide the scrollbar until needed
        self._scrollbar.configure(width=0)
        self.lap_number = 0

    def create_lap_object(self, lap_time: float) -> None:
        self.lap_number += 1
        # Now that frame is getting large enough, bring back the scrollbar
        if self.lap_number > 6:
            self._scrollbar.configure(width=16)
        formatted_time: str = format_time(lap_time)[0]
        LapObject(self, self.lap_number, formatted_time)


class LapObject(ctk.CTkFrame):
    def __init__(self, parent, lap_number, formatted_time):
        super().__init__(master=parent, fg_color='transparent')
        self.lap_number = lap_number
        self.formatted_time = formatted_time

        self.pack(expand=True, fill='both', padx=5, pady=5)
        self.set_layout()
        self.create_widgets()

    def set_layout(self):
        self.rowconfigure(0, weight=1, uniform='a')
        self.columnconfigure((0, 1), weight=1, uniform='b')

    def create_widgets(self):
        font = (TEXT_FONT, CLOCK_FONT_SIZE)
        ctk.CTkLabel(self,
                     text=f'Lap {self.lap_number}',
                     text_color=WHITE, anchor='w',
                     font=font
                     ).grid(row=0, column=0, sticky='nsew')
        ctk.CTkLabel(self,
                     text=self.formatted_time,
                     text_color=WHITE,
                     anchor='e',
                     font=font
                     ).grid(row=0, column=1, sticky='nsew')
