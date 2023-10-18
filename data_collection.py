import mediapipe as mp
import numpy as np
import cv2

def inFrame(lst):
    return all(landmark.visibility > 0.6 for landmark in [lst[28], lst[27], lst[15], lst[16]])

def collect_data(name):
    cap = cv2.VideoCapture(0)
    holistic = mp.solutions.pose.Pose()
    drawing = mp.solutions.drawing_utils
    X = []

    while True:
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        results = holistic.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if results.pose_landmarks and inFrame(results.pose_landmarks.landmark):
            X.append([(landmark.x - results.pose_landmarks.landmark[0].x, landmark.y - results.pose_landmarks.landmark[0].y) for landmark in results.pose_landmarks.landmark])
        else:
            cv2.putText(frame, "Make Sure Full body visible", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        drawing.draw_landmarks(frame, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
        cv2.putText(frame, str(len(X)), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("window", frame)

        if cv2.waitKey(1) == 27 or len(X) > 80:
            cv2.destroyAllWindows()
            cap.release()
            break

    np.save(f"{name}.npy", np.array(X))
    print(np.array(X).shape)

def main():
    name = input("Enter the name of the Asana : ")
    collect_data(name)

if __name__ == "__main__":
    main()
