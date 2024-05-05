import pyautogui
import datetime
import time
from PIL import Image
import cv2
import numpy as np
import keyboard
import os
import math


def click_circle(center_x, center_y, radius, clicks):
    """
    Clicks around a circle at intervals.

    Args:
    center_x (int): The x-coordinate of the center of the circle.
    center_y (int): The y-coordinate of the center of the circle.
    radius (int): The radius of the circle.
    clicks (int): The number of times to click around the circle.
    """
    for i in range(clicks):
        angle = math.radians(30 * i)  # Convert degrees to radians
        x = center_x + int(radius * math.cos(angle))  # Calculate the x coordinate
        y = center_y - int(radius * math.sin(angle))  # Calculate the y coordinate

        pyautogui.moveTo(x, y)  # Move to the calculated coordinates
        pyautogui.click()  # Perform the click


def find_color_in_screenshot(file_path, target_color, tolerance):
    """
    Searches for a pixel with the specified color in a screenshot with a tolerance.

    Parameters:
    file_path (str): The path to the screenshot file.
    target_color (tuple): The RGB color to search for (e.g., (255, 0, 0) for red).
    tolerance (int): The allowable margin of error for each color channel (default 10).

    Returns:
    tuple: The coordinates (x, y) of the first pixel found with the target color, or None if no such pixel exists.
    """
    # Load the image from the given file path
    with Image.open(file_path) as img:
        pixels = img.convert("RGB").load()  # Convert to RGB if necessary

        # Get image dimensions
        width, height = img.size

        # Iterate over each pixel to find the target color within the tolerance
        for x in range(width):
            for y in range(height):
                current_pixel = pixels[x, y]
                if all(
                    abs(current_pixel[channel] - target_color[channel]) <= tolerance
                    for channel in range(3)
                ):
                    return (
                        x,
                        y,
                    )  # Return the position as soon as the color is found within tolerance

    return None  # Return None if the color is not found in the image


def take_screenshot(x, y, width, height, current_time):
    """
    Takes a screenshot of a specified rectangle and saves it.

    Parameters:
    x (int): The x-coordinate of the upper-left corner of the rectangle.
    y (int): The y-coordinate of the upper-left corner of the rectangle.
    width (int): The width of the rectangle.
    height (int): The height of the rectangle.
    """
    # Take a screenshot of the desired rectangle
    screenshot = pyautogui.screenshot(region=(x, y, width, height))

    # Save the screenshot
    screenshot.save(
        "C:\\Users\\karon\\Documents\\Cookies\\screenshot_" + current_time + ".png"
    )


def move_and_click(position):
    """
    Moves the mouse to the given position and performs a click.

    Parameters:
    position (tuple): The (x, y) coordinates where you want to move the mouse.
    """
    # Move the mouse to the specified position

    pyautogui.moveTo(position)

    # Click at the current location
    pyautogui.click()


def find_and_click_pattern(screenshot_path, pattern_path, threshold=0.5):
    # Load images
    screenshot = cv2.imread(screenshot_path, cv2.IMREAD_COLOR)
    pattern = cv2.imread(pattern_path, cv2.IMREAD_COLOR)

    # Convert images to grayscale
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    pattern_gray = cv2.cvtColor(pattern, cv2.COLOR_BGR2GRAY)

    # Perform template matching
    result = cv2.matchTemplate(screenshot_gray, pattern_gray, cv2.TM_CCOEFF_NORMED)

    # Find all locations where the matched result exceeds the threshold
    locations = np.where(result >= threshold)
    locations = list(
        zip(*locations[::-1])
    )  # Swap the coordinates and make a list of them

    # limit locations
    locations = locations[:4]

    # Get the size of the pattern image
    pattern_height, pattern_width = pattern_gray.shape

    # Loop over all the locations
    for loc in locations:
        # Calculate the center of the pattern for the current location
        center_x = loc[0] + pattern_width // 2
        center_y = loc[1] + pattern_height // 2

        # Move to the center of the pattern and click
        pyautogui.moveTo(center_x, center_y)
        pyautogui.click()

    # if not locations:
    # print("Pattern not found or matches are below threshold.")


def is_time_to_act(elapsed_time, time_refresh, tolerance):
    """
    Determines if the current time is within the tolerance of the scheduled time refresh.

    Args:
    elapsed_time (int): The total time elapsed since the start.
    time_refresh (int): The scheduled interval for action in seconds.
    tolerance (int): The acceptable range of seconds around the time_refresh to trigger action.

    Returns:
    bool: True if it's time to act, False otherwise.
    """
    return (
        elapsed_time % time_refresh <= tolerance
        or elapsed_time % time_refresh >= time_refresh - tolerance
    )


def check_time_refresh_condition(n, time_refresh_incrementation, max_refresh_time):
    """
    Checks if the updated time refresh value is within the allowed maximum limit.

    Args:
    n (int): The current increment step.
    time_refresh_incrementation (int): The increment value to be added per step.
    max_refresh_time (int): The maximum allowable time refresh value.

    Returns:
    bool: True if condition is met, False otherwise.
    """
    return n * time_refresh_incrementation <= max_refresh_time


def update_time_refresh_and_increment_n(
    time_refresh, time_refresh_start, time_refresh_incrementation, n
):
    """
    Updates the time_refresh value and increments the step counter n.

    Args:
    time_refresh (int): The current time refresh value (this argument will be modified).
    time_refresh_start (int): The initial time refresh value.
    time_refresh_incrementation (int): The increment value to be added per step.
    n (int): The current increment step (this argument will be incremented).

    Returns:
    tuple: A tuple containing updated values of time_refresh and n.
    """
    time_refresh += time_refresh_start + n * time_refresh_incrementation
    n += 1
    return time_refresh, n


def buying_buildings(x_coordinate, y_coordinates):
    """
    Automatically moves the mouse to specified coordinates and performs clicks,
    used for buying upgrades in a game or application.
    """
    for y in y_coordinates:
        pyautogui.moveTo(x_coordinate, y)
        pyautogui.click()
        time.sleep(0.3)  # Wait a short interval after each click


def buying_all_upgrades(x_coordinate, y_coordinate):
    """
    Automatically moves the mouse to specified coordinates and performs clicks,
    used for buying upgrades in a game or application.
    """
    pyautogui.moveTo(x_coordinate, y_coordinate)
    pyautogui.click()
    time.sleep(0.1)  # Wait a short interval after each click


def buying_store(x_coordinate, y_coordinate):
    """
    Automatically moves the mouse to specified coordinates and performs clicks,
    used for buying upgrades in a game or application.
    """
    pyautogui.moveTo(x_coordinate, y_coordinate)
    pyautogui.click()
    time.sleep(0.1)  # Wait a short interval after each click


def handle_screenshot_and_pattern_search(current_time_file, num):
    """
    Takes a screenshot, waits for a moment, and then searches for a specified pattern within that screenshot.

    Args:
    current_time_file (str): Timestamp or unique identifier used to name the screenshot file.
    """
    # Define file paths for the screenshot and the pattern
    screenshot_file_path = (
        f"C:\\Users\\karon\\Documents\\Cookies\\screenshot_{current_time_file}.png"
    )
    pattern_file_path = f"C:\\Users\\karon\\Documents\\Cookies\\cookie_{num}.png"

    # Take a screenshot
    take_screenshot(0, 0, 1920, 1080, current_time_file)

    # Wait a bit for file write operations to complete
    time.sleep(1)

    # Search for the pattern and click if found
    find_and_click_pattern(screenshot_file_path, pattern_file_path, threshold=0.5)
    try:
        os.remove(screenshot_file_path)
        # print(f"Deleted {screenshot_file_path}")
    except OSError as e:
        print(f"Error: {e.filename} - {e.strerror}.")


def main():
    pyautogui.FAILSAFE = True
    start_time = datetime.datetime.now()
    tolerance = 1
    time_refresh_start = 300
    time_refresh = time_refresh_start
    time_refresh_incrementation = 1
    max_refresh_time = 600
    n = 0
    y_upgrade = 203
    y_store = 175
    y_coordinates = [
        920,
        880,
        855,
        820,
        785,
        755,
        725,
        690,
        655,
        625,
        590,
        560,
        530,
        500,
        470,
        435,
        400,
        370,
        335,
        300,
        270,
    ]
    x_coordinate = 1770
    pyautogui.press("f6")
    # pyautogui.press("f6")
    while 1:
        current_time_file = datetime.datetime.now().strftime("%H_%M_%S")
        current_time = datetime.datetime.now()
        elapsed_time = round((current_time - start_time).total_seconds())
        if is_time_to_act(elapsed_time, time_refresh, tolerance):
            if check_time_refresh_condition(
                n, time_refresh_incrementation, max_refresh_time
            ):
                time_refresh, n = update_time_refresh_and_increment_n(
                    time_refresh, time_refresh_start, time_refresh_incrementation, n
                )
            else:
                time_refresh += max_refresh_time
            # click_circle(288, 493, 75, 12)
            buying_all_upgrades(x_coordinate, 225)
            buying_all_upgrades(x_coordinate, y_upgrade)
            buying_store(x_coordinate, y_store)
            buying_buildings(x_coordinate, y_coordinates)
            buying_all_upgrades(x_coordinate, y_upgrade)

        pyautogui.moveTo(300, 500)
        handle_screenshot_and_pattern_search(current_time_file, 1)
        handle_screenshot_and_pattern_search(current_time_file, 2)

        if keyboard.is_pressed("q"):  # If 'q' is pressed, it breaks the loop
            pyautogui.press("f6")
            break
        time.sleep(0.1)
        # pyautogui.press("f6")


if __name__ == "__main__":
    main()
