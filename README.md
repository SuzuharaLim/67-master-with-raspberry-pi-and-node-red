# 🕺 67 Meme Edge AI Vision Sensor (67迷因邊緣視覺感測器)

![Python](https://img.shields.io/badge/Python-3.11-blue.svg) ![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.9-orange.svg) ![MQTT](https://img.shields.io/badge/Protocol-MQTT-green.svg) ![Node-RED](https://img.shields.io/badge/Dashboard-Node--RED-red.svg) ![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20ARM64-lightgrey.svg)

本專案是一個輕量級的**邊緣 AI 視覺感測器**，專門用來即時偵測網路爆紅的 **「67 迷因 (Six-Seven Meme)」** 手勢動作（雙手平攤、交替上下魔性擺動）。

系統採用純粹無 GUI 架構，底層結合 MediaPipe 手部骨架追蹤與時間序列震盪分析 (Time-Series Analysis)，並實作多執行緒解耦。運算結果會透過 **MQTT** 即時發送至 **Node-RED**，同時內建輕量級 **MJPEG 串流伺服器** 提供即時骨架影像，最終支援使用 PyInstaller 跨平台打包成「免安裝單一執行檔」。

---

## 📂 專案目錄結構

```text
67_meme_project/
├── main.py                # 系統進入點 (管理多執行緒與生命週期)
├── camera.py              # OpenCV 影像擷取封裝模組
├── gesture_analyzer.py    # MediaPipe AI 推論與 67 迷因幾何震盪演算法
├── streamer.py            # Flask MJPEG 網頁即時推播伺服器
├── mqtt_client.py         # MQTT 通訊模組
├── requirements.txt       # 鎖定版本的黃金相容套件清單
└── README.md              # 專案說明文件
```

---

## 🛠️ 1. 核心環境準備 (必讀)

本專案針對 MediaPipe 與 Protobuf 的底層相容性進行了極度嚴格的測試。請務必使用我們提供的 `requirements.txt` 以避開著名的版本衝突 Bug。

**`requirements.txt` 黃金配置內容：**
```text
numpy==1.26.4
protobuf==3.20.3
opencv-python-headless==4.9.0.80
mediapipe==0.10.9
paho-mqtt==2.0.0
Flask==3.0.2
```

---

## 🪟 2. Windows 平台指南

### 2.1 本機執行測試
1. 開啟終端機 (PowerShell 或 CMD)，進入專案資料夾。
2. 確保沒有殘留會干擾的套件（如 TensorFlow），並安裝依賴：
   ```bash
   pip uninstall -y tensorflow tensorflow-intel onnx protobuf mediapipe
   pip install -r requirements.txt
   ```
3. 執行主程式：
   ```bash
   python main.py
   ```

### 2.2 打包成免安裝單一執行檔 (`.exe`)
在 Windows 上產出的 `.exe` 可以直接拷貝至其他無 Python 環境的 Windows 10/11 電腦執行。

```bash
# 安裝打包工具
pip install pyinstaller

# 執行終極打包指令 (排除 TensorFlow，並強制收集 MediaPipe 模型)
pyinstaller --name GestureEdgeApp --onefile --collect-all mediapipe --exclude-module tensorflow main.py
```
> 💡 **Troubleshooting小提醒：**  
> 如果打包過程中報錯 `The 'pathlib' package is an obsolete backport...`，請執行 `pip uninstall -y pathlib` 後再次執行打包指令即可。

打包完成後，在 `dist/` 資料夾內即可找到 **`GestureEdgeApp.exe`**。

---

## 🍓 3. Linux / 樹莓派 ARM64 平台指南

> ⚠️ **極度重要：** 你的樹莓派 (Raspberry Pi 4B / 5) 必須安裝 **64-bit (AArch64)** 版本的作業系統。MediaPipe 不支援 32-bit 系統。

### 3.1 樹莓派環境安裝與執行
1. 更新系統並安裝 OpenCV 必備的 Linux 系統圖形庫：
   ```bash
   sudo apt update
   sudo apt install -y libgl1-mesa-glx libglib2.0-0
   ```
2. 進入專案資料夾，安裝 Python 依賴：
   ```bash
   pip install -r requirements.txt
   ```
3. 執行測試：
   ```bash
   python main.py
   ```

### 3.2 在樹莓派上打包成免安裝執行檔 (ELF Binary)
要產出 Linux ARM64 的執行檔，**必須在樹莓派本機上進行打包**。指令與 Windows 完全相同：

```bash
pip install pyinstaller
pyinstaller --name GestureEdgeApp --onefile --collect-all mediapipe --exclude-module tensorflow main.py
```
打包完成後，在 `dist/` 資料夾內會生成名為 **`GestureEdgeApp`** 的二進位檔案。
以後在任何同架構的樹莓派上，只需賦予權限並執行：
```bash
chmod +x GestureEdgeApp
./GestureEdgeApp
```

---

## 📊 4. Node-RED 儀表板與 MQTT 設置

無論你在哪一個系統上運行，都需要架設 MQTT Broker 與 Node-RED 以作為視覺化中樞。

### 4.1 安裝 MQTT Broker (Mosquitto)
* **Windows:** 前往 [Mosquitto 官網](https://mosquitto.org/download/) 下載 `.exe` 安裝，並在系統「服務」中啟動 `Mosquitto Broker`。
* **Linux / 樹莓派:** 
  ```bash
  sudo apt install -y mosquitto mosquitto-clients
  sudo systemctl enable mosquitto && sudo systemctl start mosquitto
  ```

### 4.2 安裝 Node-RED
* **Windows:** 需先安裝 Node.js，然後在終端機執行：`npm install -g --unsafe-perm node-red`，接著輸入 `node-red` 啟動。
* **Linux / 樹莓派 (一鍵安裝腳本):**
  ```bash
  bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)
  sudo systemctl enable nodered.service && sudo systemctl start nodered.service
  ```

### 4.3 匯入 67 迷因專屬儀表板
1. 打開瀏覽器進入 Node-RED 介面：`http://127.0.0.1:1880` (若在其他設備則輸入該設備 IP)。
2. 點擊右上角選單 ➜ **管理選單 (Manage palette)** ➜ 安裝 **`node-red-dashboard`** 套件。
3. 點擊右上角選單 ➜ **匯入 (Import)**，貼上以下 JSON 程式碼：

<details>
<summary><b>👉 點此展開並複製 JSON 程式碼</b></summary>

```json
[{"id":"mqtt_in_node","type":"mqtt in","z":"d3725b8f.6f23e8","name":"接收迷因計數","topic":"edge/gesture/counts","qos":"0","datatype":"json","broker":"mqtt_broker_node","nl":false,"rap":true,"rh":0,"inputs":0,"x":190,"y":160,"wires":[["function_node"]]},{"id":"function_node","type":"function","z":"d3725b8f.6f23e8","name":"解析 67 迷因","func":"var memeCount = { payload: msg.payload[\"67_meme\"] || 0 };\nreturn memeCount;","outputs":1,"timeout":"","noerr":0,"initialize":"","finalize":"","libs":[],"x":410,"y":160,"wires":[["ui_text_node"]]},{"id":"ui_text_node","type":"ui_text","z":"d3725b8f.6f23e8","group":"ui_group_count","order":1,"width":0,"height":0,"name":"","label":"🕺 SIX-SEVEN 發動次數：","format":"{{msg.payload}} 次","layout":"row-spread","className":"","x":650,"y":160,"wires":[]},{"id":"ui_template_node","type":"ui_template","z":"d3725b8f.6f23e8","group":"ui_group_stream","name":"AI 即時串流影像","order":1,"width":"12","height":"9","format":"<div style=\"display: flex; flex-direction: column; align-items: center; width: 100%;\">\n    <h3 style=\"color: #ff0055; font-weight: bold;\">67 偵測</h3>\n    <img src=\"http://127.0.0.1:8080/video_feed\" alt=\"等待 AI 攝影機連線...\" style=\"max-width: 100%; border-radius: 8px; border: 3px solid #ff0055; box-shadow: 0px 4px 10px rgba(0,0,0,0.3);\">\n</div>","storeOutMessages":true,"fwdInMessages":true,"resendOnRefresh":true,"templateScope":"local","className":"","x":200,"y":260,"wires":[[]]},{"id":"mqtt_broker_node","type":"mqtt-broker","name":"本機 Broker","broker":"127.0.0.1","port":"1883","clientid":"","autoConnect":true,"usetls":false,"protocolVersion":"4","keepalive":"60","cleansession":true,"birthTopic":"","birthQos":"0","birthPayload":"","birthMsg":{},"closeTopic":"","closeQos":"0","closePayload":"","closeMsg":{},"willTopic":"","willQos":"0","willPayload":"","willMsg":{},"userProps":"","sessionExpiry":""},{"id":"ui_group_count","type":"ui_group","name":"迷因統計區","tab":"ui_tab_main","order":2,"disp":true,"width":"6","collapse":false,"className":""},{"id":"ui_group_stream","type":"ui_group","name":"邊緣視覺畫面","tab":"ui_tab_main","order":1,"disp":true,"width":"12","collapse":false,"className":""},{"id":"ui_tab_main","type":"ui_tab","name":"67 迷因儀表板","icon":"dashboard","order":1,"disabled":false,"hidden":false}]
```
</details>

4. 點擊右上角紅色的 **部署 (Deploy)** 按鈕。

---

## 🚀 5. 啟動與操作指南

1. 開啟你的 Python 程式 (`python main.py` 或點擊打包後的執行檔)。
2. 開啟瀏覽器，前往 **`http://127.0.0.1:1880/ui`** 進入專屬儀表板（注意：若在跨設備存取，請將 127.0.0.1 換成設備的真實 IP）。
3. 站在攝影機前，將雙手平攤，並交替上下魔性擺動。
4. 當系統偵測到高度差震盪超過閾值，畫面上會噴出紅色的 `SIX-SEVEN!!!` 字樣，並即時將計數更新至 Node-RED 儀表板上！