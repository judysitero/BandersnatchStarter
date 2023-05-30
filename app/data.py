from os import getenv

from certifi import where
from dotenv import load_dotenv
from MonsterLab import Monster
from pandas import DataFrame
from pymongo import MongoClient


class Database:
    load_dotenv()
    database = MongoClient(getenv("DB_URL"), tlsCAFile=where())["Database"]

    def __init__(self, collection: str):
        self.collection = self.database[collection]

    def seed(self, amount):
        # Generate random monster data using MonsterLab
        monster = [Monster().to_dict() for _ in range(amount)]
        return self.collection.insert_many(monster)

    def reset(self):
        # Deleting all documents in the collection
        return self.collection.delete_many({})

    def count(self) -> int:
        # Getting the count of documents in the collection
        return self.collection.count_documents({})

    def dataframe(self) -> DataFrame:
        return DataFrame(self.collection.find({}, {"_id": False}))

    def html_table(self) -> str:
        return self.dataframe().to_html()


if __name__ == '__main__':
    db = Database("monster")
    db.seed(1000)
    # db.reset()
    print(db.count())  # To print count of documents
    print(db.dataframe())
    print(db.html_table())
