from flask import Flask, Response
import cv2
import threading
import time

class Streamer:
    def __init__(self, get_frame_callback, host='0.0.0.0', port=8080):
        self.app = Flask(__name__)
        self.get_frame_callback = get_frame_callback
        self.host = host
        self.port = port

        @self.app.route('/video_feed')
        def video_feed():
            return Response(self._generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def _generate(self):
        while True:
            frame = self.get_frame_callback()
            if frame is None:
                continue
            
            ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
            if not ret:
                continue
            
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            time.sleep(0.06)

    def run_server(self):
        # 關閉 werkzeug 日誌以保持終端機乾淨
        import logging
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        
        self.app.run(host=self.host, port=self.port, debug=False, use_reloader=False)

    def start_in_thread(self):
        """以 Daemon Thread 啟動 Flask，避免阻塞主程式"""
        t = threading.Thread(target=self.run_server, daemon=True)
        t.start()
        print(f"[Streamer] MJPEG Server started at http://{self.host}:{self.port}/video_feed")