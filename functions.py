import win32api, win32gui, ctypes, pyautogui, webbrowser

class button():
    pass

def nothing():
    pass

#volume_power = int(packet.decode('utf')) - 1000
#volume_power_normalized = ((volume_power/100) * 65) - 65
#volume.SetMasterVolumeLevel(int(volume_power_normalized), None)

def master_volume_controller(volume_name, packet_decode):
    volume_power = packet_decode - 1000
    volume_power_normalized = ((volume_power/100) * 65) - 65
    volume_name.SetMasterVolumeLevel(int(volume_power_normalized), None)

def app_volume_controller(volume_name, packet_decode, app_name):
    pass

def webrowser_open():
    webbrowser.open("https://google.com")

def play_pause():
    VK_MEDIA_PLAY_PAUSE = 0xB3
    hwcode = win32api.MapVirtualKey(VK_MEDIA_PLAY_PAUSE, 0)
    win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, hwcode)

def mute_mic():
    WM_APPCOMMAND = 0x319
    APPCOMMAND_MICROPHONE_VOLUME_MUTE = 0x180000
    hwnd_active = win32gui.GetForegroundWindow()
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_MUTE)

def next_song():
    VK_MEDIA_NEXT_SONG = 0xB0
    hwcode1 = win32api.MapVirtualKey(VK_MEDIA_NEXT_SONG, 0)
    win32api.keybd_event(VK_MEDIA_NEXT_SONG, hwcode1)

def previous_song():
    VK_MEDIA_PREVIOUS_SONG = 0xB1
    hwcode2 = win32api.MapVirtualKey(VK_MEDIA_PREVIOUS_SONG, 0)
    win32api.keybd_event(VK_MEDIA_PREVIOUS_SONG, hwcode2)

def print_screen():
    VK_MEDIA_PRINT_SCREEN = 0x2C
    hwcode3 = win32api.MapVirtualKey(VK_MEDIA_PRINT_SCREEN, 0)
    win32api.keybd_event(VK_MEDIA_PRINT_SCREEN, hwcode3)

def lock_screen():
    ctypes.windll.user32.LockWorkStation()