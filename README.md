# PC Hardware Performance Profiler

A simple real-time PC hardware monitoring dashboard built with Python and Tkinter. This tool provides a graphical user interface to display live performance metrics of your computer's hardware.

## Preview

![Monitor](https://github.com/user-attachments/assets/8d045df3-f6e0-4f36-a3e6-cb3f95eeedde)

## Features

- **Real-time CPU Usage:** Monitors and displays the current CPU load. The background color changes based on usage (green for low, orange for medium, red for high).
- **RAM Usage:** Shows the amount of used and total RAM in gigabytes.
- **GPU Statistics:** Displays GPU utilization, VRAM usage, and temperature. **Note:** This feature is only compatible with NVIDIA GPUs and requires the NVML library.
- **Webcam FPS Monitoring:** Measures and shows the frames per second of a connected webcam.

## Requirements

- Python 3.x
- `psutil`
- `pynvml`
- `opencv-python`
- `flet` 

You can install the required packages using pip:
`pip install psutil pynvml opencv-python flet`

## How to Run

1.  Make sure you have Python and the required libraries installed.
2.  Save the code as `PC Monitor Dashboard.py`.
3.  Run the script from your terminal:
         `python PC Monitor Dashboard.py`

## Note

- The GPU statistics will only be displayed if you have an NVIDIA GPU and the necessary drivers installed. If not, it will show an error message in the GPU section.
- The application requires access to a webcam for FPS monitoring. If no webcam is detected, it will display a "No Webcam" message.
