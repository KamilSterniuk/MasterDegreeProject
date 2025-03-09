import cv2
import os

# Ścieżka do pliku wideo
video_path = "ASMR_long1.mp4"

# Nazwa folderu, w którym zapiszą się klatki
output_folder = "frames_ASMR1_long_120"

# Stworzenie folderu, jeśli nie istnieje
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Otwarcie pliku wideo
cap = cv2.VideoCapture(video_path)

# Sprawdzenie, czy plik wideo został poprawnie otwarty
if not cap.isOpened():
    print("Błąd: Nie można otworzyć pliku wideo.")
    exit()

# Licznik klatek
frame_count = 0

# Liczba klatek do wyciągnięcia
frames_to_extract = 120

while frame_count < frames_to_extract:
    # Odczyt klatki
    ret, frame = cap.read()

    # Sprawdzenie, czy klatka została poprawnie odczytana
    if not ret:
        print("Koniec filmu lub błąd odczytu.")
        break

    # Ścieżka zapisu z folderem
    output_path = os.path.join(output_folder, f"frame_{frame_count + 1}.jpg")
    cv2.imwrite(output_path, frame)
    print(f"Zapisano: {output_path}")

    # Zwiększenie licznika
    frame_count += 1

# Zwolnienie zasobów
cap.release()
print("Zakończono przetwarzanie.")