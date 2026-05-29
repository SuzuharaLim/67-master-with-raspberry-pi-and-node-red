import sys
import time
import threading
import multiprocessing
from camera import Camera
from gesture_analyzer import GestureAnalyzer
from streamer import Streamer
from mqtt_client import MQTTClient

latest_frame = None
frame_lock = threading.Lock()

def get_latest_frame():
    # Callback for Streamer to get the latest frame safely
    with frame_lock:
        if latest_frame is None:
            return None
        return latest_frame.copy()

def main():
    print("[System] Initializing modules...")
    cam = Camera(camera_index=0, width=320, height=240)
    analyzer = GestureAnalyzer(debounce_n=8, reset_m=5)
    mqtt = MQTTClient(broker="127.0.0.1", port=1883)
    streamer = Streamer(get_frame_callback=get_latest_frame, port=8080)

    try:
        cam.start()
        mqtt.start()
        streamer.start_in_thread()
        print("[System] All modules running. Press Ctrl+C to stop.")

        global latest_frame
        while True:
            frame = cam.read_frame()
            if frame is None:
                time.sleep(0.01)
                continue

            processed_frame, count_updated, counts = analyzer.analyze(frame)

            with frame_lock:
                latest_frame = processed_frame

            if count_updated:
                mqtt.publish_counts(counts)

    except KeyboardInterrupt:
        print("\n[System] Shutdown signal received.")
    except Exception as e:
        print(f"[System] Error occurred: {e}")
    finally:
        print("[System] Releasing resources...")
        cam.release()
        mqtt.stop()
        print("[System] Shutdown complete.")
        sys.exit(0)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()