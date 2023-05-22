import customtkinter as ctk
from functools import partial
import json, threading, time, serial.tools.list_ports, win32api, win32gui, ctypes, pystray, PIL.Image, os
from functions import *
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from tkinter import colorchooser
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume

image = PIL.Image.open("data/icons/Mixr2.png")


master_volume = ["a", "a", "a", "a", "a", "a"]
app_volume = ["a", "a", "a", "a", "a", "a"]
ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
portlist = []

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

def macro_function1():
    pyautogui.typewrite(macrovar[0].get())

def macro_function2():
    pyautogui.typewrite(macrovar[1].get())

def macro_function3():
    pyautogui.typewrite(macrovar[2].get())

def macro_function4():
    pyautogui.typewrite(macrovar[3].get())

def macro_function5():
    pyautogui.typewrite(macrovar[4].get())

def macro_function6():
    pyautogui.typewrite(macrovar[5].get())

def close_window_tf():
    window.withdraw()

sound = 0
def mute_sound():
    global sound
    if sound == 0:
        volume.SetMute(1, None)
        sound = 1
    else:
        volume.SetMute(0, None)
        sound = 0

def language_change(choice):
    settings["language"] = str(choice)
    with open('data/settings/settings.json', 'w') as plik_settings:
        json.dump(settings, plik_settings)
    restart_label = ctk.CTkLabel(window, text=text["Restart App"], text_color="red").place(relx=0.3, rely=0.085)

def theme_change(choice):
    settings["theme"] = str(choice)
    with open ('data/settings/settings.json', 'w') as plik_settings:
        json.dump(settings, plik_settings)
    restart_label = ctk.CTkLabel(window, text=text["Restart App"], text_color="red").place(relx=0.6, rely=0.085)

key_function = ["","","","","","","","",""]
is_key_function = ["","","","","","","",""]
function_list = [master_volume_controller,
                 app_volume_controller,
                 play_pause,
                 mute_mic,
                 next_song,
                 previous_song,
                 print_screen,
                 lock_screen,
                 macro_function1,
                 macro_function2,
                 macro_function3,
                 macro_function4,
                 macro_function5,
                 macro_function6,
                 webrowser_open,
                 mute_sound,
                 nothing
                 ]

keyboard_butto_list = ['a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7',
'8', '9', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
')', '*', '+', ',', '-', '.', '/',  ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
 '{', '|', '}', '~', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10',
'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20',
'f21', 'f22', 'f23', 'f24', 'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
'browserback', 'browserfavorites', 'browserforward', 'browserhome',
'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 
'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
'command', 'option', 'optionleft', 'optionright']

function_button = [nothing,
                   nothing,
                   nothing,
                   nothing,
                   nothing,
                   nothing]

function_slider = [nothing,
                   nothing,
                   nothing,
                   nothing,
                   nothing,
                   nothing]

#window
window = ctk.CTk()
window.title("MixR")
window.geometry('800x450')
window.minsize(600,350)
window.protocol('WM_DELETE_WINDOW', close_window_tf)
window.iconbitmap("data/icons/Mixr2.ico")

with open("data/settings/settings.json") as file_settings:
    settings = json.load(file_settings)

with open('data/languages/'+settings["language"]) as texts:
    text = json.load(texts)

with open('data/themes/'+settings["theme"]) as colors:
    theme = json.load(colors)

with open("data/settings/macros.json") as macros:
    macro = json.load(macros)

with open("data/settings/buttons.json") as macros:
    buttons = json.load(macros)

with open("data/settings/keyboard.json") as keyboard:
    is_key_function = json.load(keyboard)

g=0
for g in range(5):
    key_function[g] = buttons[g+5][len(buttons[g+5]) - 1]

port_val = 0    

intvar = [ctk.IntVar(window, value=1),
          ctk.IntVar(window, value=1),
          ctk.IntVar(window, value=1),
          ctk.IntVar(window, value=1),
          ctk.IntVar(window, value=1),
          ctk.IntVar(window, value=1)
          ]

macrovar=[
        ctk.StringVar(window, value=macro[0]),
        ctk.StringVar(window, value=macro[1]),
        ctk.StringVar(window, value=macro[2]),
        ctk.StringVar(window, value=macro[3]),
        ctk.StringVar(window, value=macro[4]),
        ctk.StringVar(window, value=macro[5]),
        ]

bindvar=[
    "",
    "",
    "",
    "",
    "",
    ""
]

slidervar=[
        "",
        "",
        "",
        "",
        "",
        ""
        ]

buttonvar=[
        "",
        "",
        "",
        "",
        "",
        ""
        ]

keyboardfunctionvar={
    "",
    "",
    "",
    "",
    "",
    ""
}

switchvar = ctk.StringVar(value="dark")

i = 0
for i in range(5):
    function_button[i] = function_list[int(buttons[i])]

j = 0
for j in range(6):
    buttonvar[j] = str(buttons[j+5])

#main frames
frame_sliders = ctk.CTkFrame(window)
frame_mixr = ctk.CTkFrame(window)
frame_buttons = ctk.CTkFrame(window)

def set_keyboard_function(button_number, key_number):
    key_function[button_number] = keyboard_butto_list[key_number]
    buttons[button_number+5] =str(text["Keyboard"])+str(key_function[button_number])
    is_key_function[button_number] = True
    buttonvar[button_number] =str(text["Keyboard"])+str(keyboard_butto_list[key_number])
    save_keyboard()
    save_buttons()
    buttons_on()
    deafult()

#menu in sliders frame
def buttons_on():
    #frame
    frame_sliders.place(x=0, y=0, relwidth=0.2, relheight=1)
    #slider1
    ctk.CTkLabel(frame_sliders, text=text["Slider 1 label"] + " " + slidervar[0]).place(relx=0, rely=0, relwidth=1, relheight=0.1)
    ctk.CTkButton(frame_sliders, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]),  height=30, text=text["Slider 1 Button"], text_color=(theme["text_color_light"],theme["text_color_dark"]), command=lambda:bind_slider(1)).place(relx=0.04, rely=0.08, relwidth=0.92)
    #slider2
    ctk.CTkLabel(frame_sliders, text=text["Slider 2 label"] + " " + slidervar[1]).place(relx=0, rely=0.15, relwidth=1, relheight=0.1)
    ctk.CTkButton(frame_sliders, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), height=30, text=text["Slider 2 Button"], text_color=(theme["text_color_light"],theme["text_color_dark"]), command=lambda:bind_slider(2)).place(relx=0.04, rely=0.23, relwidth=0.92)
    #slider3
    ctk.CTkLabel(frame_sliders, text=text["Slider 3 label"] + " " + slidervar[2]).place(relx=0, rely=0.30, relwidth=1, relheight=0.1)
    ctk.CTkButton(frame_sliders, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), height=30, text=text["Slider 3 Button"], text_color=(theme["text_color_light"],theme["text_color_dark"]), command=lambda:bind_slider(3)).place(relx=0.04, rely=0.38, relwidth=0.92)
    #slider4
    ctk.CTkLabel(frame_sliders, text=text["Slider 4 label"] + " " + slidervar[3]).place(relx=0, rely=0.45, relwidth=1, relheight=0.1)
    ctk.CTkButton(frame_sliders, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), height=30, text=text["Slider 4 Button"], text_color=(theme["text_color_light"],theme["text_color_dark"]), command=lambda:bind_slider(4)).place(relx=0.04, rely=0.53, relwidth=0.92)
    #slider5
    ctk.CTkLabel(frame_sliders, text=text["Slider 5 label"] + " " + slidervar[4]).place(relx=0, rely=0.60, relwidth=1, relheight=0.1)
    ctk.CTkButton(frame_sliders, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), height=30, text=text["Slider 5 Button"], text_color=(theme["text_color_light"],theme["text_color_dark"]), command=lambda:bind_slider(5)).place(relx=0.04, rely=0.68, relwidth=0.92)
    #slider6
    ctk.CTkLabel(frame_sliders, text=text["Slider 6 label"] + " " + slidervar[5]).place(relx=0, rely=0.75, relwidth=1, relheight=0.1)
    ctk.CTkButton(frame_sliders, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), height=30, text=text["Slider 6 Button"], text_color=(theme["text_color_light"],theme["text_color_dark"]), command=lambda:bind_slider(6)).place(relx=0.04, rely=0.83, relwidth=0.92)


#menu in buttons frame
    #frame
    frame_buttons.place(relx=0.8, y=0, relwidth=0.2, relheight=1)
    #button1
    ctk.CTkLabel(frame_buttons, text=text["Button 1 label"] + " " + buttonvar[0]).place(relx=0, rely=0, relwidth=1, relheight=0.1)
    ctk.CTkButton(frame_buttons, text_color=(theme["text_color_light"],theme["text_color_dark"]), fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Button 1 Button"], command=lambda:bind_button(0)).place(relx=0.04, rely=0.08, relwidth=0.92)
    #button2
    ctk.CTkLabel(frame_buttons, text=text["Button 2 label"] + " " + buttonvar[1]).place(relx=0, rely=0.15, relwidth=1, relheight=0.1)
    ctk.CTkButton(frame_buttons, text_color=(theme["text_color_light"],theme["text_color_dark"]), fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Button 2 Button"], command=lambda:bind_button(1)).place(relx=0.04, rely=0.23, relwidth=0.92)
    #button3
    ctk.CTkLabel(frame_buttons, text=text["Button 3 label"] + " " + buttonvar[2]).place(relx=0, rely=0.30, relwidth=1, relheight=0.1)
    ctk.CTkButton(frame_buttons, text_color=(theme["text_color_light"],theme["text_color_dark"]), fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Button 3 Button"], command=lambda:bind_button(2)).place(relx=0.04, rely=0.38, relwidth=0.92)
    #button4
    ctk.CTkLabel(frame_buttons, text=text["Button 4 label"] + " " + buttonvar[3]).place(relx=0, rely=0.45, relwidth=1, relheight=0.1)
    ctk.CTkButton(frame_buttons, text_color=(theme["text_color_light"],theme["text_color_dark"]), fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Button 4 Button"], command=lambda:bind_button(3)).place(relx=0.04, rely=0.53, relwidth=0.92)
    #button5
    ctk.CTkLabel(frame_buttons, text=text["Button 5 label"] + " " + buttonvar[4]).place(relx=0, rely=0.60, relwidth=1, relheight=0.1)
    ctk.CTkButton(frame_buttons, text_color=(theme["text_color_light"],theme["text_color_dark"]), fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Button 5 Button"], command=lambda:bind_button(4)).place(relx=0.04, rely=0.68, relwidth=0.92)
    #button6
    ctk.CTkLabel(frame_buttons, text=text["Button 6 label"] + " " + buttonvar[5]).place(relx=0, rely=0.75, relwidth=1, relheight=0.1)
    ctk.CTkButton(frame_buttons, text_color=(theme["text_color_light"],theme["text_color_dark"]), fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Button 6 Button"], command=lambda:bind_button(5)).place(relx=0.04, rely=0.83, relwidth=0.92)

def port_select():
    frame_mixr.place(relx=0.225, rely=0.1, relheight=0.8, relwidth=0.55)
    ctk.CTkLabel(frame_mixr, text="").place(relx=0, rely=0, relwidth=1, relheight=1)
    ctk.CTkLabel(frame_mixr, text=text["Port Select Label"], text_color=(theme["text_color_light"],theme["text_color_dark"])).place(relx=0, rely=0, relwidth=1, relheight=0.1)
    scrollable_frame = ctk.CTkScrollableFrame(frame_mixr)
    scrollable_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.8)

    var_holder = {}
    port_names = []
    a = -1

    for onePort in ports:
        a += 1
        portlist.append(str(onePort))
        port_number = [x[0:4] for x in onePort]
        var_holder['my_var_' + str(a)] = port_number[0]
        port_names.append(port_number[0])
        ctk.CTkButton(scrollable_frame, text=str(onePort), fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), command= partial(set_port, port_names[a]), text_color=(theme["text_color_light"],theme["text_color_dark"])).pack(pady=5)

def deafult():
    frame_mixr.place(relx=0.225, rely=0.25, relheight=0.6, relwidth=0.55)
    button_label1 = ctk.CTkLabel(frame_mixr, text="")
    button_label1.place(relx=0, rely=0, relwidth=1, relheight=1)
    slider1 = ctk.CTkSlider(frame_mixr, button_color=(theme["slider_light"],theme["slider_dark"]), progress_color=(theme["slider_light"], theme["slider_dark"]), orientation="vertical", variable=intvar[0], state="disabled", number_of_steps=100, from_=0, to=100).place(relx=0.05, rely=0.05, relwidth=0.05, relheight=0.9)
    slider2 = ctk.CTkSlider(frame_mixr, button_color=(theme["slider_light"],theme["slider_dark"]), progress_color=(theme["slider_light"], theme["slider_dark"]), orientation="vertical", variable=intvar[1], state="disabled", number_of_steps=100, from_=0, to=100).place(relx=0.14, rely=0.05, relwidth=0.05, relheight=0.9)
    slider3 = ctk.CTkSlider(frame_mixr, button_color=(theme["slider_light"],theme["slider_dark"]), progress_color=(theme["slider_light"], theme["slider_dark"]), orientation="vertical", variable=intvar[2], state="disabled", number_of_steps=100, from_=0, to=100).place(relx=0.23, rely=0.05, relwidth=0.05, relheight=0.9)
    slider4 = ctk.CTkSlider(frame_mixr, button_color=(theme["slider_light"],theme["slider_dark"]), progress_color=(theme["slider_light"], theme["slider_dark"]), orientation="vertical", variable=intvar[3], state="disabled", number_of_steps=100, from_=0, to=100).place(relx=0.32, rely=0.05, relwidth=0.05, relheight=0.9)
    slider5 = ctk.CTkSlider(frame_mixr, button_color=(theme["slider_light"],theme["slider_dark"]), progress_color=(theme["slider_light"], theme["slider_dark"]), orientation="vertical", variable=intvar[4], state="disabled", number_of_steps=100, from_=0, to=100).place(relx=0.41, rely=0.05, relwidth=0.05, relheight=0.9)
    slider6 = ctk.CTkSlider(frame_mixr, button_color=(theme["slider_light"],theme["slider_dark"]), progress_color=(theme["slider_light"], theme["slider_dark"]), orientation="vertical", variable=intvar[5], state="disabled", number_of_steps=100, from_=0, to=100).place(relx=0.50, rely=0.05, relwidth=0.05, relheight=0.9)

    button1 = ctk.CTkLabel(frame_mixr, text_color=(theme["text_color_light"],theme["text_color_dark"]), bg_color=(theme["button_light"],theme["button_dark"]), text="1").place(relx=0.65, rely=0.15, relwidth=0.1, relheight=0.16)
    button2 = ctk.CTkLabel(frame_mixr, text_color=(theme["text_color_light"],theme["text_color_dark"]), bg_color=(theme["button_light"],theme["button_dark"]), text="2").place(relx=0.65, rely=0.4, relwidth=0.1, relheight=0.16)
    button3 = ctk.CTkLabel(frame_mixr, text_color=(theme["text_color_light"],theme["text_color_dark"]), bg_color=(theme["button_light"],theme["button_dark"]), text="3").place(relx=0.65, rely=0.65, relwidth=0.1, relheight=0.16)
    button4 = ctk.CTkLabel(frame_mixr, text_color=(theme["text_color_light"],theme["text_color_dark"]), bg_color=(theme["button_light"],theme["button_dark"]), text="4").place(relx=0.8, rely=0.15, relwidth=0.1, relheight=0.16)
    button5 = ctk.CTkLabel(frame_mixr, text_color=(theme["text_color_light"],theme["text_color_dark"]), bg_color=(theme["button_light"],theme["button_dark"]), text="5").place(relx=0.8, rely=0.4, relwidth=0.1, relheight=0.16)
    button6 = ctk.CTkLabel(frame_mixr, text_color=(theme["text_color_light"],theme["text_color_dark"]), bg_color=(theme["button_light"],theme["button_dark"]), text="6").place(relx=0.8, rely=0.65, relwidth=0.1, relheight=0.16)

    theme_mode_switch = ctk.CTkSwitch(window, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), progress_color=(theme["button_light_menu"],theme["button_dark_menu"]), text="Night mode", command = day_or_night, variable=switchvar, onvalue="dark", offvalue="light").place(relx=0.25, rely=0.9)
    
    languages = os.listdir('data/languages')
    language_switch = ctk.CTkOptionMenu(window, text_color=(theme["text_color_light"],theme["text_color_dark"]), values=languages, command=language_change, fg_color=(theme["button_light"],theme["button_dark"]), button_color=(theme["button_light"],theme["button_dark"]) )
    language_switch.place(relx=0.25, rely=0.02)
    language_switch.set(settings["language"])

    themes = os.listdir('data/themes')
    theme_color_switch = ctk.CTkOptionMenu(window, text_color=(theme["text_color_light"],theme["text_color_dark"]), values=themes, command=theme_change, fg_color=(theme["button_light"],theme["button_dark"]), button_color=(theme["button_light"],theme["button_dark"]))
    theme_color_switch.place(relx=0.55, rely=0.02, relwidth=0.179, relheight=0.062)
    theme_color_switch.set(settings["theme"])
    theme_color_adder = ctk.CTkButton(window, text="+", text_color=(theme["text_color_light"],theme["text_color_dark"]), fg_color=(theme["button_light"],theme["button_dark"]), command=theme_maker_screen)
    theme_color_adder.place(relx=0.73, rely=0.02, relwidth=0.037, relheight=0.062)

def day_or_night():
    ctk.set_appearance_mode(switchvar.get())

def bind_slider(slider_number):
    frame_mixr.place(relx=0.225, rely=0.1, relheight=0.8, relwidth=0.55)
    ctk.CTkLabel(frame_mixr, text="").place(relx=0, rely=0, relwidth=1, relheight=1)
    ctk.CTkLabel(frame_mixr, text=text["App Select Label"]).place(relx=0, rely=0, relwidth=1, relheight=0.1)
    scrollable_frame = ctk.CTkScrollableFrame(frame_mixr)
    scrollable_frame.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.7)
    cancel_button = ctk.CTkButton(frame_mixr, text_color=(theme["text_color_light"],theme["text_color_dark"]), text=text["Cancel Button"], fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), command= deafult).place(relx=0.1, rely=0.85, relwidth=0.8)

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    label = ctk.CTkButton(scrollable_frame, text_color=(theme["text_color_light"],theme["text_color_dark"]), text=text["Master Volume"], fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), command=lambda: set_master_volume_function(slider_number))
    label.pack(pady=5)

    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process:
            label = ctk.CTkButton(scrollable_frame, text_color=(theme["text_color_light"],theme["text_color_dark"]), fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=session.Process.name(), command= partial(set_function_slider, slider_number, session.Process.name()))
            label.pack(pady=5)

def bind_button(button_number):
    #menu for functions
    frame_mixr.place(relx=0.225, rely=0.1, relheight=0.8, relwidth=0.55)
    label = ctk.CTkLabel(frame_mixr, text="").place(relx=0, rely=0, relwidth=1, relheight=1)
    label =ctk.CTkLabel(frame_mixr, text=text["Select function"]).place(relx=0, rely=0, relwidth=1, relheight=0.1)
    scrollable_frame = ctk.CTkScrollableFrame(frame_mixr)
    scrollable_frame.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.7)
    cancel_button = ctk.CTkButton(frame_mixr, text_color=(theme["text_color_light"],theme["text_color_dark"]), fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Cancel Button"], command= deafult).place(relx=0.1, rely=0.85, relwidth=0.8)

    #functions
    label = ctk.CTkLabel(scrollable_frame, text=text["Multimedia Label"]).pack(pady=5)
    label = ctk.CTkButton(scrollable_frame, text_color=(theme["text_color_light"],theme["text_color_dark"]), fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Play/Pause"],command= lambda: set_function(button_number, 2, text["Play/Pause"])).pack(pady=5)
    label = ctk.CTkButton(scrollable_frame, text_color=(theme["text_color_light"],theme["text_color_dark"]), fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Next Song"],command= lambda: set_function(button_number, 4, text["Next Song"])).pack(pady=5)
    label = ctk.CTkButton(scrollable_frame, text_color=(theme["text_color_light"],theme["text_color_dark"]), fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Prevous Song"],command= lambda: set_function(button_number, 5, text["Prevous Song"])).pack(pady=5)
    label = ctk.CTkButton(scrollable_frame, text_color=(theme["text_color_light"],theme["text_color_dark"]), fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Mute Sound"],command= lambda: set_function(button_number, 14, text["Mute Sound"])).pack(pady=5)

    label = ctk.CTkLabel(scrollable_frame, text_color=(theme["text_color_light"],theme["text_color_dark"]), text=text["Functions Label"]).pack(pady=5, expand=True, fill="x")
    label = ctk.CTkButton(scrollable_frame, text_color=(theme["text_color_light"],theme["text_color_dark"]), fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Keyboard Function"],command= lambda: keyboard_function_screen(button_number, 3)).pack(pady=5)
    label = ctk.CTkButton(scrollable_frame, text_color=(theme["text_color_light"],theme["text_color_dark"]), fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Mute Mic"],command= lambda: set_function(button_number, 3, text["Mute Mic"])).pack(pady=5)
    label = ctk.CTkButton(scrollable_frame, text_color=(theme["text_color_light"],theme["text_color_dark"]), fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Print Screen"],command= lambda: set_function(button_number, 6, text["Print Screen"])).pack(pady=5)
    label = ctk.CTkButton(scrollable_frame, text_color=(theme["text_color_light"],theme["text_color_dark"]), fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Lock Screen"],command= lambda: set_function(button_number, 7, text["Lock Screen"])).pack(pady=5)
    label = ctk.CTkButton(scrollable_frame, text_color=(theme["text_color_light"],theme["text_color_dark"]), fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Webbrowser"],command= lambda: set_function(button_number, 15, text["Webbrowser"])).pack(pady=5)
    
    label = ctk.CTkLabel(scrollable_frame, text=text["Macro Label"]).pack(pady=5, expand=True, fill="x")
    label = ctk.CTkButton(scrollable_frame, text_color=(theme["text_color_light"],theme["text_color_dark"]), fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=macrovar[0].get(),command= lambda: macro_change_screen(button_number, 0, 8)).pack(pady=5)
    label = ctk.CTkButton(scrollable_frame, text_color=(theme["text_color_light"],theme["text_color_dark"]), fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=macrovar[1].get(),command= lambda: macro_change_screen(button_number, 1, 9)).pack(pady=5)
    label = ctk.CTkButton(scrollable_frame, text_color=(theme["text_color_light"],theme["text_color_dark"]), fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=macrovar[2].get(),command= lambda: macro_change_screen(button_number, 2, 10)).pack(pady=5)
    label = ctk.CTkButton(scrollable_frame, text_color=(theme["text_color_light"],theme["text_color_dark"]), fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=macrovar[3].get(),command= lambda: macro_change_screen(button_number, 3, 11)).pack(pady=5)
    label = ctk.CTkButton(scrollable_frame, text_color=(theme["text_color_light"],theme["text_color_dark"]), fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=macrovar[4].get(),command= lambda: macro_change_screen(button_number, 4, 12)).pack(pady=5)
    label = ctk.CTkButton(scrollable_frame, text_color=(theme["text_color_light"],theme["text_color_dark"]), fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=macrovar[5].get(),command= lambda: macro_change_screen(button_number, 5, 13)).pack(pady=5)

def macro_change_screen(button_number, macro_number, macro_command_number):
    frame_mixr.place(relx=0.225, rely=0.3, relheight=0.4, relwidth=0.55)
    ctk.CTkLabel(frame_mixr, text="").place(relx=0, rely=0, relwidth=1, relheight=1)
    ctk.CTkLabel(frame_mixr, text=text["Set Macro Label"]).place(relx=0, rely=0.1, relwidth=1, relheight=0.1)
    text_entry = ctk.CTkEntry(frame_mixr, textvariable= macrovar[macro_number]).place(relx=0, rely=0.3, relwidth=1)
    cancel_button = ctk.CTkButton(frame_mixr, text_color=(theme["text_color_light"],theme["text_color_dark"]), fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Save Button"], command= partial(save_macro, button_number, macro_command_number, macro_number) ).place(relx=0.1, rely=0.60, relwidth=0.8)
    cancel_button = ctk.CTkButton(frame_mixr, text_color=(theme["text_color_light"],theme["text_color_dark"]), fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Cancel Button"], command= deafult).place(relx=0.1, rely=0.80, relwidth=0.8)

def keyboard_function_screen(button_number, function):
    frame_mixr.place(relx=0.225, rely=0.05, relheight=0.8, relwidth=0.55)
    ctk.CTkLabel(frame_mixr, text="").place(relx=0, rely=0, relwidth=1, relheight=1)
    ctk.CTkLabel(frame_mixr, text=text["Set Keyboard Function"]).place(relx=0, rely=0, relwidth=1, relheight=0.1)
    cancel_button = ctk.CTkButton(frame_mixr, text_color=(theme["text_color_light"],theme["text_color_dark"]), fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Cancel Button"], command= deafult).place(relx=0.1, rely=0.90, relwidth=0.8)
    tabview = ctk.CTkTabview(master=frame_mixr)
    tabview.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.8)
    letters = tabview.add(text["Tab Letters"])
    fun = tabview.add(text["Tab Functions"])
    numb = tabview.add("Tab Numbers")
    other = tabview.add("Tab Others")
    letters1 = ctk.CTkScrollableFrame(letters)
    letters1.place(relx = 0, rely=0, relwidth=1, relheight=1)
    numb1 = ctk.CTkScrollableFrame(numb)
    numb1.place(relx = 0, rely=0, relwidth=1, relheight=1)
    other1 = ctk.CTkScrollableFrame(other)
    other1.place(relx = 0, rely=0, relwidth=1, relheight=1)
    fun1 = ctk.CTkScrollableFrame(fun)
    fun1.place(relx = 0, rely=0, relwidth=1, relheight=1)

    i = 0
    for x in range(26):
        button_1 = ctk.CTkButton(letters1, text_color=(theme["text_color_light"],theme["text_color_dark"]), text=keyboard_butto_list[int(i)], fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), command=partial(set_keyboard_function, button_number, i))
        button_1.pack(padx=5, pady=5)
        i += 1
    for x in range(10):
        button_1 = ctk.CTkButton(numb1, text_color=(theme["text_color_light"],theme["text_color_dark"]), text=keyboard_butto_list[int(i)], fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), command=partial(set_keyboard_function, button_number, i))
        button_1.pack(padx=5, pady=5)
        i += 1
    for x in range(33):
        button_1 = ctk.CTkButton(other1, text_color=(theme["text_color_light"],theme["text_color_dark"]), text=keyboard_butto_list[int(i)], fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), command=partial(set_keyboard_function, button_number, i))
        button_1.pack(padx=5, pady=5)
        i += 1
    for x in range(len(keyboard_butto_list) - 69):
        button_1 = ctk.CTkButton(fun1, text_color=(theme["text_color_light"],theme["text_color_dark"]), text=keyboard_butto_list[int(i)], fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), command=partial(set_keyboard_function, button_number, i))
        button_1.pack(padx=5, pady=5)
        i += 1

new_theme = {
    "button_light_menu": "#4694FF",
    "button_dark_menu": "#4694FF",
    "slider_light": "#4694FF",
    "slider_dark": "#4694FF",
    "button_light": "#4694FF",
    "button_dark": "#4694FF",
    "pressed_button": "#4694FF",
    "button_hover_light": "#4694FF",
    "button_hover_dark": "#4694FF",
    "text_color_light": "white",
    "text_color_dark": "white" 
    }

def theme_maker_screen():
    global frame_mixr1
    frame_mixr1 = ctk.CTkFrame(window)
    frame_mixr1.place(relx=0, rely=0, relheight=1, relwidth=1)

    label_button_color = ctk.CTkLabel(frame_mixr1, text=text["Theme Button Menu Light"])
    label_button_color.place(relx = 0.05, rely=0.02)
    button_button_color = ctk.CTkButton(frame_mixr1, fg_color=new_theme["button_light_menu"], text="", corner_radius=0, command=partial(set_color, "button_light_menu"))
    button_button_color.place(relx=0.23, rely=0.02, relwidth=0.05, relheight=0.16)

    label_button_color = ctk.CTkLabel(frame_mixr1, text=text["Theme Button Menu Dark"])
    label_button_color.place(relx = 0.05, rely=0.11)
    button_button_color = ctk.CTkButton(frame_mixr1, fg_color=new_theme["button_dark_menu"], text="", corner_radius=0, command=partial(set_color, "button_dark_menu"))
    button_button_color.place(relx=0.23, rely=0.11, relwidth=0.05, relheight=0.16)

    label_button_color = ctk.CTkLabel(frame_mixr1, text=text["Theme Slider Light"])
    label_button_color.place(relx = 0.05, rely=0.20)
    button_button_color = ctk.CTkButton(frame_mixr1, fg_color=new_theme["slider_light"], text="", corner_radius=0, command=partial(set_color, "slider_light"))
    button_button_color.place(relx=0.23, rely=0.20, relwidth=0.05, relheight=0.16)

    label_button_color = ctk.CTkLabel(frame_mixr1, text=text["Theme Slider Dark"])
    label_button_color.place(relx = 0.05, rely=0.29)
    button_button_color = ctk.CTkButton(frame_mixr1, fg_color=new_theme["slider_dark"], text="", corner_radius=0, command=partial(set_color, "slider_dark"))
    button_button_color.place(relx=0.23, rely=0.29, relwidth=0.05, relheight=0.16)

    label_button_color = ctk.CTkLabel(frame_mixr1, text=text["Theme Button Light"])
    label_button_color.place(relx = 0.05, rely=0.38)
    button_button_color = ctk.CTkButton(frame_mixr1, fg_color=new_theme["button_light"], text="", corner_radius=0, command=partial(set_color, "button_light"))
    button_button_color.place(relx=0.23, rely=0.38, relwidth=0.05, relheight=0.16)

    label_button_color = ctk.CTkLabel(frame_mixr1, text=text["Theme Button Dark"])
    label_button_color.place(relx = 0.05, rely=0.47)
    button_button_color = ctk.CTkButton(frame_mixr1, fg_color=new_theme["button_dark"], text="", corner_radius=0, command=partial(set_color, "button_dark"))
    button_button_color.place(relx=0.23, rely=0.47, relwidth=0.05, relheight=0.16)

    label_button_color = ctk.CTkLabel(frame_mixr1, text=text["Theme Button Clicked"])
    label_button_color.place(relx = 0.05, rely=0.56)
    button_button_color = ctk.CTkButton(frame_mixr1, fg_color=new_theme["pressed_button"], text="", corner_radius=0, command=partial(set_color, "pressed_button"))
    button_button_color.place(relx=0.23, rely=0.56, relwidth=0.05, relheight=0.16)

    label_button_color = ctk.CTkLabel(frame_mixr1, text=text["Theme Button Hover Light"])
    label_button_color.place(relx = 0.05, rely=0.65)
    button_button_color = ctk.CTkButton(frame_mixr1, fg_color=new_theme["button_hover_light"], text="", corner_radius=0, command=partial(set_color, "button_hover_light"))
    button_button_color.place(relx=0.23, rely=0.65, relwidth=0.05, relheight=0.16)

    label_button_color = ctk.CTkLabel(frame_mixr1, text=text["Theme Button Hover Dark"])
    label_button_color.place(relx = 0.05, rely=0.74)
    button_button_color = ctk.CTkButton(frame_mixr1, fg_color=new_theme["button_hover_dark"], text="", corner_radius=0, command=partial(set_color, "button_hover_dark"))
    button_button_color.place(relx=0.23, rely=0.74, relwidth=0.05, relheight=0.16)

    label_button_color = ctk.CTkLabel(frame_mixr1, text=text["Theme Text Light"])
    label_button_color.place(relx = 0.05, rely=0.83)
    button_button_color = ctk.CTkButton(frame_mixr1, fg_color=new_theme["text_color_light"], text="", corner_radius=0, command=partial(set_color, "text_color_light"))
    button_button_color.place(relx=0.23, rely=0.83, relwidth=0.05, relheight=0.16)

    label_button_color = ctk.CTkLabel(frame_mixr1, text=text["Theme Text Dark"])
    label_button_color.place(relx = 0.05, rely=0.92)
    button_button_color = ctk.CTkButton(frame_mixr1, fg_color=new_theme["text_color_dark"], text="", corner_radius=0, command=partial(set_color, "text_color_dark"))
    button_button_color.place(relx=0.23, rely=0.92, relwidth=0.05, relheight=0.16)

    label_button_color = ctk.CTkLabel(frame_mixr1, text=text["Theme Preview"])
    label_button_color.place(relx = 0.6, rely=0.1)

    slider1 = ctk.CTkSlider(frame_mixr1, button_color=new_theme["slider_light"], progress_color=new_theme["slider_light"], orientation="vertical", variable=intvar[0], state="disabled", number_of_steps=100, from_=0, to=100).place(relx=0.8, rely=0.2, relwidth=0.03, relheight=0.6)
    button1 = ctk.CTkLabel(frame_mixr1, text_color=new_theme["text_color_light"], bg_color=new_theme["button_light"], text="1").place(relx=0.55, rely=0.3, relwidth=0.1, relheight=0.16)
    ctk.CTkButton(frame_mixr1, fg_color=new_theme["button_light_menu"], hover_color=new_theme["button_hover_light"],  height=30, text=text["Slider 1 Button"], text_color=new_theme["text_color_light"]).place(relx=0.55, rely=0.6, relwidth=0.2)

    slider1 = ctk.CTkSlider(frame_mixr1, button_color=new_theme["slider_dark"], progress_color=new_theme["slider_dark"], orientation="vertical", variable=intvar[0], state="disabled", number_of_steps=100, from_=0, to=100).place(relx=0.85, rely=0.2, relwidth=0.03, relheight=0.6)
    button1 = ctk.CTkLabel(frame_mixr1, text_color=new_theme["text_color_dark"], bg_color=new_theme["button_dark"], text="1").place(relx=0.66, rely=0.3, relwidth=0.1, relheight=0.16)
    ctk.CTkButton(frame_mixr1, fg_color=new_theme["button_dark_menu"], hover_color=new_theme["button_hover_dark"],  height=30, text=text["Slider 1 Button"], text_color=new_theme["text_color_dark"]).place(relx=0.55, rely=0.7, relwidth=0.2)

    save_button = ctk.CTkButton(frame_mixr1, text_color=(theme["text_color_light"],theme["text_color_dark"]), fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Save Button"], command=save_theme_screen).place(relx=0.4, rely=0.90, relwidth=0.2)
    cancel_button = ctk.CTkButton(frame_mixr1, text_color=(theme["text_color_light"],theme["text_color_dark"]), fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Cancel Button"], command=cancel_theme).place(relx=0.7, rely=0.90, relwidth=0.2)

def cancel_theme():
    frame_mixr1.place_forget()
    deafult()
    buttons_on()

def set_color(number):
    new_theme[number] = colorchooser.askcolor()[1]
    frame_mixr1.place_forget()
    theme_maker_screen()

namevar = ctk.StringVar(value=1)

def save_theme_screen():
    frame_mixr1.place(relx=0, rely=0, relheight=1, relwidth=1)
    ctk.CTkLabel(frame_mixr1, text="").place(relx=0, rely=0, relwidth=1, relheight=1)
    ctk.CTkLabel(frame_mixr1, text=text["Set Name"]).place(relx=0, rely=0.1, relwidth=1, relheight=0.1)
    text_entry1 = ctk.CTkEntry(frame_mixr1, textvariable=namevar)
    text_entry1.place(relx=0.1, rely=0.3, relwidth=0.8)
    cancel_button = ctk.CTkButton(frame_mixr1, text_color=(theme["text_color_light"],theme["text_color_dark"]), fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Save Button"], command=save_theme).place(relx=0.2, rely=0.70, relwidth=0.6)
    cancel_button = ctk.CTkButton(frame_mixr1, text_color=(theme["text_color_light"],theme["text_color_dark"]), fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Cancel Button"], command=cancel_theme).place(relx=0.2, rely=0.80, relwidth=0.6)

def save_theme():
    with open('data/themes/'+str(namevar.get())+'.json', 'w') as plik_theme:
        json.dump(new_theme, plik_theme)
    cancel_theme()

def save_macro(button_number, macro_command_number, macro_number):
    macro=[
        macrovar[0].get(),
        macrovar[1].get(),
        macrovar[2].get(),
        macrovar[3].get(),
        macrovar[4].get(),
        macrovar[5].get()
    ]
    with open('data/settings/macros.json', 'w') as plik_macros:
        json.dump(macro, plik_macros)
    set_function(button_number, macro_command_number, macrovar[macro_number].get())

def save_buttons():
    with open('data/settings/buttons.json', 'w') as plik_buttons:
        json.dump(buttons, plik_buttons)

def save_keyboard():
    with open('data/settings/keyboard.json', 'w') as plik_keyboard:
        json.dump(is_key_function, plik_keyboard)

def set_function(button_number, function_number, function_name):
    buttons[button_number] = function_number
    function_button[button_number] = function_list[function_number]
    buttonvar[button_number] = str(function_name)
    buttons[button_number+5] = buttonvar[button_number]
    is_key_function[button_number] = False
    save_buttons()
    save_keyboard()
    buttons_on()
    deafult()

def set_function_slider(slider_number, app_name):
    master_volume[slider_number - 1] = 0
    app_volume[slider_number -1] = app_name
    slidervar[slider_number -1] = app_name
    buttons_on()
    deafult()

def set_master_volume_function(slider_number):
    master_volume[slider_number - 1] = 1
    slidervar[slider_number -1] = text["Master Volume"]
    buttons_on()
    deafult()

def set_port(portnumber):
    global port_val
    port_val = portnumber
    start()
    deafult()
    buttons_on()

def start():
    threading.Thread(target=mixer_control, daemon=True).start()
    threading.Thread(target=icon_start, daemon=True).start()

if port_val == 0:
    port_select()
else:
    buttons_on()
    deafult()
    start() 

#function_button[0]() tak działa

#mixR working
def mixer_control():
    serialInst.baudrate = 115200
    serialInst.port = port_val
    serialInst.open()
    while True:
        time.sleep(0.1)
        if serialInst.in_waiting:
            packet = serialInst.readline()
            if int(packet.decode('utf')) >= 1000 and int(packet.decode('utf')) <= 1100:
                intvar[0].set(int(packet.decode('utf')) - 1000)
                if master_volume[0] == 1:
                    volume.SetMasterVolumeLevelScalar((int(packet.decode('utf')) - 1000)/100, None )
                elif master_volume[0] == 0:
                    sessions2 = AudioUtilities.GetAllSessions()
                    for session in sessions2:
                        volume_app = session._ctl.QueryInterface(ISimpleAudioVolume)
                        if session.Process and session.Process.name() == app_volume[0]:
                            volume_app.SetMasterVolume((int(packet.decode('utf')) - 1000)/100, None )                    
                else:
                    pass
            if int(packet.decode('utf')) >= 2000 and int(packet.decode('utf')) <= 2100:
                intvar[1].set(int(packet.decode('utf')) - 2000)
                if master_volume[1] == 1:
                    volume.SetMasterVolumeLevelScalar((int(packet.decode('utf')) - 2000)/100, None )
                elif master_volume[1] == 0:
                    sessions2 = AudioUtilities.GetAllSessions()
                    for session in sessions2:
                        volume_app = session._ctl.QueryInterface(ISimpleAudioVolume)
                        if session.Process and session.Process.name() == app_volume[1]:
                            volume_app.SetMasterVolume((int(packet.decode('utf')) - 2000)/100, None )
                else:
                    pass
            if int(packet.decode('utf')) >= 3000 and int(packet.decode('utf')) <= 3100:
                intvar[2].set(int(packet.decode('utf')) - 3000)
                if master_volume[2] == 1:
                    volume.SetMasterVolumeLevelScalar((int(packet.decode('utf')) - 3000)/100, None )
                elif master_volume[2] == 0:
                    sessions2 = AudioUtilities.GetAllSessions()
                    for session in sessions2:
                        volume_app = session._ctl.QueryInterface(ISimpleAudioVolume)
                        if session.Process and session.Process.name() == app_volume[2]:
                            volume_app.SetMasterVolume((int(packet.decode('utf')) - 3000)/100, None )
                else:
                    pass
            if int(packet.decode('utf')) >= 4000 and int(packet.decode('utf')) <= 4100:
                intvar[3].set(int(packet.decode('utf')) - 4000)
                if master_volume[3] == 1:
                    volume.SetMasterVolumeLevelScalar((int(packet.decode('utf')) - 4000)/100, None )
                elif master_volume[3] == 0:
                    sessions2 = AudioUtilities.GetAllSessions()
                    for session in sessions2:
                        volume_app = session._ctl.QueryInterface(ISimpleAudioVolume)
                        if session.Process and session.Process.name() == app_volume[3]:
                            volume_app.SetMasterVolume((int(packet.decode('utf')) - 4000)/100, None )
                else:
                    pass
            if int(packet.decode('utf')) >= 5000 and int(packet.decode('utf')) <= 5100:
                intvar[4].set(int(packet.decode('utf')) - 5000)
                if master_volume[4] == 1:
                    volume.SetMasterVolumeLevelScalar((int(packet.decode('utf')) - 5000)/100, None )
                elif master_volume[4] == 0:
                    sessions2 = AudioUtilities.GetAllSessions()
                    for session in sessions2:
                        volume_app = session._ctl.QueryInterface(ISimpleAudioVolume)
                        if session.Process and session.Process.name() == app_volume[4]:
                            volume_app.SetMasterVolume((int(packet.decode('utf')) - 5000)/100, None )
                else:
                    pass
            if int(packet.decode('utf')) >= 6000 and int(packet.decode('utf')) <= 6100:
                intvar[5].set(int(packet.decode('utf')) - 6000)
                if master_volume[5] == 1:
                    volume.SetMasterVolumeLevelScalar((int(packet.decode('utf')) - 6000)/100, None )
                elif master_volume[5] == 0:
                    sessions2 = AudioUtilities.GetAllSessions()
                    for session in sessions2:
                        volume_app = session._ctl.QueryInterface(ISimpleAudioVolume)
                        if session.Process and session.Process.name() == app_volume[5]:
                            volume_app.SetMasterVolume((int(packet.decode('utf')) - 6000)/100, None )
                else:
                    pass
    
            if int(packet.decode('utf')) == 4:
                if is_key_function[3]:
                    pyautogui.press(key_function[3])
                    button4 = ctk.CTkLabel(frame_mixr, bg_color=theme["pressed_button"], text="").place(relx=0.8, rely=0.15, relwidth=0.1, relheight=0.16)
                    time.sleep(0.1)
                    button4 = ctk.CTkLabel(frame_mixr, bg_color=(theme["button_light"],theme["button_dark"]), text="4").place(relx=0.8, rely=0.15, relwidth=0.1, relheight=0.16)
                else:
                    #button4
                    function_button[3]()
                    button4 = ctk.CTkLabel(frame_mixr, bg_color=theme["pressed_button"], text="").place(relx=0.8, rely=0.15, relwidth=0.1, relheight=0.16)
                    time.sleep(0.1)
                    button4 = ctk.CTkLabel(frame_mixr, bg_color=(theme["button_light"],theme["button_dark"]), text="4").place(relx=0.8, rely=0.15, relwidth=0.1, relheight=0.16)
            elif int(packet.decode('utf')) == 1:
                if is_key_function[0]:
                    pyautogui.press(key_function[0])
                    button1 = ctk.CTkLabel(frame_mixr, bg_color=theme["pressed_button"], text="").place(relx=0.65, rely=0.15, relwidth=0.1, relheight=0.16)
                    time.sleep(0.1)
                    button1 = ctk.CTkLabel(frame_mixr, bg_color=(theme["button_light"],theme["button_dark"]), text="1").place(relx=0.65, rely=0.15, relwidth=0.1, relheight=0.16)
                else:
                    #button1
                    function_button[0]()
                    button1 = ctk.CTkLabel(frame_mixr, bg_color=theme["pressed_button"], text="").place(relx=0.65, rely=0.15, relwidth=0.1, relheight=0.16)
                    time.sleep(0.1)
                    button1 = ctk.CTkLabel(frame_mixr, bg_color=(theme["button_light"],theme["button_dark"]), text="1").place(relx=0.65, rely=0.15, relwidth=0.1, relheight=0.16)
            elif int(packet.decode('utf')) == 2:
                #button2
                if is_key_function[1]:
                    pyautogui.press(key_function[1])
                    button2 = ctk.CTkLabel(frame_mixr, bg_color=theme["pressed_button"], text="").place(relx=0.65, rely=0.4, relwidth=0.1, relheight=0.16)
                    time.sleep(0.1)
                    button2 = ctk.CTkLabel(frame_mixr, bg_color=(theme["button_light"],theme["button_dark"]), text="2").place(relx=0.65, rely=0.4, relwidth=0.1, relheight=0.16)
                else:
                    function_button[1]()
                    button2 = ctk.CTkLabel(frame_mixr, bg_color=theme["pressed_button"], text="").place(relx=0.65, rely=0.4, relwidth=0.1, relheight=0.16)
                    time.sleep(0.1)
                    button2 = ctk.CTkLabel(frame_mixr, bg_color=(theme["button_light"],theme["button_dark"]), text="2").place(relx=0.65, rely=0.4, relwidth=0.1, relheight=0.16)
            elif int(packet.decode('utf')) == 3:
                #button3
                if is_key_function[2]:
                    pyautogui.press(key_function[2])
                    button3 = ctk.CTkLabel(frame_mixr, bg_color=theme["pressed_button"], text="").place(relx=0.65, rely=0.65, relwidth=0.1, relheight=0.16)
                    time.sleep(0.1)
                    button3 = ctk.CTkLabel(frame_mixr, bg_color=(theme["button_light"],theme["button_dark"]), text="3").place(relx=0.65, rely=0.65, relwidth=0.1, relheight=0.16)
                else:
                    function_button[2]()
                    button3 = ctk.CTkLabel(frame_mixr, bg_color=theme["pressed_button"], text="").place(relx=0.65, rely=0.65, relwidth=0.1, relheight=0.16)
                    time.sleep(0.1)
                    button3 = ctk.CTkLabel(frame_mixr, bg_color=(theme["button_light"],theme["button_dark"]), text="3").place(relx=0.65, rely=0.65, relwidth=0.1, relheight=0.16)
            elif int(packet.decode('utf')) == 5:
                #button5
                if is_key_function[4]:
                    pyautogui.press(key_function[4])
                    button5 = ctk.CTkLabel(frame_mixr, bg_color=theme["pressed_button"], text="").place(relx=0.8, rely=0.4, relwidth=0.1, relheight=0.16)
                    time.sleep(0.1)
                    button5 = ctk.CTkLabel(frame_mixr, bg_color=(theme["button_light"],theme["button_dark"]), text="5").place(relx=0.8, rely=0.4, relwidth=0.1, relheight=0.16)
                else:
                    function_button[4]()
                    button5 = ctk.CTkLabel(frame_mixr, bg_color=theme["pressed_button"], text="").place(relx=0.8, rely=0.4, relwidth=0.1, relheight=0.16)
                    time.sleep(0.1)
                    button5 = ctk.CTkLabel(frame_mixr, bg_color=(theme["button_light"],theme["button_dark"]), text="5").place(relx=0.8, rely=0.4, relwidth=0.1, relheight=0.16)
            elif int(packet.decode('utf')) == 6:
                #button6
                if is_key_function[5]:
                    pyautogui.press(key_function[5])
                    button6 = ctk.CTkLabel(frame_mixr, bg_color=theme["pressed_button"], text="").place(relx=0.8, rely=0.65, relwidth=0.1, relheight=0.16)
                    time.sleep(0.1)
                    button6 = ctk.CTkLabel(frame_mixr, bg_color=(theme["button_light"],theme["button_dark"]), text="6").place(relx=0.8, rely=0.65, relwidth=0.1, relheight=0.16)  
                else:
                    function_button[5]()
                    button6 = ctk.CTkLabel(frame_mixr, bg_color=theme["pressed_button"], text="").place(relx=0.8, rely=0.65, relwidth=0.1, relheight=0.16)
                    time.sleep(0.1)
                    button6 = ctk.CTkLabel(frame_mixr, bg_color=(theme["button_light"],theme["button_dark"]), text="6").place(relx=0.8, rely=0.65, relwidth=0.1, relheight=0.16)  

def icon_function(icon, item):
    if  str(item) == text["Tray Show"]:
        window.deiconify()
    elif str(item) == text["Tray Close"]:
        window.destroy()

def icon_start():
    icon.run()

icon = pystray.Icon("MixR", image, menu=pystray.Menu(
    pystray.MenuItem(text["Tray Show"], icon_function),
    pystray.MenuItem(text["Tray Close"], icon_function)
))

#loop
window.mainloop()