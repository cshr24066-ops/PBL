import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32
imm32 = ctypes.windll.imm32


def is_ime_composing(hwnd):

    himc = imm32.ImmGetContext(hwnd)

    if not himc:
        return False

    GCS_COMPSTR = 0x0008

    length = imm32.ImmGetCompositionStringW(
        himc,
        GCS_COMPSTR,
        None,
        0
    )

    imm32.ImmReleaseContext(hwnd, himc)

    return length > 0