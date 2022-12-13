import os
from pymongo import MongoClient
from urllib.parse import quote_plus

MONGO_USERNAME = quote_plus(os.environ["MONGO_USERNAME"])
MONGO_PASSWORD = quote_plus(os.environ["MONGO_PASSWORD"])
MONGO_URL = os.environ["MONGO_URL"]
CONNECTION_STRING = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_URL}"

client = MongoClient(CONNECTION_STRING)
db = client["C4G"]
users_collections = db["users"]
global_stats_collections = db["global_stats"]


def insert_user(user_id, username, max_steps):
    _user_id = users_collections.find_one({}, {"user_id": 1})
    if not _user_id:
        users_collections.insert_one(
            {
                "user_id": user_id,
                "username": username,
                "max_steps": max_steps
            }
        )
    else:
        user = users_collections.find_one(_user_id)
        max_steps = max(user["max_steps"], max_steps)
        users_collections.update_one(
            _user_id,
            {
                "$set":
                {
                    "max_steps": max_steps
                }
            }
        )


def update_global_stats(interaction_count, user_id):
    _global_stats_id = global_stats_collections.find_one({}, {"interaction_count": 1})
    if not _global_stats_id:
        global_stats_collections.insert_one(
            {
                "interaction_count": interaction_count,
                "user_list": [user_id],
                "user_count": 1
            }
        )
    else:
        global_stats = global_stats_collections.find_one(_global_stats_id)
        user_set = set(global_stats["user_list"])
        user_set.add(user_id)
        global_stats_collections.update_one(
            _global_stats_id,
            {
                "$set":
                {
                    "interaction_count": interaction_count,
                    "user_list": list(user_set),
                    "user_count": len(user_set)
                }
            }
        )
