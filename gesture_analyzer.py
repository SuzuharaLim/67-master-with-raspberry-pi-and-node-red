import cv2
import mediapipe as mp
import collections

class GestureAnalyzer:
    def __init__(self, debounce_n=10, reset_m=5):
        # 初始化 MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,       # <--- 關鍵修改：67 迷因必須同時偵測「雙手」
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # 用來記錄雙手 Y 軸高度差的歷史軌跡 (長度 15 約等於半秒鐘)
        self.y_diff_history = collections.deque(maxlen=15)
        
        # 迷因計數器與冷卻狀態機
        self.counts = {"67_meme": 0}
        self.cooldown = 0

    def analyze(self, frame):
        count_updated = False
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)
        
        meme_detected = False
        hand_y_positions = []

        if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 2:
            # 當畫面上確實出現兩隻手時
            for hand_landmarks in results.multi_hand_landmarks:
                # 取「中指底部關節 (MCP, 節點 9)」的 Y 座標，代表這隻手的高度
                hand_y_positions.append(hand_landmarks.landmark[9].y)
                # 畫出炫酷骨架
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                
            # 計算兩隻手的高度差
            if len(hand_y_positions) == 2:
                diff = hand_y_positions[0] - hand_y_positions[1]
                self.y_diff_history.append(diff)
                
                # 【67 迷因核心演算法：天平般的交替上下擺動】
                if len(self.y_diff_history) >= 10:
                    max_diff = max(self.y_diff_history)
                    min_diff = min(self.y_diff_history)
                    
                    # 如果高度差的最大值與最小值差距夠大，且跨越正負零點 (代表左手與右手一高一低互換)
                    # 0.08 代表雙手交換高度的幅度需達到畫面高度的 8% 以上
                    if max_diff > 0.08 and min_diff < -0.08:
                        meme_detected = True

        # 狀態機：冷卻時間遞減 (避免你瘋狂搖手時，計數器爆表)
        if self.cooldown > 0:
            self.cooldown -= 1
        
        # 觸發迷因計數！
        if meme_detected and self.cooldown == 0:
            self.counts["67_meme"] += 1
            self.cooldown = 20          # 觸發後冷卻約 20 幀
            count_updated = True
            self.y_diff_history.clear() # 清空歷史軌跡重新計算

        # 在畫面上印出 67 迷因計數
        cv2.putText(frame, f"67 Meme Count: {self.counts['67_meme']}", (10, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                    
        # 觸發時出現魔性大字！
        if meme_detected or self.cooldown > 10:
            cv2.putText(frame, "SIX-SEVEN!!!", (10, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4)

        return frame, count_updated, self.counts.copy()