import cv2
import os
import numpy as np
import pandas as pd
import re

# Ścieżki
input_folder = "frames_ASMR1_long_120"  # Folder z klatkami
output_folder = "frames_ASMR1_11_output"  # Folder na klatki z punktami
csv_file_path = "20250308170651_asmr_play_raw_gaze.csv"  # Plik CSV

# Wczytanie danych
try:
    df = pd.read_csv(csv_file_path, delimiter=";")
    time_data = [float(t) for t in df.columns[1:] if t]
    x_data = [float(v) for v in df.iloc[0, 1:] if v]
    y_data = [float(v) for v in df.iloc[1, 1:] if v]
except Exception as e:
    print(f"Błąd wczytywania danych: {e}")
    exit()

# Tworzenie folderu wyjściowego
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Parametry
fps = 30
frame_duration = 1 / fps
height, width = 1080, 1920  # Rozdzielczość obrazu (dostosuj jeśli inna)

# Lista klatek
frame_files = [f for f in os.listdir(input_folder) if f.endswith(".jpg")]
frame_files.sort(key=lambda x: int(re.search(r'\d+', x).group()))

# Tablica do akumulacji punktów dla heatmapy
heatmap_accumulator = np.zeros((height, width), dtype=np.float32)
points_history = []  # Historia punktów do łączenia liniami

frame_count = 0
data_index = 0

for frame_file in frame_files:
    frame_path = os.path.join(input_folder, frame_file)
    frame = cv2.imread(frame_path)
    if frame is None:
        print(f"Błąd: Nie udało się wczytać {frame_path}.")
        continue

    frame_time = frame_count * frame_duration

    while (data_index < len(time_data) - 1 and 
           abs(time_data[data_index] - frame_time) > abs(time_data[data_index + 1] - frame_time)):
        data_index += 1

    if data_index >= len(time_data):
        print("Koniec danych przed końcem klatek.")
        break

    x = int(x_data[data_index])
    y = int(y_data[data_index])
    y_inv = height - y  # Odwrócenie osi Y

    # Dodanie punktu do historii
    points_history.append((x, y_inv))

    # Dodanie do heatmapy
    cv2.circle(heatmap_accumulator, (x, y_inv), 20, 1, -1)  # Promień 20 dla rozproszenia

    # Tworzenie heatmapy
    heatmap_blur = cv2.GaussianBlur(heatmap_accumulator, (51, 51), 0)
    heatmap_normalized = np.uint8(255 * heatmap_blur / (heatmap_blur.max() + 1e-10))
    heatmap_color = cv2.applyColorMap(heatmap_normalized, cv2.COLORMAP_JET)

    # Nałożenie heatmapy na ramkę
    alpha = 0.3  # Przezroczystość heatmapy
    frame_with_heatmap = cv2.addWeighted(frame, 1.0, heatmap_color, alpha, 0.0)

    # Rysowanie linii między punktami
    for i in range(1, len(points_history)):
        cv2.line(frame_with_heatmap, points_history[i-1], points_history[i], (0, 255, 0), 1)

    # Rysowanie aktualnego punktu
    cv2.circle(frame_with_heatmap, (x, y_inv), 5, (0, 0, 255), -1)

    # Zapis
    output_path = os.path.join(output_folder, f"klatka_{frame_count:04d}.jpg")
    cv2.imwrite(output_path, frame_with_heatmap)
    print(f"Zapisano: {output_path}, czas: {frame_time:.3f}s, X: {x}, Y: {y}")

    frame_count += 1

print("Zakończono przetwarzanie.")