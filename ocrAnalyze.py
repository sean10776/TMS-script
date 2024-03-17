from PIL import Image
import cv2
import numpy as np
import pytesseract as tess

def get_clear_img(img: str|Image.Image):
    if isinstance(img, Image.Image):
        img = np.asanyarray(img)
    if isinstance(img, str):
        img = cv2.imread(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    img = img[2:45,7:140,:]
    img = cv2.resize(img, None, fx=9, fy=8) #10 8.5

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thre = cv2.threshold(gray, 0, 255,  cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]

    # ore = cv2.dilate(thre, np.ones((2,2), np.uint8), iterations=1)
    # cv2.imshow("img", ore)
    # cv2.imshow("img", thre)
    return thre

def getCubeInfo(img)->list|None:
    def toString(img)->dict:
        config = r'--oem 3 --psm 6'
        return tess.image_to_string(img, lang='eng', config=config, output_type=tess.Output.DICT)
    text = toString(img)['text']
    # print(text)
    if text == "": return None
    info_list = text.replace(" ", "").split("\n")
    info_list = filter(lambda x: x != "", info_list)
    return list(info_list)

def analyzeCubeInfo(info: list|None)->dict|None:
    if info == None: return None
    ap = ['STR', 'DEX', 'INT', 'LUK', 'HP']
    info_dict = {}
    for i in info:
        if ":" not in i: continue

        _ap, _val = i.split(":")
        if "HP" in _ap: _ap = "HP"
        if _ap not in ap: continue

        if _ap not in info_dict: info_dict[_ap] = {"flat": 0, "per": 0}
        if "%" in _val: info_dict[_ap]["per"] += int(_val.replace("%", ""))
        else: info_dict[_ap]["flat"] += int(_val)

    return info_dict

def getCubeInfoFromImg(img: str | Image.Image)->dict|None:
    return analyzeCubeInfo(getCubeInfo(get_clear_img(img)))

if __name__ == "__main__":
    import windowDetect as wd
    import time
    # img = wd.getCubeInfoImg(wd.getCube(wd.getMapleStoryWindow())['cube'])
    delta = 0
    for i in range(20):
        s = time.time()
        img = "./res/cube_info_dex.png"
        info = getCubeInfoFromImg(img)
        # print(info)
        delta += time.time()-s
    print(delta/20)
    cv2.waitKey(0)
    cv2.destroyAllWindows()