import cv2
from deepface import DeepFace


class AntiSpoofingAPI:

    def __init__(self, detector_backend="yunet"):
        self.detector_backend = detector_backend

    def analyze_frame(self, frame):
        response_data = {"face_detected": False, "predictions": []}

        try:
            results = DeepFace.extract_faces(
                img_path=frame,
                detector_backend=self.detector_backend,
                anti_spoofing=True,
                enforce_detection=False,
            )

            if results and isinstance(results, list):
                response_data["face_detected"] = True

                for res in results:
                    facial_area = res.get("facial_area", {})

                    x = int(
                        facial_area.get("x")
                        if facial_area.get("x") is not None
                        else facial_area.get("left", 0)
                    )
                    y = int(
                        facial_area.get("y")
                        if facial_area.get("y") is not None
                        else facial_area.get("top", 0)
                    )
                    w = int(
                        facial_area.get("w")
                        if facial_area.get("w") is not None
                        else facial_area.get("width", 0)
                    )
                    h = int(
                        facial_area.get("h")
                        if facial_area.get("h") is not None
                        else facial_area.get("height", 0)
                    )

                    if w <= 10 or h <= 10:
                        continue

                    is_real = res.get("is_real", False)
                    confidence = res.get("confidence", 1.0)

                    face_data = {
                        "is_real": bool(is_real),
                        "status": "REAL" if is_real else "FAKE",
                        "confidence": float(confidence),
                        "box": {"x": x, "y": y, "width": w, "height": h},
                    }
                    response_data["predictions"].append(face_data)

        except Exception as e:
            response_data["error"] = str(e)

        return response_data
