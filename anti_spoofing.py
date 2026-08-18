import cv2
from deepface import DeepFace

class AntiSpoofingDetector:
    def __init__(self):
        pass

    def process_frame(self, frame):
        try:
            # anti_spoofing=True memanggil model MiniFASNet bawaan DeepFace
            results = DeepFace.extract_faces(
                img_path=frame,
                detector_backend="yunet",  # YuNet kencang di CPU; gunakan 'opencv' jika Yunet error
                anti_spoofing=True,
                enforce_detection=False,
            )

            if results and isinstance(results, list):
                for res in results:
                    facial_area = res.get("facial_area", {})

                    x = int(facial_area.get("x", 0))
                    y = int(facial_area.get("y", 0))
                    w = int(facial_area.get("w", 0))
                    h = int(facial_area.get("h", 0))

                    if w <= 10 or h <= 10:
                        continue

                    is_real = res.get("is_real", False)
                    score = res.get("antispoof_score", 0.0)

                    if is_real:
                        color = (0, 255, 0)  # Hijau = ASLI
                        label = f"ASLI ({score:.2f})"
                    else:
                        color = (0, 0, 255)  # Merah = PALSU / LAYAR HP
                        label = f"PALSU ({score:.2f})"

                    # Gambar Bounding Box & Label
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(
                        frame,
                        label,
                        (x, max(y - 10, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        color,
                        2,
                    )

        except Exception as e:
            pass

        return frame


if __name__ == "__main__":
    detector = AntiSpoofingDetector()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[ERROR] Kamera tidak dapat diakses!")
        exit()

    print("[INFO] Program Anti-Spoofing Berjalan. Tekan 'q' untuk keluar.")
 
    frame_count = 0
    process_every_n_frames = 2  # Set ke 3 atau 4 jika CPU terasa berat
    processed_frame = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        frame_count += 1

        if frame_count % process_every_n_frames == 0 or processed_frame is None:
            processed_frame = detector.process_frame(frame)

        cv2.imshow("Anti-Spoofing Detection", processed_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()