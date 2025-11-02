from pymongo import MongoClient
import os

mongoURI = os.getenv('MONGO_URI')

class mapLeaderboard:
    def __init__(self, map_name):
        # Connect to MongoDB
        self.client = MongoClient(mongoURI)
        self.db = self.client['trackmaniac']  # database name
        self.collection = self.db['mapleaderboards']  # collection name
        self.map_name = map_name

    def get_times(self):
        try:
            # Find document for this map
            result = self.collection.find_one({'map_name': self.map_name})
            return result['times'] if result and 'times' in result else []
        except:
            return []

    def add_time(self, user, time):
        times = self.get_times()
        times.append([user, time])
        times.sort(key=lambda x: x[1])  # Sort by time

        # Only keep best time per user
        for i in range(len(times) - 1):
            if times[i][0] == times[i+1][0]:        # same name
                if times[i][1] >= times[i+1][1]:    # better or equal time
                    times.pop(i)
                    continue
                else:
                    times.pop(i+1)
                    continue

        # Update or insert document
        self.collection.update_one(
            {'map_name': self.map_name},
            {'$set': {'times': times}},
            upsert=True
        )

    def remove_time(self, index):
        times = self.get_times()
        if 0 <= index < len(times):
            times.pop(index)
            self.collection.update_one(
                {'map_name': self.map_name},
                {'$set': {'times': times}}
            )

    def delete_map(self):
        self.collection.delete_one({'map_name': self.map_name})