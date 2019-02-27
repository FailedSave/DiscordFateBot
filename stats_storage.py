import pickle
import os

stats = {}

def increment_fate():
    stats["fates_delivered"] += 1

async def save_stats():
    output = open('stats.pkl', 'wb')

    pickle.dump(stats, output)
    output.close()

def load_stats():
    global stats
    if (os.path.isfile('stats.pkl')):
        input = open('stats.pkl', 'rb')
        stats = pickle.load(input)
        input.close()
    else:
        stats = {}
        stats["fates_delivered"] = 0