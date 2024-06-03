from pymongo import MongoClient
from bson.objectid import ObjectId

connection_string: str = 'mongodb://localhost:27017'

# Create a MongoClient instance with the annotated connection string
client: MongoClient = MongoClient(connection_string)
db = client['library']
books_collection = db['books']

sample_books = {
   '_id' : ObjectId(),
   "title" : "The Greate Gatsby"
}

result = books_collection.insert_one(sample_books)
print(result.inserted_id)

document = {"name": "John", "age": 30}
result = books_collection.insert_one(document)

# Retrieve the inserted ID
inserted_id = result.inserted_id
print("Inserted ID:", inserted_id)

# Retrieve the document using the inserted ID
inserted_document = books_collection.find_one({"_id": inserted_id})
print("Inserted Document:", inserted_document['name'],inserted_document['age'] )