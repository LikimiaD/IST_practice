import json
import os

FILE_NAME = "data.json"

class DataHandler:
    def __init__(self):
        self.file_name = FILE_NAME
        self.data = self.load_data()

    def load_data(self):
        if not os.path.exists(self.file_name):
            self.create_file()
        with open(self.file_name, "r", encoding='utf-8') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
        return data

    def save_data(self):
        with open(self.file_name, "w") as file:
            json.dump(self.data, file, indent=4, ensure_ascii=True)

    def create_file(self):
        with open(self.file_name, "w") as file:
            file.write("[]")

    def create_record(self, id: int, name: str = None, directions: list = None, score: int = None, quest: str = None, quest_status: int = None):
        for record in self.data:
            print("REWRITE")
            if record["id"] == id:
                if name is not None:
                    record["name"] = name
                if directions is not None:
                    record["directions"] = directions
                if score is not None:
                    record["score"] = score
                if quest is not None:
                    record["quest"] = quest
                if  quest_status is not None:
                    record["quest_status"] = quest_status
                self.save_data()
                break
        else:
            print("WRITE")
            new_record = {
                "id": id,
                "name": name,
                "directions": directions,
                "score": score,
                "quest": quest,
                "quest_status": quest_status,
            }
            self.data.append(new_record)
            self.save_data()

    def export_record(self, id):
        for record in self.data:
            if record["id"] == id:
                return record
        return None

    def search_record(self, id):
        for record in self.data:
            if record["id"] == id:
                return record
        return None

if __name__ == "__main__":
    handler = DataHandler()
    handler.create_record(1, "LikimiaD LikimiaD", ["ITKN", "АЛЛО"], 1337)
    record = handler.search_record(1)
    if record:
        print("ID:", record["id"])
        print("Name:", record["name"])
        print("Directions:", record["directions"])
        print("Score:", record["score"])
    else:
        print("Record with ID 1 not found")
    
    handler.create_record(1, name="New Name")
    handler.create_record(1, directions=["АХАХАХАХ АХАХАХА"])
    handler.create_record(1, score=999)