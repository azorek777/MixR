import customtkinter as ctk
from functools import partial
import json, threading, time, serial.tools.list_ports, win32api, win32gui, ctypes, pystray, PIL.Image
from functions import *
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume

image = PIL.Image.open("Mixr2.png")


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
window.iconbitmap("Mixr2.ico")

with open("settings.json") as file_settings:
    settings = json.load(file_settings)

with open(settings["language"]) as texts:
    text = json.load(texts)

with open(settings["theme"]) as colors:
    theme = json.load(colors)

with open("macros.json") as macros:
    macro = json.load(macros)

with open("buttons.json") as macros:
    buttons = json.load(macros)

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

#menu in sliders frame
def buttons_on():
    #frame
    frame_sliders.place(x=0, y=0, relwidth=0.2, relheight=1)
    #slider1
    ctk.CTkLabel(frame_sliders, text=text["Slider 1 label"] + " " + slidervar[0]).place(relx=0, rely=0, relwidth=1, relheight=0.1)
    ctk.CTkButton(frame_sliders, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]),  height=30, text=text["Slider 1 Button"], command=lambda:bind_slider(1)).place(relx=0.04, rely=0.08, relwidth=0.92)
    #slider2
    ctk.CTkLabel(frame_sliders, text=text["Slider 2 label"] + " " + slidervar[1]).place(relx=0, rely=0.15, relwidth=1, relheight=0.1)
    ctk.CTkButton(frame_sliders, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), height=30, text=text["Slider 2 Button"], command=lambda:bind_slider(2)).place(relx=0.04, rely=0.23, relwidth=0.92)
    #slider3
    ctk.CTkLabel(frame_sliders, text=text["Slider 3 label"] + " " + slidervar[2]).place(relx=0, rely=0.30, relwidth=1, relheight=0.1)
    ctk.CTkButton(frame_sliders, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), height=30, text=text["Slider 3 Button"], command=lambda:bind_slider(3)).place(relx=0.04, rely=0.38, relwidth=0.92)
    #slider4
    ctk.CTkLabel(frame_sliders, text=text["Slider 4 label"] + " " + slidervar[3]).place(relx=0, rely=0.45, relwidth=1, relheight=0.1)
    ctk.CTkButton(frame_sliders, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), height=30, text=text["Slider 4 Button"], command=lambda:bind_slider(4)).place(relx=0.04, rely=0.53, relwidth=0.92)
    #slider5
    ctk.CTkLabel(frame_sliders, text=text["Slider 5 label"] + " " + slidervar[4]).place(relx=0, rely=0.60, relwidth=1, relheight=0.1)
    ctk.CTkButton(frame_sliders, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), height=30, text=text["Slider 5 Button"], command=lambda:bind_slider(5)).place(relx=0.04, rely=0.68, relwidth=0.92)
    #slider6
    ctk.CTkLabel(frame_sliders, text=text["Slider 6 label"] + " " + slidervar[5]).place(relx=0, rely=0.75, relwidth=1, relheight=0.1)
    ctk.CTkButton(frame_sliders, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), height=30, text=text["Slider 6 Button"], command=lambda:bind_slider(6)).place(relx=0.04, rely=0.83, relwidth=0.92)


#menu in buttons frame
    #frame
    frame_buttons.place(relx=0.8, y=0, relwidth=0.2, relheight=1)
    #button1
    ctk.CTkLabel(frame_buttons, text=text["Button 1 label"] + " " + buttonvar[0]).place(relx=0, rely=0, relwidth=1, relheight=0.1)
    ctk.CTkButton(frame_buttons, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Button 1 Button"], command=lambda:bind_button(0)).place(relx=0.04, rely=0.08, relwidth=0.92)
    #button2
    ctk.CTkLabel(frame_buttons, text=text["Button 2 label"] + " " + buttonvar[1]).place(relx=0, rely=0.15, relwidth=1, relheight=0.1)
    ctk.CTkButton(frame_buttons, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Button 2 Button"], command=lambda:bind_button(1)).place(relx=0.04, rely=0.23, relwidth=0.92)
    #button3
    ctk.CTkLabel(frame_buttons, text=text["Button 3 label"] + " " + buttonvar[2]).place(relx=0, rely=0.30, relwidth=1, relheight=0.1)
    ctk.CTkButton(frame_buttons, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Button 3 Button"], command=lambda:bind_button(2)).place(relx=0.04, rely=0.38, relwidth=0.92)
    #button4
    ctk.CTkLabel(frame_buttons, text=text["Button 4 label"] + " " + buttonvar[3]).place(relx=0, rely=0.45, relwidth=1, relheight=0.1)
    ctk.CTkButton(frame_buttons, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Button 4 Button"], command=lambda:bind_button(3)).place(relx=0.04, rely=0.53, relwidth=0.92)
    #button5
    ctk.CTkLabel(frame_buttons, text=text["Button 5 label"] + " " + buttonvar[4]).place(relx=0, rely=0.60, relwidth=1, relheight=0.1)
    ctk.CTkButton(frame_buttons, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Button 5 Button"], command=lambda:bind_button(4)).place(relx=0.04, rely=0.68, relwidth=0.92)
    #button6
    ctk.CTkLabel(frame_buttons, text=text["Button 6 label"] + " " + buttonvar[5]).place(relx=0, rely=0.75, relwidth=1, relheight=0.1)
    ctk.CTkButton(frame_buttons, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Button 6 Button"], command=lambda:bind_button(5)).place(relx=0.04, rely=0.83, relwidth=0.92)

def port_select():
    frame_mixr.place(relx=0.225, rely=0.1, relheight=0.8, relwidth=0.55)
    ctk.CTkLabel(frame_mixr, text="").place(relx=0, rely=0, relwidth=1, relheight=1)
    ctk.CTkLabel(frame_mixr, text=text["Port Select Label"]).place(relx=0, rely=0, relwidth=1, relheight=0.1)
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
        ctk.CTkButton(scrollable_frame, text=str(onePort), fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), command= partial(set_port, port_names[a])).pack(pady=5)

def deafult():
    frame_mixr.place(relx=0.225, rely=0.25, relheight=0.6, relwidth=0.55)
    button_label1 = ctk.CTkLabel(frame_mixr, text="")
    button_label1.place(relx=0, rely=0, relwidth=1, relheight=1)
    slider1 = ctk.CTkSlider(frame_mixr,  button_color=(theme["slider_light"],theme["slider_dark"]), progress_color=(theme["slider_light"], theme["slider_dark"]), orientation="vertical", variable=intvar[0], state="disabled", number_of_steps=100, from_=0, to=100).place(relx=0.05, rely=0.05, relwidth=0.05, relheight=0.9)
    slider2 = ctk.CTkSlider(frame_mixr,  button_color=(theme["slider_light"],theme["slider_dark"]), progress_color=(theme["slider_light"], theme["slider_dark"]), orientation="vertical", variable=intvar[1], state="disabled", number_of_steps=100, from_=0, to=100).place(relx=0.14, rely=0.05, relwidth=0.05, relheight=0.9)
    slider3 = ctk.CTkSlider(frame_mixr,  button_color=(theme["slider_light"],theme["slider_dark"]), progress_color=(theme["slider_light"], theme["slider_dark"]), orientation="vertical", variable=intvar[2], state="disabled", number_of_steps=100, from_=0, to=100).place(relx=0.23, rely=0.05, relwidth=0.05, relheight=0.9)
    slider4 = ctk.CTkSlider(frame_mixr,  button_color=(theme["slider_light"],theme["slider_dark"]), progress_color=(theme["slider_light"], theme["slider_dark"]), orientation="vertical", variable=intvar[3], state="disabled", number_of_steps=100, from_=0, to=100).place(relx=0.32, rely=0.05, relwidth=0.05, relheight=0.9)
    slider5 = ctk.CTkSlider(frame_mixr,  button_color=(theme["slider_light"],theme["slider_dark"]), progress_color=(theme["slider_light"], theme["slider_dark"]), orientation="vertical", variable=intvar[4], state="disabled", number_of_steps=100, from_=0, to=100).place(relx=0.41, rely=0.05, relwidth=0.05, relheight=0.9)
    slider6 = ctk.CTkSlider(frame_mixr,  button_color=(theme["slider_light"],theme["slider_dark"]), progress_color=(theme["slider_light"], theme["slider_dark"]), orientation="vertical", variable=intvar[5], state="disabled", number_of_steps=100, from_=0, to=100).place(relx=0.50, rely=0.05, relwidth=0.05, relheight=0.9)

    button1 = ctk.CTkLabel(frame_mixr, bg_color=(theme["button_light"],theme["button_dark"]), text="").place(relx=0.65, rely=0.15, relwidth=0.1, relheight=0.16)
    button2 = ctk.CTkLabel(frame_mixr, bg_color=(theme["button_light"],theme["button_dark"]), text="").place(relx=0.65, rely=0.4, relwidth=0.1, relheight=0.16)
    button3 = ctk.CTkLabel(frame_mixr, bg_color=(theme["button_light"],theme["button_dark"]), text="").place(relx=0.65, rely=0.65, relwidth=0.1, relheight=0.16)
    button4 = ctk.CTkLabel(frame_mixr, bg_color=(theme["button_light"],theme["button_dark"]), text="").place(relx=0.8, rely=0.15, relwidth=0.1, relheight=0.16)
    button5 = ctk.CTkLabel(frame_mixr, bg_color=(theme["button_light"],theme["button_dark"]), text="").place(relx=0.8, rely=0.4, relwidth=0.1, relheight=0.16)
    button6 = ctk.CTkLabel(frame_mixr, bg_color=(theme["button_light"],theme["button_dark"]), text="").place(relx=0.8, rely=0.65, relwidth=0.1, relheight=0.16)

    theme_mode_switch = ctk.CTkSwitch(window, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), progress_color=(theme["button_light_menu"],theme["button_dark_menu"]), text="Night mode", command = day_or_night, variable=switchvar, onvalue="dark", offvalue="light").place(relx=0.25, rely=0.9)

def day_or_night():
    ctk.set_appearance_mode(switchvar.get())

def bind_slider(slider_number):
    frame_mixr.place(relx=0.225, rely=0.1, relheight=0.8, relwidth=0.55)
    ctk.CTkLabel(frame_mixr, text="").place(relx=0, rely=0, relwidth=1, relheight=1)
    ctk.CTkLabel(frame_mixr, text=text["App Select Label"]).place(relx=0, rely=0, relwidth=1, relheight=0.1)
    scrollable_frame = ctk.CTkScrollableFrame(frame_mixr)
    scrollable_frame.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.7)
    cancel_button = ctk.CTkButton(frame_mixr, text=text["Cancel Button"], fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), command= deafult).place(relx=0.1, rely=0.85, relwidth=0.8)

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    label = ctk.CTkButton(scrollable_frame, text="Master volume", fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), command=lambda: set_master_volume_function(slider_number))
    label.pack(pady=5)

    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process:
            label = ctk.CTkButton(scrollable_frame, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=session.Process.name(), command= partial(set_function_slider, slider_number, session.Process.name()))
            label.pack(pady=5)

def bind_button(button_number):
    #menu for functions
    frame_mixr.place(relx=0.225, rely=0.1, relheight=0.8, relwidth=0.55)
    label = ctk.CTkLabel(frame_mixr, text="").place(relx=0, rely=0, relwidth=1, relheight=1)
    label =ctk.CTkLabel(frame_mixr, text="select function").place(relx=0, rely=0, relwidth=1, relheight=0.1)
    scrollable_frame = ctk.CTkScrollableFrame(frame_mixr)
    scrollable_frame.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.7)
    cancel_button = ctk.CTkButton(frame_mixr, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Cancel Button"], command= deafult).place(relx=0.1, rely=0.85, relwidth=0.8)

    #functions
    label = ctk.CTkLabel(scrollable_frame, text=text["Multimedia Label"]).pack(pady=5)
    label = ctk.CTkButton(scrollable_frame, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Play/Pause"],command= lambda: set_function(button_number, 2, text["Play/Pause"])).pack(pady=5)
    label = ctk.CTkButton(scrollable_frame, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Next Song"],command= lambda: set_function(button_number, 4, text["Next Song"])).pack(pady=5)
    label = ctk.CTkButton(scrollable_frame, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Prevous Song"],command= lambda: set_function(button_number, 5, text["Prevous Song"])).pack(pady=5)
    
    label = ctk.CTkLabel(scrollable_frame, text=text["Functions Label"]).pack(pady=5, expand=True, fill="x")
    label = ctk.CTkButton(scrollable_frame, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Mute Mic"],command= lambda: set_function(button_number, 3, text["Mute Mic"])).pack(pady=5)
    label = ctk.CTkButton(scrollable_frame, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Print Screen"],command= lambda: set_function(button_number, 6, text["Print Screen"])).pack(pady=5)
    label = ctk.CTkButton(scrollable_frame, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Lock Screen"],command= lambda: set_function(button_number, 7, text["Lock Screen"])).pack(pady=5)
    label = ctk.CTkButton(scrollable_frame, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=text["Webbrowser"],command= lambda: set_function(button_number, 15, text["Webbrowser"])).pack(pady=5)
    
    label = ctk.CTkLabel(scrollable_frame, text=text["Macro Label"]).pack(pady=5, expand=True, fill="x")
    label = ctk.CTkButton(scrollable_frame, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=macrovar[0].get(),command= lambda: macro_change_screen(button_number, 0, 8)).pack(pady=5)
    label = ctk.CTkButton(scrollable_frame, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=macrovar[1].get(),command= lambda: macro_change_screen(button_number, 1, 9)).pack(pady=5)
    label = ctk.CTkButton(scrollable_frame, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=macrovar[2].get(),command= lambda: macro_change_screen(button_number, 2, 10)).pack(pady=5)
    label = ctk.CTkButton(scrollable_frame, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=macrovar[3].get(),command= lambda: macro_change_screen(button_number, 3, 11)).pack(pady=5)
    label = ctk.CTkButton(scrollable_frame, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=macrovar[4].get(),command= lambda: macro_change_screen(button_number, 4, 12)).pack(pady=5)
    label = ctk.CTkButton(scrollable_frame, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text=macrovar[5].get(),command= lambda: macro_change_screen(button_number, 5, 13)).pack(pady=5)

def macro_change_screen(button_number, macro_number, macro_command_number):
    frame_mixr.place(relx=0.225, rely=0.3, relheight=0.4, relwidth=0.55)
    ctk.CTkLabel(frame_mixr, text="").place(relx=0, rely=0, relwidth=1, relheight=1)
    ctk.CTkLabel(frame_mixr, text="Set macro").place(relx=0, rely=0.1, relwidth=1, relheight=0.1)
    text_entry = ctk.CTkEntry(frame_mixr, textvariable= macrovar[macro_number]).place(relx=0, rely=0.3, relwidth=1)
    cancel_button = ctk.CTkButton(frame_mixr, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text="Save", command= partial(save_macro, button_number, macro_command_number, macro_number) ).place(relx=0.1, rely=0.60, relwidth=0.8)
    cancel_button = ctk.CTkButton(frame_mixr, fg_color=(theme["button_light_menu"],theme["button_dark_menu"]), hover_color=(theme["button_hover_light"],theme["button_hover_dark"]), text="Cancel", command= deafult).place(relx=0.1, rely=0.80, relwidth=0.8)

def save_macro(button_number, macro_command_number, macro_number):
    macro=[
        macrovar[0].get(),
        macrovar[1].get(),
        macrovar[2].get(),
        macrovar[3].get(),
        macrovar[4].get(),
        macrovar[5].get()
    ]
    with open('macros.json', 'w') as plik_macros:
        json.dump(macro, plik_macros)
    set_function(button_number, macro_command_number, macrovar[macro_number].get())

def save_buttons():
    with open('buttons.json', 'w') as plik_buttons:
        json.dump(buttons, plik_buttons)

def set_function(button_number, function_number, function_name):
    buttons[button_number] = function_number
    function_button[button_number] = function_list[function_number]
    buttonvar[button_number] = str(function_name)
    buttons[button_number+5] = buttonvar[button_number]
    save_buttons()
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
    slidervar[slider_number -1] = "Master volume"
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
                #button4
                function_button[3]()
                button4 = ctk.CTkLabel(frame_mixr, bg_color=theme["pressed_button"], text="").place(relx=0.8, rely=0.15, relwidth=0.1, relheight=0.16)
                time.sleep(0.1)
                button4 = ctk.CTkLabel(frame_mixr, bg_color=(theme["button_light"],theme["button_dark"]), text="").place(relx=0.8, rely=0.15, relwidth=0.1, relheight=0.16)
            elif int(packet.decode('utf')) == 1:
                #button1
                function_button[0]()
                button1 = ctk.CTkLabel(frame_mixr, bg_color=theme["pressed_button"], text="").place(relx=0.65, rely=0.15, relwidth=0.1, relheight=0.16)
                time.sleep(0.1)
                button1 = ctk.CTkLabel(frame_mixr, bg_color=(theme["button_light"],theme["button_dark"]), text="").place(relx=0.65, rely=0.15, relwidth=0.1, relheight=0.16)
            elif int(packet.decode('utf')) == 2:
                #button2
                function_button[1]()
                button2 = ctk.CTkLabel(frame_mixr, bg_color=theme["pressed_button"], text="").place(relx=0.65, rely=0.4, relwidth=0.1, relheight=0.16)
                time.sleep(0.1)
                button2 = ctk.CTkLabel(frame_mixr, bg_color=(theme["button_light"],theme["button_dark"]), text="").place(relx=0.65, rely=0.4, relwidth=0.1, relheight=0.16)
            elif int(packet.decode('utf')) == 3:
                #button3
                function_button[2]()
                button3 = ctk.CTkLabel(frame_mixr, bg_color=theme["pressed_button"], text="").place(relx=0.65, rely=0.65, relwidth=0.1, relheight=0.16)
                time.sleep(0.1)
                button3 = ctk.CTkLabel(frame_mixr, bg_color=(theme["button_light"],theme["button_dark"]), text="").place(relx=0.65, rely=0.65, relwidth=0.1, relheight=0.16)
            elif int(packet.decode('utf')) == 5:
                #button5
                function_button[4]()
                button5 = ctk.CTkLabel(frame_mixr, bg_color=theme["pressed_button"], text="").place(relx=0.8, rely=0.4, relwidth=0.1, relheight=0.16)
                time.sleep(0.1)
                button5 = ctk.CTkLabel(frame_mixr, bg_color=(theme["button_light"],theme["button_dark"]), text="").place(relx=0.8, rely=0.4, relwidth=0.1, relheight=0.16)
            elif int(packet.decode('utf')) == 6:
                #button6
                function_button[5]()
                button6 = ctk.CTkLabel(frame_mixr, bg_color=theme["pressed_button"], text="").place(relx=0.8, rely=0.65, relwidth=0.1, relheight=0.16)
                time.sleep(0.1)
                button6 = ctk.CTkLabel(frame_mixr, bg_color=(theme["button_light"],theme["button_dark"]), text="").place(relx=0.8, rely=0.65, relwidth=0.1, relheight=0.16)  

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