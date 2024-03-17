import enum
import time
from typing import Tuple

from PIL import Image
import pyautogui
from pyautogui import Point
import win32gui

def getMapleStoryWindow()->tuple: 
    winlist = []
    def enum_cb(hwnd, results: list):
        results.append((hwnd, win32gui.GetWindowText(hwnd)))
    win32gui.EnumWindows(enum_cb, winlist)

    mapleStorys = [(hwnd, title) for hwnd, title in winlist if 'MapleStory' in title]
    if len(mapleStorys) == 0: raise Exception("No MapleStory window found")
    
    winLocate = []
    for mapleStory in mapleStorys:
        print(mapleStory)
        try:
            win32gui.SetForegroundWindow(mapleStory[0])
            time.sleep(0.1)
        except Exception as e:
            print("Error", e)
        bbox = win32gui.GetWindowRect(mapleStory[0])
        winLocate.append((bbox[0], bbox[1], bbox[2]-bbox[0], bbox[3]-bbox[1]))
        # img = ImageGrab.grab(bbox)
        # img.save(f"window_{mapleStory[0]}.png")
    
    winBox = winLocate[0]
    for box in winLocate:
        if box[2]*box[3] > winBox[2]*winBox[3]:
            winBox = box
    return winBox

class CubeNotFound(Exception):...
class NoItem(Exception):...

def __getConfirmButton(cube: tuple)->Point|None:
    try:
        confirm: Point = pyautogui.locateCenterOnScreen(image="cube_button_confirm.png", confidence = 0.9, region=cube)
    except:
        return None
    return confirm

def getCube(window_bbox: tuple)->dict:
    try:
        cube = pyautogui.locateOnScreen(image="cube.png", confidence=0.7, grayscale=True, region=window_bbox)
    except:
        raise CubeNotFound("Cube not found")
    
    confirm: Point = __getConfirmButton(cube)
    if confirm is None: raise NoItem("No Item")

    return {
        "cube": cube,
        "confirm": confirm
    }

def getCubeInfoImg(cube: tuple)->Image:
    info = pyautogui.locateOnScreen(image="cube_info2.png", confidence=0.5, grayscale=True, region=cube)
    info_box = ([int(x) for x in info])
    info_box = (info_box[0], info_box[1], info_box[2], info_box[3])
    return pyautogui.screenshot("cube_info_tmp.png", region=info_box)

class ItemValue(enum.Enum):
    NONE = 0
    NORMAL = 1
    RARE = 2
    EPIC = 3
    UNIQUE = 4
    LEGENDARY = 5
    UNKNOWN = 6

def getItemValue(cube: tuple)->Tuple[ItemValue, Point|None] | None:
    confirm = __getConfirmButton(cube)
    if confirm is None: return None
    try:
        return (
            ItemValue.NONE,
            pyautogui.locateCenterOnScreen(image="cube_none.png", confidence=0.9, region=cube)
        )
    except:
        pass
    try:
        return (
            ItemValue.NORMAL,
            pyautogui.locateCenterOnScreen(image="cube_normal.png", confidence=0.9, region=cube)
        )
    except:
        pass
    try:
        return (
            ItemValue.RARE,
            pyautogui.locateCenterOnScreen(image="cube_rare.png", confidence=0.9, region=cube)
        )
    except:
        pass
    return (ItemValue.UNKNOWN, None)


# Additional function
def hasItemWindow(window_bbox: tuple)->bool:
    try:
        pyautogui.locateOnScreen(image="item_window.png", confidence=0.8, region=window_bbox)
        return True
    except:
        return False

if __name__ == "__main__":
    try:
        
        window = getMapleStoryWindow()
        cube = getCube(window)
        info = getCubeInfoImg(cube["cube"])
        print(info)
        value = getItemValue(cube["cube"])
        print(value)

    except Exception as e:
        pyautogui.alert(str(e))
        print(e)
    pass