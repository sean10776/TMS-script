import pyautogui
import pynput
import time

import windowDetect as wd
from startHotKey import cubeHotKey


# Get main windows
main_win = wd.getMapleStoryWindow()

if __name__ == "__main__":
    start = True
    confirm = ""
    confirmQueue = []
    # detect fn key on press by user
    def on_press(key):
        global confirmQueue, start
        if key == pynput.keyboard.Key.pause:
            confirmQueue.append("")
            confirm = pyautogui.confirm("腳本？", buttons=["楓方跳框", "關閉"])
            confirmQueue.append(confirm)
        if key == pynput.keyboard.Key.esc:
            start = False
            confirmQueue.append("關閉")

    listener = pynput.keyboard.Listener(on_press=on_press)
    listener.start()
    print("Start")
    while start:
        if len(confirmQueue) > 0:
            confirm = confirmQueue.pop(0)
            if confirm == '楓方跳框':
                # Get cube window
                try:
                    cube = wd.getCube(main_win)
                    x, y = cube['confirm']
                    pyautogui.moveTo(cube['confirm'])
                    time.sleep(0.01)
                except Exception as e:
                    if e is wd.CubeNotFound:
                        pyautogui.alert("找不到楓方")
                    if e is wd.NoItem:
                        pyautogui.alert("找不到物品")
                    print(e)
            elif confirm == "關閉": break
        
        if confirm == "楓方跳框":
            if pyautogui.position() != cube['confirm']: confirm = "" # if mouse move, reset confirm
            try:
                value = wd.getItemValue(cube["cube"])
                if value is None:
                    time.sleep(0.001)
                    continue
                elif value[0] == wd.ItemValue.NONE or value[0] == wd.ItemValue.NORMAL:
                    cubeHotKey()
                else:
                    confirm = ""
            except Exception as e:
                pyautogui.alert(str(e))
                print(e)
                confirm = ""
        time.sleep(0.001)
    listener.stop()
    print("End")