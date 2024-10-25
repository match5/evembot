import win32api
import win32gui
import win32ui
import win32con
import cv2
import numpy as np

from PIL import Image
import ddddocr
ocr = ddddocr.DdddOcr(show_ad=False)

templates = dict()
def get_template(name):
    img = templates.get(name)
    if img is None:
        img = Image.open('image_templates/%s.png' % name)
        templates[name] = img
    # print(name)
    return img


def capture_window(hwnd, file_name=None):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top

    hdc = win32gui.GetWindowDC(hwnd)
    dc = win32ui.CreateDCFromHandle(hdc)
    cdc = dc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(dc, width, height)
    cdc.SelectObject(bmp)
    cdc.BitBlt((0, 0), (width, height), dc, (0, 0), win32con.SRCCOPY)

    info = bmp.GetInfo()
    bits = bmp.GetBitmapBits(True)
    img = Image.frombuffer('RGB', (info['bmWidth'], info['bmHeight']), bits, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(bmp.GetHandle())
    dc.DeleteDC()
    cdc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hdc)

    if file_name is not None:
        img.save(file_name)

    return img


def locate_image(image, template, threshold=0):
    image = np.asarray(image)
    template = np.asarray(template)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)

    h, w = template.shape[:2]

    res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # print (max_val, threshold)

    if max_val > threshold:
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        center = np.mean((top_left, bottom_right), axis=0)
        return center

    return None


def locate_image_rect(image, template, threshold=0):
    image = np.asarray(image)
    template = np.asarray(template)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)

    h, w = template.shape[:2]

    res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # print (max_val, threshold)

    if max_val > threshold:
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        return (top_left[0], top_left[1], bottom_right[0], bottom_right[1])

    return None


def read_image_num(img, box):
    im_crop = img.crop(box)
    name = 'temp/num_%d_%d_%d_%d.png' % (int(box[0]), int(box[1]), int(box[2]), int(box[3]))
    im_crop.save(name)
    text = ''
    with open(name, 'rb') as f:
        text = ocr.classification(f.read())
    return text