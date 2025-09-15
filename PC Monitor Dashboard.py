import flet as ft
import psutil
from pynvml import *
import cv2
import time
from threading import Thread
from collections import deque

def main(page: ft.Page):
    # Modern UI theme
    page.title = "System Performance Profiler"
    page.bgcolor = ft.Colors.BLUE_GREY_900
    page.theme_mode = ft.ThemeMode.DARK
    page.window.maximizable = False
    page.window.resizable = False
    page.window.width = 500  # Increased for better readability
    page.window.height = 700  # Increased for better layout
    page.update()


    # Stats holders
    cpu_percent = ft.Text("0", size=28, weight=ft.FontWeight.BOLD)
    cpu_status = ft.Icon(ft.Icons.COMPUTER, color=ft.Colors.GREEN_400, size=36)
    mem_info = ft.Text("0/0 GB", size=20)
    mem_status = ft.Icon(ft.Icons.MEMORY, color=ft.Colors.GREEN_400, size=36)
    gpu_data = ft.Text("N/A", size=16)
    gpu_status = ft.Icon(ft.Icons.DEVELOPER_BOARD, color=ft.Colors.GREEN_400, size=36)
    fps_text = ft.Text("0", size=28, weight=ft.FontWeight.BOLD)
    fps_status = ft.Icon(ft.Icons.SLOW_MOTION_VIDEO, color=ft.Colors.CYAN_400, size=36)

    # Use: with_opacity(opacity, color)
    def get_card_bg(opac, color):
        return ft.Colors.with_opacity(opac, color)

    # Helper: Color for intensity
    def get_bar_color(val):
        if val >= 70:
            return ft.Colors.RED_400
        elif val > 40:
            return ft.Colors.ORANGE_400
        else:
            return ft.Colors.GREEN_400

    # Pretty cards for each stat
    def stat_card(icon, value, text, bg_color):
        return ft.Container(
            content=ft.Row(
                [
                    icon,
                    ft.VerticalDivider(width=12, color=ft.Colors.with_opacity(0.1, ft.Colors.WHITE)),
                    ft.Column([
                        value,
                        text
                    ], spacing=2)
                ], vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            bgcolor=bg_color,
            margin=10,
            padding=20,
            border_radius=16,
            shadow=ft.BoxShadow(blur_radius=18, color=ft.Colors.BLUE_GREY_800)
        )

    # Layout with fixed with_opacity bug
    stats_column = ft.Column([
        stat_card(cpu_status, cpu_percent, ft.Text("CPU Usage", size=16), get_card_bg(0.13, ft.Colors.RED_400)),
        stat_card(mem_status, mem_info, ft.Text("RAM Usage", size=16), get_card_bg(0.13, ft.Colors.LIGHT_GREEN_400)),
        stat_card(gpu_status, gpu_data, ft.Text("GPU Stats", size=16), get_card_bg(0.13, ft.Colors.GREEN_400)),
        stat_card(fps_status, fps_text, ft.Text("Webcam FPS", size=16), get_card_bg(0.13, ft.Colors.CYAN_400))
    ], alignment=ft.MainAxisAlignment.SPACE_AROUND, expand=True)

    page.add(
        ft.Column(
            [
                ft.Container(
                    content=ft.Text("🌀 System Monitor Dashboard", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_100),
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(top=16, bottom=10),
                ),
                stats_column,
                ft.Text("Made By Manas Kushwaha", size=13, color=ft.Colors.with_opacity(0.4, ft.Colors.WHITE), italic=True)
            ],
            alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True
        )
    )

    # Threads: live stats
    def update_stats():
        while True:
            cpu = psutil.cpu_percent()
            cpu_percent.value = f"{cpu:.1f} %"
            cpu_status.color = get_bar_color(cpu)
            cpu_percent.update()
            cpu_status.update()
            
            mem = psutil.virtual_memory()
            mem_used = mem.used / (1024 ** 3)
            mem_total = mem.total / (1024 ** 3)
            mem_info.value = f"{mem_used:.2f} / {mem_total:.2f} GB"
            mem_status.color = get_bar_color(mem.percent)
            mem_info.update()
            mem_status.update()

            try:
                nvmlInit()
                h = nvmlDeviceGetHandleByIndex(0)
                util = nvmlDeviceGetUtilizationRates(h).gpu
                mem_info_g = nvmlDeviceGetMemoryInfo(h)
                temp = nvmlDeviceGetTemperature(h, NVML_TEMPERATURE_GPU)
                vram_used = mem_info_g.used / (1024 ** 3)
                vram_total = mem_info_g.total / (1024 ** 3)
                gpu_data.value = f"Util: {util}% | VRAM: {vram_used:.2f}/{vram_total:.2f} GB\nTemp: {temp}°C"
                gpu_status.color = get_bar_color(util)
            except Exception:
                gpu_data.value = "No NVIDIA GPU"
                gpu_status.color = ft.Colors.GREY_600
            gpu_data.update()
            gpu_status.update()
            page.update()
            time.sleep(1.0)

    def get_fps():
        cap = cv2.VideoCapture(0)
        ts = deque(maxlen=32)
        while True:
            ret, frame = cap.read()
            if not ret:
                fps_text.value = "No Webcam"
                fps_status.color = ft.Colors.RED_400
                page.update()
                break
            ts.append(time.time())
            if len(ts) >= 2:
                fps = (len(ts) - 1) / (ts[-1] - ts[0])
                fps_text.value = f"{fps:.1f} fps"
                if fps >= 60:
                    fps_status.color = ft.Colors.GREEN_400
                elif fps >= 24:
                    fps_status.color = ft.Colors.ORANGE_400
                else:
                    fps_status.color = ft.Colors.RED_400
                fps_text.update()
                fps_status.update()
            page.update()
            time.sleep(1 / 30)
        cap.release()

    Thread(target=update_stats, daemon=True).start()
    Thread(target=get_fps, daemon=True).start()

ft.app(target=main)
