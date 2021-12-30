import pymongo

class DB:

    def __init__(self):
        db_config = {
            "username": "Jasleen",
            "password": "C1PAWclhAIuys672",
            "database_name": "BizLog"
        }
        db_uri = "mongodb+srv://{username}:{password}@cluster0.0sti8.mongodb.net/{database_name}?retryWrites=true&w=majority".format_map(
            db_config)
        # client = pymongo.MongoClient(db_uri)
        client = pymongo.MongoClient(db_uri)
        print("DB Connection Created :)")

        # self.db = client.gw2021py1
        self.db = client['BizLog']  # get the reference of our database
        self.collections = self.db.list_collection_names()

    def insert(self, document):
        # Select the Collection in which you wish to work
        self.collection = self.db['BizLog']
        self.collection.insert_one(document)
        print("Document Inserted")

    def insert_operation(self, collection, document):
        # Select the Collection in which you wish to work
        self.collection = self.db[collection]
        self.collection.insert_one(document)
        print("Document Inserted")

    def fetch_collections(self):
        print("Fetching Collections from DB")
        for collection in self.collections:
            print(collection)

    def fetch_documents_in_collection(self, collection_name):
        print("Fetching Documents from", collection_name)
        self.collection = self.db[collection_name]
        documents = self.collection.find()
        # for document in documents:
        #     print(document)
        # print(type(document)) # DataType -> Dictionary
        return documents


    def validate_document_in_collection(self, collection_name, query):
        self.collection = self.db[collection_name]
        documents = self.collection.find(query)
        return self.db.collection.count()

    def delete_document(self, collection_name, query):
        self.collection = self.db[collection_name]
        result = self.collection.delete_one(query)
        return result

    def delete_document_from_collection(self, collection_name, roll_number):
        query = {"roll": roll_number}
        self.collection = self.db[collection_name]
        result = self.collection.delete_one(query)
        # self.collection.delete_many(query)
        if result.deleted_count > 0:
            print("Document Deleted: ", result.deleted_count)
        else:
            print("Document Could'nt be Found :(")

    def update_document_in_collection(self, collection_name, roll_number):

        document = {"name": "John Watson", "email": "john.watson@example.com", "age": 25}
        update_query = {"$set": document}
        query = {"roll": roll_number}

        self.collection = self.db[collection_name]
        self.collection.update_one(query, update_query)
        # self.collection.update_many()

        print("Record Updated")


def main():
    my_db = DB()


if __name__ == '__main__':
    main()
