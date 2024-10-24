import utils.globals as g
from threading import Timer


def reset_eye():
    for i in [9, 10]:
        g.data["BlendShapes"][i]["e"] = True
        g.data["BlendShapes"][i]["s"] = -g.data["BlendShapes"][i]["v"] + 0.2
    for i in range(11, 23):
        g.data["BlendShapes"][i]["e"] = True
        g.data["BlendShapes"][i]["s"] = -g.data["BlendShapes"][i]["v"]
    for i in range(56, 62):
        g.data["BlendShapes"][i]["e"] = True
        g.data["BlendShapes"][i]["s"] = -g.data["BlendShapes"][i]["v"]


def disable_eye_yaw():
    for i in [57, 60]:
        g.data["BlendShapes"][i]["e"] = False


def disable_eye():
    for i in range(56, 62):
        g.data["BlendShapes"][i]["e"] = False


def reset_head():
    g.config["Tracking"]["Head"]["yaw_calibration"] = g.data["Rotation"][0]["v"]
    g.config["Tracking"]["Head"]["pitch_calibration"] = g.data["Rotation"][1]["v"]
    g.config["Tracking"]["Head"]["roll_calibration"] = g.data["Rotation"][2]["v"]
    print(g.config["Tracking"]["Head"]["yaw_calibration"],g.config["Tracking"]["Head"]["pitch_calibration"],g.config["Tracking"]["Head"]["roll_calibration"])
    for i in range(0, 3):
        g.data["Position"][i]["s"] = -g.data["Position"][i]["v"]
    for i in range(0, 3):
        g.data["Rotation"][i]["s"] = -g.data["Rotation"][i]["v"]

def up():
    g.data["Position"][2]["s"] += 5


def down():
    g.data["Position"][2]["s"] -= 5


def left():
    g.data["Position"][0]["s"] -= 5


def right():
    g.data["Position"][0]["s"] += 5


def head_pitch(flag=True):
    if flag:
        g.data["Rotation"][1]["s"] += 5
    else:
        g.data["Rotation"][1]["s"] -= 5


grab_status = {True: False, False: False}
def grab(value, index):
    grab_status[value] = not grab_status[value]
    print(value, grab_status[value])
    if grab_status[value]:
        g.controller.send_trigger(value, index, 1.0)
    else:
        g.controller.send_trigger(value, index, 0.0)


def trigger_press(value, index):
    print(1)
    g.controller.send_trigger(value, index, 1.0)


def trigger_release(value, index):
    print(0)
    g.controller.send_trigger(value, index, 0.0)

joystick_reset_timer = None
joystick_status = (0.0, 0.7)
joystick_step = 0.2

def reset_joystick(value, index):
    global joystick_reset_timer
    g.controller.send_joystick(value, index, 0.0, 0.0)
    if joystick_reset_timer is not None:
        joystick_reset_timer.cancel()
        joystick_reset_timer = None

    
def joystick_up(value, index):
    global joystick_status, joystick_step, joystick_reset_timer
    x, y = joystick_status
    if x > -0.7 and y == 0.7:
        x = max(x - joystick_step, -0.7)
    elif x <= -0.7 and y > -0.7:
        y = max(y - joystick_step, -0.7)
    elif y <= -0.7 and x < 0.7:
        x = min(x + joystick_step, 0.7)
    elif x >= 0.7 and y < 0.7:
        y = min(y + joystick_step, 0.7)
    joystick_status = (round(x, 1), round(y, 1))
    print(joystick_status)
    g.controller.send_joystick(value, index, joystick_status[0], joystick_status[1])
    if joystick_reset_timer is not None:
        joystick_reset_timer.cancel()
    joystick_reset_timer = Timer(1.5, lambda: reset_joystick(value, index))
    joystick_reset_timer.start()


def joystick_down(value, index):
    global joystick_status, joystick_step, joystick_reset_timer
    x, y = joystick_status
    if x < 0.7 and y == 0.7:
        x = min(x + joystick_step, 0.7)
    elif x >= 0.7 and y > -0.7:
        y = max(y - joystick_step, -0.7)
    elif y <= -0.7 and x > -0.7:
        x = max(x - joystick_step, -0.7)
    elif x <= -0.7 and y < 0.7:
        y = min(y + joystick_step, 0.7)
    joystick_status = (round(x, 1), round(y, 1))
    print(joystick_status)
    g.controller.send_joystick(value, index, joystick_status[0], joystick_status[1])
    if joystick_reset_timer is not None:
        joystick_reset_timer.cancel()
    joystick_reset_timer = Timer(1.5, lambda: reset_joystick(value, index))
    joystick_reset_timer.start()



def joystick_middle(value, index):
    global joystick_status
    g.controller.send_joystick(value, index, 0.0, 0.0)
    joystick_status = (0.0, 0.7)
    print(joystick_status)


fingers_enbale_status = {True: False, False: False}


def enable_fingers(value=None):
    global fingers_enbale_status
    finger_side = "LeftHandFinger" if value else "RightHandFinger"
    for d in g.data[finger_side]:
        d["e"] = fingers_enbale_status[value]
    fingers_enbale_status[value] = not fingers_enbale_status[value]
    print(g.data[finger_side])


def set_finger(value=None, index=None):
    finger_side = "LeftHandFinger" if value else "RightHandFinger"
    for d in g.data[finger_side]:
        d["e"] = False
    if g.default_data[finger_side][index]["v"] != 0.0:
        g.default_data[finger_side][index]["v"] = 0.0
    else:
        g.default_data[finger_side][index]["v"] = 1.0
    print(g.default_data[finger_side])


def enable_hand():
    g.config["Tracking"]["Hand"]["enable"] = not g.config["Tracking"]["Hand"]["enable"]
    if not g.config["Tracking"]["Hand"]["enable"]:
        g.controller.left_hand.position = (-0.1, -0.4, -0.2)
        g.controller.left_hand.rotation = (0.0, 0.0, 0.0, 1.0)
        g.controller.left_hand.finger = (0.0, 0.0, 0.0, 0.0, 0.0)
        g.controller.right_hand.position = (0.1, -0.4, -0.2)
        g.controller.right_hand.rotation = (0.0, 0.0, 0.0, 1.0)
        g.controller.right_hand.finger = (0.0, 0.0, 0.0, 0.0, 0.0)
        g.controller.update()


hand_reset_timer = None


def reset_hand(value=None):
    global hand_reset_timer
    hand_side = "LeftHandPosition" if value else "RightHandPosition"
    original_state = g.config["Tracking"]["Hand"]["only_front"]

    def update_z_shifting():
        global hand_reset_timer
        g.config["Tracking"]["Hand"]["z_shifting"] -= (
            g.data[hand_side][2]["v"] / g.config["Tracking"]["Hand"]["z_scalar"]
        )
        g.config["Tracking"]["Hand"]["only_front"] = original_state
        if hand_reset_timer is not None:
            hand_reset_timer.cancel()
            hand_reset_timer = None

    if hand_reset_timer is None:
        if g.config["Tracking"]["Hand"]["only_front"]:
            g.config["Tracking"]["Hand"]["only_front"] = False
            hand_reset_timer = Timer(1.0, update_z_shifting)
            hand_reset_timer.start()
        else:
            update_z_shifting()

def enable_tongue():
    g.config["Tracking"]["Tongue"]["enable"] = not g.config["Tracking"]["Tongue"]["enable"]

tongue_status = 0.0

def set_tongue():
    g.config["Tracking"]["Tongue"]["enable"] = False
    global tongue_status
    if tongue_status == 0.0:
        tongue_status = 1.0
    else:
        tongue_status = 0.0
    g.latest_data[52] = tongue_status
    g.latest_data[62] = 0.0
    g.latest_data[63] = 0.0
    g.data["BlendShapes"][52]["v"] = tongue_status
    g.data["BlendShapes"][62]["v"] = 0.0
    g.data["BlendShapes"][63]["v"] = 0.0
        
    