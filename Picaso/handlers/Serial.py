import time
import math

letters = ['T', 'y', 'Q', 'S', 'P', 'B', 'j', 'M', 'Z', 'm']


def getSerial() -> str:
    _Now = (time.time() * 1e7) * 31.4
    _Now = math.floor(_Now)
    _Now = str(_Now)

    for i, letter in enumerate(letters):
        _Now = _Now.replace(str(i), letter)

    return f"{chr(72)}{chr(63)}{_Now[:4]}{chr(69)}{chr(63)}{_Now[5:7]}{chr(82)}{chr(63)}{_Now[8:]}{chr(63)}{chr(65)}"
