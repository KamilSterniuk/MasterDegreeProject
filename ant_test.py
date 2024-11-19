import os

from psychopy import visual, core, event
import random
import csv

# Tworzenie okna na głównym monitorze (screen=1)
win = visual.Window(fullscr=True, color="grey", units="pix", screen=1)

# Czas trwania różnych etapów
cue_time = 0.1  # 100 ms
post_cue_time = 0.4  # 400 ms
target_time = 1.7  # 1700 ms
feedback_time = 1.5  # 1500 ms na odpowiedź

# Ładowanie grafik
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


def trial_ant_test():
    """Test próbny ANT"""
    for _ in range(5):  # 10 prób
        fixation.draw()
        win.flip()
        core.wait(random.uniform(0.4, 1.6))

        cue_type = random.choice(["none", "center", "double", "spatial"])
        target_type = random.choice(["compatible", "incompatible", "neutral"])
        position = random.choice(["left", "right"])

        y_position = show_cue(cue_type)
        show_target(target_type, position, y_position, feedback=True)

    # Komunikat po zakończeniu testu próbnego
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
    event.waitKeys()  # Czeka na dowolny klawisz

    main_ant_test()  # Uruchomienie głównego testu


def main_ant_test():
    """Główny test ANT"""
    trial_data = []
    results_dir = "results"
    target_folder = get_highest_numbered_folder(results_dir)

    # Tworzenie folderu, jeśli nie istnieje
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # Ścieżka do pliku CSV
    csv_file_path = os.path.join(target_folder, "ant_results.csv")

    for trial_num in range(10):  # 10 prób
        fixation.draw()
        win.flip()
        core.wait(random.uniform(0.4, 1.6))

        cue_type = random.choice(["none", "center", "double", "spatial"])
        target_type = random.choice(["compatible", "incompatible", "neutral"])
        position = random.choice(["left", "right"])

        y_position = show_cue(cue_type)
        response, reaction_time, correct_response, arrow_y_pos = show_target(target_type, position, y_position, feedback=False)
        is_correct = response == correct_response if response else False

        if arrow_y_pos == 100:
            target_y_pos = 'top'
        else:
            target_y_pos = 'bottom'

        trial_data.append({
            "trial": trial_num + 1,
            "cue_type": cue_type,
            "target_type": target_type,
            "target_direction": position,
            "target_y_position": target_y_pos,
            "reaction_time": reaction_time,
            "correct": is_correct,
        })

    # Zapis danych do pliku CSV
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


def get_highest_numbered_folder(base_dir):
    """Znajduje katalog o najwyższym numerze w podanym katalogu bazowym."""
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)  # Tworzy katalog, jeśli go nie ma
        return os.path.join(base_dir, "example1")

    existing_folders = [
        folder for folder in os.listdir(base_dir) if folder.startswith("example") and folder[7:].isdigit()
    ]
    if not existing_folders:
        return os.path.join(base_dir, "example1")

    max_number = max(int(folder[7:]) for folder in existing_folders)
    return os.path.join(base_dir, f"example{max_number}")
