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
        with open(self.file_name, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
        return data

    def save_data(self):
        with open(self.file_name, "w") as file:
            json.dump(self.data, file, indent=4)

    def create_file(self):
        with open(self.file_name, "w") as file:
            file.write("[]")

    def create_record(self, id: int, name: str, directions: list, score: int):
        for record in self.data:
            if record["id"] == id:
                record["name"] = name
                record["directions"] = directions
                record["score"] = score
                break
        else:
            new_record = {
                "id": id,
                "name": name,
                "directions": directions,
                "score": score
            }
            self.data.append(new_record)

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
    handler.create_record(1, "LikimiaD LikimiaD", ["ITKN", "BISUP"], 1337)
    handler.save_data()
    record = handler.search_record(1)
    if record:
        print("ID:", record["id"])
        print("Name:", record["name"])
        print("Directions:", record["directions"])
        print("Score:", record["score"])
    else:
        print("Record with ID 1 not found")