from psychopy import visual, core, event, data
import random

# Ustawienia eksperymentu
win = visual.Window(fullscr=True, color="grey", units="pix")

# Czas trwania różnych etapów (w sekundach)
cue_time = 0.1  # 100 ms
post_cue_time = 0.4  # 400 ms
target_time = 1.7  # 1700 ms maksymalny czas reakcji

# Ładowanie grafik z folderu 'images'
fixation = visual.ImageStim(win, image="images/plus.png", pos=(0, 0), size=(40, 40))
cue = visual.ImageStim(win, image="images/asteriks.png", pos=(0, 0), size=(40, 40))
arrow_compatible_left = visual.ImageStim(win, image="images/compatible_left.png", size=(325, 64))
arrow_compatible_right = visual.ImageStim(win, image="images/compatible_right.png", size=(325, 64))
arrow_incompatible_left = visual.ImageStim(win, image="images/incompatible_left.png", size=(325, 64))
arrow_incompatible_right = visual.ImageStim(win, image="images/incompatible_right.png", size=(325, 64))
arrow_neutral_left = visual.ImageStim(win, image="images/neutral_left.png", size=(325, 64))
arrow_neutral_right = visual.ImageStim(win, image="images/neutral_right", size=(325, 64))

# Funkcja do wyświetlania wskazówki
def show_cue(cue_type):
    if cue_type == "none":
        fixation.draw()  # Krzyżyk zawsze widoczny
        win.flip()
        core.wait(post_cue_time)
    elif cue_type == "center":
        cue.draw()
        fixation.draw()  # Krzyżyk wyświetlany razem z cue
        win.flip()
        core.wait(cue_time)
        win.flip()
        fixation.draw()  # Wyświetlamy krzyżyk samodzielnie po cue
        win.flip()
        core.wait(post_cue_time)
    elif cue_type == "double":
        cue.pos = (0, 100)  # wyświetl nad krzyżykiem
        cue.draw()
        cue.pos = (0, -100)  # wyświetl pod krzyżykiem
        cue.draw()
        fixation.draw()
        win.flip()
        core.wait(cue_time)
        win.flip()
        fixation.draw()
        win.flip()
        core.wait(post_cue_time)
    elif cue_type == "spatial":
        cue.pos = (0, 100) if random.choice([True, False]) else (0, -100)  # góra/dół
        cue.draw()
        fixation.draw()
        win.flip()
        core.wait(cue_time)
        win.flip()
        fixation.draw()
        win.flip()
        core.wait(post_cue_time)
    cue.pos = (0, 0)  # reset pozycji


# Funkcja do wyświetlania bodźca i mierzenia czasu reakcji
def show_target(target_type, position, y_position):
    # Ustawienie pozycji strzałek (góra lub dół)
    arrow_y_pos = 100 if y_position == "top" else -100

    # Wybór odpowiedniego bodźca
    if target_type == "compatible":
        arrow = arrow_compatible_right if position == "right" else arrow_compatible_left
        correct_response = "right" if position == "right" else "left"
    elif target_type == "incompatible":
        arrow = arrow_incompatible_right if position == "right" else arrow_incompatible_left
        correct_response = "right" if position == "right" else "left"
    else:  # Neutral
        arrow = arrow_neutral_right if position == "right" else arrow_neutral_left
        correct_response = "right" if position == "right" else "left"

    # Ustawienie pozycji i wyświetlenie bodźca
    arrow.pos = (0, arrow_y_pos)
    arrow.draw()
    fixation.draw()  # Krzyżyk na środku
    win.flip()

    clock = core.Clock()  # Użycie zegara do pomiaru czasu reakcji
    keys = event.waitKeys(maxWait=target_time, keyList=["left", "right"], timeStamped=clock)

    win.flip()
    if keys:
        response, reaction_time = keys[0]
        is_correct = (response == correct_response)
        return reaction_time, is_correct
    return None, False  # brak reakcji

# Główna pętla prób
trial_data = []
for i in range(10):  # 10 prób do przykładu
    fixation.draw()
    win.flip()
    core.wait(random.uniform(0.4, 1.6))  # losowa przerwa 400-1600 ms

    # Wybór typu wskazówki i bodźca
    cue_type = random.choice(["none", "center", "double", "spatial"])
    target_type = random.choice(["compatible", "incompatible", "neutral"])
    position = random.choice(["left", "right"])  # kierunek środkowej strzałki
    y_position = random.choice(["top", "bottom"])  # pozycja góra/dół

    show_cue(cue_type)
    reaction_time, is_correct = show_target(target_type, position, y_position)

    # Zbieranie danych z próby
    trial_data.append({
        "trial": i + 1,
        "cue_type": cue_type,
        "target_type": target_type,
        "position": position,
        "y_position": y_position,
        "reaction_time": reaction_time,
        "correct": is_correct
    })

# Zapis wyników do pliku
with open("ant_results.csv", "w") as f:
    f.write("trial,cue_type,target_type,position,y_position,reaction_time,correct\n")
    for trial in trial_data:
        f.write(
            f"{trial['trial']},{trial['cue_type']},{trial['target_type']},{trial['position']},{trial['y_position']},{trial['reaction_time']},{trial['correct']}\n")

# Wyświetlanie wyników na konsoli
win.close()
for trial in trial_data:
    print(trial)
