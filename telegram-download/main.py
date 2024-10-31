import logging
import re
import subprocess
import time

import pyautogui
from pyscreeze import ImageNotFoundException

pyautogui.PAUSE = 0.5

logging.basicConfig(level=logging.INFO)

center_x = None
center_y = None


def locateAllOnScreen(filename, confidence=0.9):
    try:
        return list(pyautogui.locateAllOnScreen(filename, confidence=confidence))
    except ImageNotFoundException:
        return []


def focus_telegram():
    global center_x, center_y
    try:
        window_ids = (
            subprocess.check_output(
                ["xdotool", "search", "--onlyvisible", "--class", "Telegram"]
            )
            .decode()
            .split()
        )
        logging.info(f"Found window IDs: {window_ids}")
        for window_id in window_ids:
            try:
                logging.info(f"Attempting to activate window ID: {window_id}")
                subprocess.run(
                    ["xdotool", "windowactivate", "--sync", window_id.strip()],
                    check=True,
                )
                logging.info(f"Successfully activated window ID: {window_id}")

                geometry_output = subprocess.check_output(
                    ["xdotool", "getwindowgeometry", window_id.strip()]
                ).decode()

                position_match = re.search(r"Position: (\d+),(\d+)", geometry_output)
                geometry_match = re.search(r"Geometry: (\d+)x(\d+)", geometry_output)
                if position_match and geometry_match:
                    pos_x, pos_y = map(int, position_match.groups())
                    width, height = map(int, geometry_match.groups())
                    center_x = pos_x + width / 2
                    center_y = pos_y + height / 2
                    logging.info(f"Telegram window center at: {center_x}, {center_y}")
                    pyautogui.moveTo(center_x, center_y)
                    time.sleep(1)
                    return
                else:
                    logging.error("Failed to parse window geometry.")
                    exit()
            except subprocess.CalledProcessError as e:
                logging.error(f"Failed to activate window ID {window_id}: {e}")
                continue
        logging.error("Could not activate any Telegram window.")
        exit()
    except subprocess.CalledProcessError as e:
        logging.error(f"No Telegram window found: {e}")
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
    global center_x, center_y
    buttons = locateAllOnScreen("download_button.png", confidence=0.9)
    if buttons:
        buttons = filter_button(buttons)
        for button in buttons:
            x, y = pyautogui.center(button)
            logging.info(f"Clicking at position: {x}, {y}")
            pyautogui.click(x, y)
            time.sleep(0.2)
            pyautogui.moveTo(center_x, center_y)
        return True
    else:
        logging.info("No download buttons found on the screen.")
        return False


def scroll_up():
    pyautogui.scroll(1)


def check_wait_buttons():
    while locateAllOnScreen("wait_button.png", confidence=0.9):
        logging.info("Wait buttons detected, waiting...")
        time.sleep(1)
    logging.info("Wait buttons gone, continuing...")


def main():
    while True:
        focus_telegram()
        check_wait_buttons()
        clicked = click_download_buttons()
        if not clicked:
            scroll_up()
        time.sleep(5)


if __name__ == "__main__":
    main()
