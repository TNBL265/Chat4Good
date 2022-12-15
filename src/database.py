import os
from pymongo import MongoClient
from urllib.parse import quote_plus
from assets.string import *

from telebot import formatting

MONGO_USERNAME = os.environ.get("MONGO_USERNAME", None)
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD", None)
MONGO_URL = os.environ.get("MONGO_URL", None)
if MONGO_USERNAME and MONGO_PASSWORD and MONGO_URL:
    CONNECTION_STRING = f"mongodb+srv://{quote_plus(MONGO_USERNAME)}:{quote_plus(MONGO_PASSWORD)}@{MONGO_URL}"
else:
    CONNECTION_STRING = "mongodb://127.0.0.1:27017/"


class StatsDatabase:
    def __init__(self):
        self.client = MongoClient(CONNECTION_STRING)
        self.db = self.client["C4G"]
        self.users_collections = self.db["users"]

    @staticmethod
    def reset_data():
        return {
            USER_ID: None,
            USERNAME: None,
            CITIZENSHIP_STATUS: None,
            GENDER: None,
            RACE: None,
            PCI: None,
            YEAR_OF_STUDY: None,
            PILLAR: None,
            MAX_STEPS: 0
        }

    def insert_user(self, user_data):
        user = self.users_collections.find_one({"user_id": user_data["user_id"]})
        if not user:
            self.users_collections.insert_one(user_data)
        elif user_data["max_steps"] >= user["max_steps"]:
            self.users_collections.update_one(
                user,
                {
                    "$set": user_data
                }
            )


class ScholarshipAndFinancialAidDatabase:
    # Need match csv order
    columns = {
            CITIZENSHIP_STATUS: "Singapore citizen; Singapore PR; Foreigner",
            GENDER: "Male; Female; Non-binary; Prefer not to disclose",
            RACE: "Chinese; Malay; Indian; Eurasian; Others; Prefer not to disclose",
            PCI: "< $2000/mth; < $2250/mth; >= $2250/mth",
            YEAR_OF_STUDY: "Freshmore; Sophomore; Junior; Senior",
            PILLAR: "EPD; ESD; ASD; CSD; DAI"
        }

    def __init__(self, safa_csv_filename):
        self.safa_csv_filename = safa_csv_filename
        self.data = None
        self.safa_options = None

    def populate_data(self):
        self.data = self.parse_csv(self.safa_csv_filename)

    def narrow_down_safa_options(self, criteria, text):
        if text == CANCEL:
            return
        if not self.safa_options:
            self.safa_options = self.data[criteria][text]
        else:
            self.safa_options = self.safa_options & self.data[criteria][text]

    def format_safa_output(self):
        msg = ""
        for i, safa_option in enumerate(self.safa_options):
            msg += f"{i + 1}. {formatting.hlink(safa_option[0], safa_option[1])}\n"
        return msg[:-1]

    def parse_csv(self, filename):
        local_db = ScholarshipAndFinancialAidDatabase.create_db(ScholarshipAndFinancialAidDatabase.columns)

        with open(filename, "r") as file:
            # Skip first line
            file.readline().strip("\n").split(",")
            for line in file:
                row = line.strip("\n").split(",")
                safa_name = row[0]
                safa_link = row[-1]
                for i, r in enumerate(row[1:-1]):
                    col_name = list(ScholarshipAndFinancialAidDatabase.columns)[i]
                    if not r:
                        # No/vague restrictions => include all
                        r = ScholarshipAndFinancialAidDatabase.columns[col_name]
                    for dr in r.split("; "):
                        local_db[col_name][dr].add((safa_name, safa_link))
        return local_db

    @staticmethod
    def create_db(data):
        """
        Use dictionary to store data in this format:
        {
          col1: {
            unique_val1: set(),
            unique_val2: set(),
          },
          col2: {}
        }
        where col[x] is the column header name
              unique_value[x] is the unique value in that column
        """
        local_db = {}
        for col_name, r in data.items():
            local_db[col_name] = {}
            for dr in r.split("; "):
                local_db[col_name][dr] = set()
        return local_db
