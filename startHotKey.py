import pyautogui as pag

def cubeHotKey():
    for i in range(3):
        pag.leftClick()
        pag.press("enter")

if __name__ == "__main__":
    print(pag.KEYBOARD_KEYS)