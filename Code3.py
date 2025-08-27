from tkinter import *
import psutil
from pynvml import *
import cv2
import time
from collections import deque
cap = cv2.VideoCapture(0)
window = Tk()
window.title("Real-Time CPU Usage")
window.geometry("500x500")
window.configure(bg="darkblue")
title = Label(window, text="System Monitor Dashboard", font=("Consolas", 24, "bold"), bg="darkblue", fg="white")
title.pack(pady=10)
cpu_frame=Frame(window,bg="dodgerblue",relief="ridge",borderwidth=10)
cpu_frame.pack(pady=10,padx=10,fill="x")
cpu_label_static = Label(cpu_frame,bg="dodgerblue",font=("Consolas",20,"bold"))
cpu_label = Label(cpu_frame,bg="dodgerblue",font=("Consolas",20,"bold"))
cpu_label.pack(pady=10)
mem_frame=Frame(window,bg="dodgerblue",relief="ridge",borderwidth=10)
mem_frame.pack(pady=10,padx=10,fill="x")
mem_label=Label(mem_frame,font=("Consolas",14,"bold"),bg="dodgerblue")
mem_label.pack(pady=20)
gpu_frame=Frame(window,bg="dodgerblue",relief="ridge",borderwidth=10)
gpu_frame.pack(pady=10,padx=10,fill="x")
gpu_label = Label(gpu_frame,bg="dodgerblue",font=("Consolas",14,"bold"))
gpu_label.pack(pady=10)
fps_frame=Frame(window,bg="dodgerblue",relief="ridge",borderwidth=10)
fps_frame.pack(pady=10,padx=10,fill="x")
fps_label = Label(fps_frame,bg="dodgerblue",font=("Consolas",15,"bold"))
fps_label.pack(pady=10)
def update_cpu():
    cpu_usage = psutil.cpu_percent()
    if cpu_usage>70:
        color='red'
    elif 40<cpu_usage<=70:
        color='orange'
    else:
        color='green'
    cpu_label.config(text=f"CPU Usage:{cpu_usage}%")
    cpu_frame.config(bg=color)
    cpu_label.config(bg=color)

    window.after(1000, update_cpu)
def update_memory():
    memory_usage=psutil.virtual_memory()
    if (memory_usage.used/memory_usage.total)*100>70:
        color='red'
    elif 40<(memory_usage.used/memory_usage.total)*100<=70:
        color='orange'
    else:
        color='green'
    mem_label.config(text=f"Used memory/Total(RAM):{memory_usage.used/1024**3:.2f}/{memory_usage.total/1024**3:.2f} GB ")
    mem_frame.config(bg=color)
    mem_label.config(bg=color)
    window.after(1000, update_memory)
def update_gpu():
    try:
        nvmlInit()
        gpu_handle = nvmlDeviceGetHandleByIndex(0)
        gpu_util = nvmlDeviceGetUtilizationRates(gpu_handle).gpu
        mem_info = nvmlDeviceGetMemoryInfo(gpu_handle)
        gpu_temp = nvmlDeviceGetTemperature(gpu_handle,NVML_TEMPERATURE_GPU)
        mem_used = mem_info.used / (1024 ** 3)
        mem_total = mem_info.total / (1024 ** 3)
        avg=(gpu_temp+(mem_used/mem_total)*100+gpu_util)/3
        if avg>70:
            color='red'
        elif 40<avg<=70:
            color='orange'
        else:
            color='green'
        gpu_label.config(text=f"GPU Usage: {gpu_util}%\nGPU VRAM Usage/Total: {mem_used:.2f} GB/{mem_total:.2f} GB\nGPU temp:{gpu_temp} C")
        gpu_frame.config(bg=color)
        gpu_label.config(bg=color)
    except NVMLError as error:
        gpu_label.config(text=f"Error initializing NVML:\nNo nivdia gpu found")
    
    window.after(1000, update_gpu)
timestamps=deque(maxlen=30)
def update_fps():
    ret,frame=cap.read()
    if ret:
        timestamps.append(time.time())
        if len(timestamps)>=2:
            fps=(len(timestamps)-1)/(timestamps[-1]-timestamps[0])
            if fps>=60:
                color='Green'
            elif 24<=fps<60:
                color='orange'
            else:
                color='red'
            fps_label.config(text=f"FPS of Webcam: {fps:.2f}")
            fps_frame.config(bg=color)
            fps_label.config(bg=color)
    else:
        fps_label.config(text="No Webcam")
    window.after(1,update_fps)
update_cpu()
update_memory()
update_gpu()
update_fps()
window.mainloop()
cap.release()
cv2.destroyAllWindows()
