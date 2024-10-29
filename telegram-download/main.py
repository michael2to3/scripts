import subprocess
import time

import pyautogui
from pyscreeze import ImageNotFoundException

pyautogui.PAUSE = 0.5


def focus_telegram():
    try:
        window_id = (
            subprocess.check_output(["xdotool", "search", "--name", "Telegram"])
            .decode()
            .split("\n")[0]
        )
        subprocess.run(["xdotool", "windowactivate", window_id.strip()], check=True)
        time.sleep(1)
    except subprocess.CalledProcessError:
        exit()
    except IndexError:
        exit()


def filter_button(buttons, threshold=50):
    filtered_buttons = []
    for button in buttons:
        if not any(
            abs(button.top - other.top) < threshold
            and abs(button.left - other.left) < threshold
            for other in filtered_buttons
        ):
            filtered_buttons.append(button)
    return filtered_buttons


def click_download_buttons():
    buttons = list(pyautogui.locateAllOnScreen("download_button.png", confidence=0.9))
    if buttons:
        buttons = filter_button(buttons)
        for button in buttons:
            x, y = pyautogui.center(button)
            print(x, y)
            pyautogui.click(x, y)
            time.sleep(0.2)
    else:
        print("No download buttons found on the screen.")


def scroll_up():
    pyautogui.scroll(5)


def main():
    focus_telegram()
    while True:
        try:
            click_download_buttons()
        except ImageNotFoundException:
            scroll_up()
        time.sleep(5)


if __name__ == "__main__":
    main()
