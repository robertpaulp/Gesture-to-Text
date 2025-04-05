# Import model dependencies
from model.src.hand_tracker_nms import HandTrackerNMS
from rapidfuzz import process
import model.src.extra as srcextra
import joblib
import cv2
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'model'))

# Model setup
PALM_MODEL_PATH = "model/models/palm_detection_without_custom_op.tflite"
LANDMARK_MODEL_PATH = "model/models/hand_landmark.tflite" 
ANCHORS_PATH = "model/models/anchors.csv"

class GestureRecognizer:
    def __init__(self):
        self.detector = HandTrackerNMS(
            PALM_MODEL_PATH,
            LANDMARK_MODEL_PATH, 
            ANCHORS_PATH,
            box_shift=0.2,
            box_enlarge=1.3
        )
        self.gesture_clf = joblib.load('model/models/gesture_clf.pkl')
        self.int_to_char = srcextra.classes
        self.word = []
        self.letter = ""
        self.static_gesture = 0
        self.none_count = 0
        
    def process_image(self, frame):
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        points, bboxes, joints = self.detector(image)
        
        if points is not None:
            srcextra.draw_points(points, frame)
            pred_sign = srcextra.predict_sign(joints, self.gesture_clf, self.int_to_char)
            srcextra.draw_sign(pred_sign, frame, (50, 560))
            
            if pred_sign is not None:
                self.add_letter(pred_sign)

            # # Return the predicted gesture
            # return pred_sign
            return "".join(self.word) if len(self.word) > 0 else None
        else:
            self.none_count += 1
            if self.none_count >= 3 and len(self.word) > 0:
                completed_word = "".join(self.word)
                self.word = []
                self.letter = ""
                self.static_gesture = 0

                self.correct_word(completed_word)

                return completed_word

        return None
    
    def add_letter(self, letter):
        self.none_count = 0
        if letter == self.letter:
            self.static_gesture += 1
            if self.static_gesture >= 3:
                self.word.append(letter)
                self.letter = ""
                self.static_gesture = 0
        else:
            self.static_gesture = 0
            self.letter = letter

    def correct_word(self, word):
        with open("words_alpha.txt") as f:
            english_words = set(f.read().split())

        # Găsește cel mai apropiat cuvânt din dicționar
        suggestion, score, _ = process.extractOne(word, english_words)

        print(f"Cuvânt introdus: {word}")
        print(f"Sugestie: {suggestion} (similaritate: {score:.2f}%)")