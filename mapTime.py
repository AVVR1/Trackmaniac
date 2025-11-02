import json
import os

class mapTime:
    def __init__(self, map_name):
        self.map_name = map_name
        self.file_path = f"times_{map_name}.json"
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)
        
    def get_times(self):
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def add_time(self, user, time):
        times = self.get_times()
        times.append([user, time])
        times.sort(key=lambda x: x[1])  # Sort by time
        with open(self.file_path, 'w') as f:
            json.dump(times, f)

    def remove_time(self, index):
        times = self.get_times()
        if 0 <= index < len(times):
            times.pop(index)
            with open(self.file_path, 'w') as f:
                json.dump(times, f)

    def delete_file(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)