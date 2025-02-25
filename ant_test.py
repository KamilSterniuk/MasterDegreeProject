import os
import random
import csv
import time
import sys
from psychopy import visual, core, event
import multiprocessing

from eye_tracker_recorder import get_target_folder

# Global parameters
cue_time = 0.1      # 100 ms
post_cue_time = 0.4   # 400 ms
target_time = 1.7     # 1700 ms
feedback_time = 1.5   # 1500 ms

# Create window (e.g. on screen=1)
win = visual.Window(fullscr=True, color="grey", units="pix", screen=1)

# Load images
fixation = visual.ImageStim(win, image="images/plus.png", pos=(0, 0), size=(40, 40))
cue = visual.ImageStim(win, image="images/asteriks.png", pos=(0, 0), size=(40, 40))
arrow_compatible_left = visual.ImageStim(win, image="images/compatible_left.png", size=(325, 64))
arrow_compatible_right = visual.ImageStim(win, image="images/compatible_right.png", size=(325, 64))
arrow_incompatible_left = visual.ImageStim(win, image="images/incompatible_left.png", size=(325, 64))
arrow_incompatible_right = visual.ImageStim(win, image="images/incompatible_right.png", size=(325, 64))
arrow_neutral_left = visual.ImageStim(win, image="images/neutral_left.png", size=(325, 64))
arrow_neutral_right = visual.ImageStim(win, image="images/neutral_right.png", size=(325, 64))


def show_cue(cue_type):
    y_position = None
    if cue_type == "none":
        fixation.draw()
        win.flip()
        core.wait(post_cue_time)
    elif cue_type == "center":
        cue.draw()
        fixation.draw()
        win.flip()
        core.wait(cue_time)
        fixation.draw()
        win.flip()
        core.wait(post_cue_time)
    elif cue_type == "double":
        cue.pos = (0, 100)
        cue.draw()
        cue.pos = (0, -100)
        cue.draw()
        fixation.draw()
        win.flip()
        core.wait(cue_time)
        fixation.draw()
        win.flip()
        core.wait(post_cue_time)
    elif cue_type == "spatial":
        y_position = 100 if random.choice([True, False]) else -100
        cue.pos = (0, y_position)
        cue.draw()
        fixation.draw()
        win.flip()
        core.wait(cue_time)
        fixation.draw()
        win.flip()
        core.wait(post_cue_time)
    cue.pos = (0, 0)
    return y_position


def show_target(target_type, position, y_position, feedback=True):
    arrow_y_pos = y_position if y_position is not None else (100 if random.choice([True, False]) else -100)
    if target_type == "compatible":
        arrow = arrow_compatible_right if position == "right" else arrow_compatible_left
    elif target_type == "incompatible":
        arrow = arrow_incompatible_right if position == "right" else arrow_incompatible_left
    else:
        arrow = arrow_neutral_right if position == "right" else arrow_neutral_left

    arrow.pos = (0, arrow_y_pos)
    arrow.draw()
    fixation.draw()
    win.flip()

    clock = core.Clock()
    keys = event.waitKeys(maxWait=target_time, keyList=["left", "right"], timeStamped=clock)

    win.flip()
    correct_response = "right" if "right" in arrow.image else "left"
    if keys:
        response, reaction_time = keys[0]
        if feedback and response != correct_response:
            feedback_text = visual.TextStim(
                win,
                text=f"Incorrect!\nCorrect answer: {correct_response.upper()}",
                color="red",
                bold=True,
                pos=(0, 0),
                height=30
            )
            feedback_text.draw()
            win.flip()
            core.wait(feedback_time)
        return response, reaction_time, correct_response, arrow_y_pos
    else:
        if feedback:
            feedback_text = visual.TextStim(
                win,
                text=f"No response!\nCorrect answer: {correct_response.upper()}",
                color="red",
                bold=True,
                pos=(0, 0),
                height=30
            )
            feedback_text.draw()
            win.flip()
            core.wait(feedback_time)
        return None, None, correct_response, arrow_y_pos


def run_eye_tracker_registration(target_folder, stop_event):
    """
    Function to run in a separate process.
    Initializes eye tracker registration (using a fresh instance) and waits until stop_event is set.
    Then calls stop_and_process() and terminates.
    """
    # Use non-interactive backend for Matplotlib
    import matplotlib
    matplotlib.use("Agg")
    from eye_tracker_recorder import EyeTrackerRecorder
    # For ANT test, use subfolder "ant_test"
    recorder = EyeTrackerRecorder(target_folder=target_folder, subfolder="ant_test")
    recorder.start()
    print("Eye tracker registration started in subprocess.")
    while not stop_event.is_set():
        time.sleep(1)
    print("Stop event received in subprocess.")
    recorder.stop_and_process()
    # Allow some time for background processing
    time.sleep(5)
    print("Subprocess eye tracker registration finished.")


def trial_ant_test():
    """Trial ANT test"""
    for _ in range(5):
        fixation.draw()
        win.flip()
        core.wait(random.uniform(0.4, 1.6))
        cue_type = random.choice(["none", "center", "double", "spatial"])
        target_type = random.choice(["compatible", "incompatible", "neutral"])
        position = random.choice(["left", "right"])
        y_position = show_cue(cue_type)
        show_target(target_type, position, y_position, feedback=True)
    end_message = visual.TextStim(
        win,
        text="Thank you for completing the trial.\n\nPress any key to continue to the main test.",
        color="black",
        bold=True,
        pos=(0, 0),
        height=24
    )
    end_message.draw()
    win.flip()
    event.waitKeys()
    main_ant_test()


def main_ant_test():
    """Main ANT test with continuous eye tracker registration in a separate process."""
    trial_data = []
    results_dir = "results"
    target_folder = get_target_folder(results_dir)
    # Create "ant_test" subfolder in the example folder
    ant_test_folder = os.path.join(target_folder, "ant_test")
    if not os.path.exists(ant_test_folder):
        os.makedirs(ant_test_folder)
    csv_file_path = os.path.join(ant_test_folder, "ant_results.csv")

    stop_event = multiprocessing.Event()
    p = multiprocessing.Process(target=run_eye_tracker_registration, args=(ant_test_folder, stop_event))
    p.start()

    for trial_num in range(10):
        fixation.draw()
        win.flip()
        core.wait(random.uniform(0.4, 1.6))
        cue_type = random.choice(["none", "center", "double", "spatial"])
        target_type = random.choice(["compatible", "incompatible", "neutral"])
        position = random.choice(["left", "right"])
        y_position = show_cue(cue_type)
        response, reaction_time, correct_response, arrow_y_pos = show_target(target_type, position, y_position, feedback=False)
        is_correct = response == correct_response if response else False
        target_y_pos = 'top' if arrow_y_pos == 100 else 'bottom'
        trial_data.append({
            "trial": trial_num + 1,
            "cue_type": cue_type,
            "target_type": target_type,
            "target_direction": position,
            "target_y_position": target_y_pos,
            "reaction_time": reaction_time,
            "correct": is_correct,
        })

    print("Main test trials completed.")
    stop_event.set()
    p.join()
    print("Eye tracker subprocess joined.")

    with open(csv_file_path, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["trial", "cue_type", "target_type", "target_direction", "target_y_position", "reaction_time", "correct"],
            delimiter=';'
        )
        writer.writeheader()
        writer.writerows(trial_data)

    print(f"Results saved to {csv_file_path}")
    for trial in trial_data:
        print(trial)
    win.close()


if __name__ == '__main__':
    trial_ant_test()
