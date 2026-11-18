import math
import config


class CentroidTracker:
    def __init__(self):
        self.next_id = 0
        self.tracks = {}
        self.total_seen = {}

    def update(self, detections):
        for track in self.tracks.values():
            track["matched"] = False

        for det in detections:
            best_id = None
            best_distance = config.MAX_TRACK_DISTANCE

            for track_id, track in self.tracks.items():
                if track["color"] != det["color"] or track["matched"]:
                    continue
                distance = math.hypot(
                    det["center"][0] - track["center"][0],
                    det["center"][1] - track["center"][1],
                )
                if distance < best_distance:
                    best_distance = distance
                    best_id = track_id

            if best_id is None:
                best_id = self.next_id
                self.next_id += 1
                self.tracks[best_id] = {"color": det["color"], "path": []}
                self.total_seen[det["color"]] = self.total_seen.get(det["color"], 0) + 1

            track = self.tracks[best_id]
            track["center"] = det["center"]
            track["matched"] = True
            track["disappeared"] = 0
            track["path"].append(det["center"])
            track["path"] = track["path"][-config.TRAIL_LENGTH:]
            det["id"] = best_id

        for track_id in list(self.tracks.keys()):
            track = self.tracks[track_id]
            if not track["matched"]:
                track["disappeared"] += 1
                if track["disappeared"] > config.MAX_DISAPPEARED:
                    del self.tracks[track_id]
