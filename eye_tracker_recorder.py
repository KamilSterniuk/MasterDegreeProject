import os
import time
import numpy as np
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import gc
import pandas as pd
import threading
from eyex.api import Sample

# Default screen settings and colors
Xres = 1920
Yres = 1080
COLS = ['#fce94f', '#edd400', '#c4a000', '#fcaf3e', '#f57900', '#ce5c00',
        '#e9b96e', '#c17d11', '#8f5902', '#8ae234', '#73d216', '#4e9a06',
        '#729fcf', '#3465a4', '#204a87', '#ad7fa8', '#75507b', '#5c3566',
        '#ef2929', '#cc0000', '#a40000', '#eeeeec', '#d3d7cf', '#babdb6',
        '#888a85', '#555753', '#2e3436']


def get_target_folder(results_dir="results"):
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    existing_folders = [folder for folder in os.listdir(results_dir)
                        if folder.startswith("example") and folder[7:].isdigit()]
    if existing_folders:
        max_number = max(int(folder[7:]) for folder in existing_folders)
    else:
        max_number = 1
    target_folder = os.path.join(results_dir, f"example{max_number}")
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    return target_folder


def centeroid(points):
    points = np.array(points)
    return np.mean(points[:, 0]), np.mean(points[:, 1])

def calc_radius(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)



def calculate_heatmap(x, y, file, show_points=True):
    title = 'Heatmap'
    grid_size = 25
    h = 150
    x_grid = np.arange(0 - h, Xres + h, grid_size)
    y_grid = np.arange(0 - h, Yres + h, grid_size)
    x_mesh, y_mesh = np.meshgrid(x_grid, y_grid)
    xc = x_mesh + grid_size / 2
    yc = y_mesh + grid_size / 2

    def kde_quartic(d, h):
        dn = d / h
        return (15 / 16) * (1 - dn ** 2) ** 2

    intensity = np.zeros(xc.shape)
    for j in range(len(xc)):
        for k in range(len(xc[0])):
            p_total = 0
            for i in range(len(x)):
                d = math.hypot(xc[j][k] - x[i], yc[j][k] - y[i])
                if d <= h:
                    p_total += kde_quartic(d, h)
            intensity[j, k] = p_total

    fig, ax = plt.subplots()
    ax.pcolormesh(x_mesh, y_mesh, intensity, cmap='turbo', shading='gouraud')
    ax.set_xlim((0, Xres))
    ax.set_ylim((0, Yres))
    ax.set_title(title)
    ax.set_aspect('equal')
    if show_points:
        plt.plot(x, y, 'ro-', linewidth=0.5)
    plt.savefig(file, dpi=300, bbox_inches="tight")
    plt.close(fig)


def calculate_gazeplot(x, y, time_btw, file):
    title = 'Gazeplot'
    fixation_radius = 100
    radius_ratio = 0.7
    x_p = y_p = 0
    count = 1
    no_points = len(x) / 100  # minimal number of points for a fixation
    fig, ax = plt.subplots()
    points = []
    for i in range(len(x)):
        if points:
            x_c, y_c = centeroid(points)
            radius = calc_radius([x[i], y[i]], [x_c, y_c])
            if radius <= fixation_radius:
                points.append([x[i], y[i]])
            else:
                if len(points) >= no_points:
                    r = radius_ratio * len(points)
                    circle = plt.Circle((x_c, y_c), r, color=COLS[count % len(COLS)])
                    ax.add_patch(circle)
                    ax.annotate(str(count), xy=(x_c, y_c), fontsize=12, ha="center", color="navy")
                    if x_p and y_p:
                        plt.plot([x_p, x_c], [y_p, y_c], color="gray")
                    x_p, y_p = x_c, y_c
                    count += 1
                points = [[x[i], y[i]]]
        else:
            points.append([x[i], y[i]])
    ax.set_aspect('equal')
    ax.set_xlim((0, Xres))
    ax.set_ylim((0, Yres))
    ax.set_title(title)
    plt.savefig(file, dpi=300, bbox_inches="tight")
    plt.close(fig)


def calculate_fixation_statistics(x, y, times, fixation_radius=100):
    min_points = len(x) / 100
    fixations = []
    current_fixation = {'points': [], 'start_time': None, 'end_time': None}
    for i in range(len(x)):
        point = (x[i], y[i])
        t = times[i]
        if not current_fixation['points']:
            current_fixation['points'].append(point)
            current_fixation['start_time'] = t
            current_fixation['end_time'] = t
        else:
            centroid = np.mean(current_fixation['points'], axis=0)
            distance = np.sqrt((point[0] - centroid[0]) ** 2 + (point[1] - centroid[1]) ** 2)
            if distance <= fixation_radius:
                current_fixation['points'].append(point)
                current_fixation['end_time'] = t
            else:
                if len(current_fixation['points']) >= min_points:
                    fixation_centroid = np.mean(current_fixation['points'], axis=0)
                    duration = current_fixation['end_time'] - current_fixation['start_time']
                    fixations.append({
                        'centroid': fixation_centroid,
                        'duration': duration,
                        'start_time': current_fixation['start_time'],
                        'end_time': current_fixation['end_time'],
                        'latency': current_fixation['start_time']  # temporary
                    })
                current_fixation = {'points': [point], 'start_time': t, 'end_time': t}
    if current_fixation['points'] and len(current_fixation['points']) >= min_points:
        fixation_centroid = np.mean(current_fixation['points'], axis=0)
        duration = current_fixation['end_time'] - current_fixation['start_time']
        fixations.append({
            'centroid': fixation_centroid,
            'duration': duration,
            'start_time': current_fixation['start_time'],
            'end_time': current_fixation['end_time'],
            'latency': current_fixation['start_time']
        })
    for i in range(1, len(fixations)):
        fixations[i]['latency'] = fixations[i]['start_time'] - fixations[i - 1]['end_time']
    return fixations


class EyeTrackerRecorder:
    def __init__(self, target_folder=None):
        if target_folder is None:
            target_folder = get_target_folder("results")
        self.target_folder = target_folder  # np. results/exampleX/
        self.data = []
        from eye_interface_safe import EyeXInterfaceSafe  # Upewnij się, że ten moduł jest dostępny
        self.eye_api = EyeXInterfaceSafe()
        self.eye_api.on_event = [lambda x: self.data.append(x)]
        self.recording = False
        self.start_time = None

    def start(self):
        time.sleep(2)
        self.data = []
        self.recording = True
        self.start_time = time.time()
        print("Eye tracker registration started.")

    def process_session(self, session_suffix=""):
        self.recording = False
        print("Processing session data...")
        if not self.data:
            print("No data from eye tracker!")
            return

        # Ustal podfolder w zależności od session_suffix:
        # Jeśli session_suffix == "play" → folder: asmr_video
        # Jeśli session_suffix == "ant" → folder: ant_test
        if session_suffix == "play":
            session_folder = "asmr_video"
        elif session_suffix == "ant":
            session_folder = "ant_test"
        else:
            session_folder = session_suffix if session_suffix else "default"

        # Tworzymy strukturę folderów: results/exampleX/session_folder/data oraz .../plots
        recorder_folder = os.path.join(self.target_folder, session_folder)
        os.makedirs(recorder_folder, exist_ok=True)
        self.data_folder = os.path.join(recorder_folder, "data")
        self.plots_folder = os.path.join(recorder_folder, "plots")
        os.makedirs(self.data_folder, exist_ok=True)
        os.makedirs(self.plots_folder, exist_ok=True)

        # Przetwarzanie danych (analogiczne do poprzedniej implementacji)
        eyedata = np.zeros((len(self.data), 13), dtype=float)
        k = 0
        for i in range(len(self.data) - 1):
            current = self.data[i]
            next_sample = self.data[i + 1]
            if isinstance(current, Sample) and isinstance(next_sample, Sample):
                eyedata[k, 0] = current.timestamp
                eyedata[k, 1] = current.x
                eyedata[k, 2] = current.y
                eyedata[k, 3] = current.timestamp
                eyedata[k, 4] = 1
                eyedata[k, 5] = 1
                eyedata[k, 6] = next_sample.x + 10
                eyedata[k, 7] = next_sample.y + 5
                eyedata[k, 8] = 50
                eyedata[k, 9] = next_sample.x - 10
                eyedata[k, 10] = next_sample.y - 5
                eyedata[k, 11] = 45
                eyedata[k, 12] = next_sample.timestamp
                k += 1
        eyedata = eyedata[:k, :]
        eyedata = eyedata[(eyedata[:, 1] > 0) & (eyedata[:, 1] <= Xres)]
        eyedata = eyedata[(eyedata[:, 2] > 0) & (eyedata[:, 2] <= Yres)]
        if len(eyedata) == 0:
            print("No data in eyedata after filtering!")
            return

        analiza = np.zeros((len(eyedata), 5), dtype=float)
        analiza[:, 1] = eyedata[:, 1]
        analiza[:, 2] = Yres - eyedata[:, 2]
        RefTimeIndex = 0
        for i in range(1, len(eyedata) - 1):
            diff1 = round((eyedata[i, 0] - eyedata[i - 1, 0]), 0)
            diff2 = round((eyedata[i, 3] - eyedata[i - 1, 3]) * 1000, 0)
            diff3 = round((eyedata[i, 12] - eyedata[i - 1, 12]) * 1000, 0)
            if (diff1 == diff2) and (diff2 == diff3):
                RefTimeIndex = i
                break
        analiza[:, 3] = (eyedata[:, 0] - eyedata[RefTimeIndex, 0]) / 1000
        analiza[1:, 4] = eyedata[1:, 0] - eyedata[0:-1, 0]
        analiza[:, 0] = eyedata[RefTimeIndex, 3] + analiza[:, 3]
        basename = time.strftime("%Y%m%d%H%M%S", time.localtime(self.start_time)) + "_" + session_suffix
        hm_file = os.path.join(self.plots_folder, f"{basename}_hm.png")
        hm_nolines = os.path.join(self.plots_folder, f"{basename}_hm_nolines.png")
        gp_file = os.path.join(self.plots_folder, f"{basename}_gp.png")
        calculate_heatmap(analiza[:, 1], analiza[:, 2], hm_file, show_points=True)
        calculate_heatmap(analiza[:, 1], analiza[:, 2], hm_nolines, show_points=False)
        calculate_gazeplot(analiza[:, 1], analiza[:, 2], analiza[1:, 4], gp_file)
        fixation_stats = calculate_fixation_statistics(analiza[:, 1], analiza[:, 2], analiza[:, 3], fixation_radius=100)
        print("\nFixation statistics:")
        print("Number of fixations:", len(fixation_stats))
        for idx, fix in enumerate(fixation_stats, start=1):
            print(f"Fixation {idx}: Latency: {fix['latency']:.2f} s, Duration: {fix['duration']:.2f} s, Position: ({fix['centroid'][0]:.1f}, {fix['centroid'][1]:.1f})")
        fixations_file = os.path.join(self.data_folder, f"{basename}_fixations.csv")
        raw_gaze_file = os.path.join(self.data_folder, f"{basename}_raw_gaze.csv")
        row_latency = ["Latency:"] + [f"{fix['latency']:.2f}" for fix in fixation_stats]
        row_duration = ["Duration:"] + [f"{fix['duration']:.2f}" for fix in fixation_stats]
        row_position = ["Position:"] + [f"({fix['centroid'][0]:.1f}, {fix['centroid'][1]:.1f})" for fix in fixation_stats]
        row_fix_count = ["Number of fixations:", len(fixation_stats)] + [""] * (len(fixation_stats) - 1)
        df_fixations = pd.DataFrame([row_latency, row_duration, row_position, row_fix_count])
        row_x = ["X (px):"] + [f"{x:.1f}" for x in analiza[:, 1]]
        row_y = ["Y (px):"] + [f"{y:.1f}" for y in analiza[:, 2]]
        time_et = ["Time (s):"] + [f"{t:.3f}" for t in analiza[:, 3]]
        df_raw_gaze = pd.DataFrame([time_et, row_x, row_y])
        df_fixations.to_csv(fixations_file, header=False, index=False, sep=';')
        df_raw_gaze.to_csv(raw_gaze_file, header=False, index=False, sep=';')
        print("Fixations saved to:", fixations_file)
        print("Raw gaze data saved to:", raw_gaze_file)
        gc.collect()
        self.data = []
        self.start_time = time.time()
