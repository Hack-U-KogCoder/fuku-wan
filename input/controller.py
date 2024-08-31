from gpiozero import MCP3008, Button
import keyboard
import time

joystick_x = MCP3008(channel=0)
joystick_y = MCP3008(channel=1)
determination_button = Button(17, bounce_time=0.01)
function_button = Button(27, bounce_time=0.01)

center_x = 0.5
center_y = 0.5
dead_zone = 0.2

last_direction = "Center"


def get_direction(x, y):
    if abs(x - center_x) < dead_zone and abs(y - center_y) < dead_zone:
        return "Center"
    if x < center_x - dead_zone:
        return "Down"
    if x > center_x + dead_zone:
        return "Up"
    if y < center_y - dead_zone:
        return "Right"
    if y > center_y + dead_zone:
        return "Left"


def handle_determination():
    keyboard.press_and_release("enter")


def handle_function():
    keyboard.press_and_release("ctrl+g")


def handle_joystick_direction(direction):
    global last_direction
    if direction != last_direction:
        if direction == "Right":
            keyboard.press_and_release("tab")
        elif direction == "Left":
            keyboard.press_and_release("shift+tab")
        elif direction == "Up":
            keyboard.press_and_release("ctrl+k")
        elif direction == "Down":
            keyboard.press_and_release("ctrl+j")
        last_direction = direction


determination_button.when_pressed = handle_determination
function_button.when_pressed = handle_function

try:
    while True:
        x_value = joystick_x.value
        y_value = joystick_y.value
        direction = get_direction(x_value, y_value)

        handle_joystick_direction(direction)

        # print(f"X: {x_value:.3f}, Y: {y_value:.3f}, Direction: {direction}")
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Finish!")
finally:
    joystick_x.close()
    joystick_y.close()
