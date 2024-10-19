import psutil
import time
from PIL import Image

# Preprocess image to improve OCR accuracy
def preprocess_image(image):
    gray = image.convert('L')  # Convert to grayscale
    binarized_image = gray.point(lambda x: 0 if x < 128 else 255)  # Simple thresholding
    return binarized_image


# Track performance metrics (processing time, memory, and CPU usage)
def track_performance():
    start_time = time.time()
    initial_memory = psutil.virtual_memory().used
    initial_cpu = psutil.cpu_percent(interval=None)
    return start_time, initial_memory, initial_cpu


# Report performance metrics
def report_performance(start_time, initial_memory, initial_cpu):
    processing_duration = time.time() - start_time
    final_memory = psutil.virtual_memory().used
    memory_used = final_memory - initial_memory
    final_cpu = psutil.cpu_percent(interval=None) - initial_cpu
    return processing_duration, memory_used, final_cpu