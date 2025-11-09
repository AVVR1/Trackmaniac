import os
from dotenv import load_dotenv
import motor.motor_asyncio

load_dotenv()
mongoURI = os.getenv('MONGO_URI')
mongoConnect = motor.motor_asyncio.AsyncIOMotorClient(mongoURI)

db = mongoConnect['trackmaniac']  # database name
collection = db['mapleaderboards']  # collection name

async def update_times(map_name, times):
    updatedTimes = {
    'map_leaderboard': map_name,
    'times': times
    }
    await collection.replace_one({'map_leaderboard' : map_name}, updatedTimes)

class mapLeaderboard:
    def __init__(self, map_name):
        self.map_name = map_name

    async def get_times(self):
        if await collection.find_one({'map_leaderboard' : self.map_name}) is None:
            return []
        mapLB = await collection.find_one({'map_leaderboard': self.map_name})
        return mapLB.get('times', [])

    async def add_time(self, user, time):
        doc = await collection.find_one({'map_leaderboard' : self.map_name})
        if (doc is None) or (doc.get('times') is None):
            await collection.insert_one({'map_leaderboard': self.map_name, 'times': [[user, time]]})

        times = await self.get_times()
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
        await update_times(self.map_name, times)

    async def remove_time(self, index):
        times = await self.get_times()
        if 0 <= index < len(times):
            times.pop(index)
            await update_times(self.map_name, times)
            return

    async def delete_map(self):
        await collection.delete_one({'map_leaderboard': self.map_name})