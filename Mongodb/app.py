from pymongo import MongoClient
from datetime import datetime, timezone

connection_string_1 = "mongodb+srv://YASEEN:PASSWORD@exp1mongo.evkt5ln.mongodb.net/"
connection_string_2 = "mongodb://localhost:27020"

# Connect to MongoDB
client = MongoClient(connection_string_1)

# Access database
db = client['vector_db']

# Access collection
collection = db['vectors']

# Create a document with current UTC datetime
document = {
    'key': 'value',
    'timestamp': datetime.now(timezone.utc)  # Add current UTC datetime
}

# Insert document
result = collection.insert_one(document)
print(result.inserted_id)

# Query documents
for doc in collection.find():
    print(doc)

# Sample story documents
stories = [
    {
        'title': 'The Adventures of Alice',
        'author': 'Lewis Carroll',
        'content': 'Alice falls down a rabbit hole into a fantasy world.',
        'timestamp': datetime.now(timezone.utc)
    },
    {
        'title': 'The Great Gatsby',
        'author': 'F. Scott Fitzgerald',
        'content': 'The story of the mysterious Jay Gatsby and his love for Daisy Buchanan.',
        'timestamp': datetime.now(timezone.utc)
    },
    {
        'title': 'To Kill a Mockingbird',
        'author': 'Harper Lee',
        'content': 'A novel set in the American South, dealing with racial injustice and moral growth.',
        'timestamp': datetime.now(timezone.utc)
    }
]


# Insert the story document
for story in stories:
    result = collection.insert_one(story)
    print(result.inserted_id)


from pymongo import MongoClient, TEXT, ASCENDING, DESCENDING

# Access database
db = client['blogging_platform']

# Access collection
articles_collection = db['articles']

# Create indexes
articles_collection.create_index([('title', TEXT)], name='title_index')
articles_collection.create_index([('author', ASCENDING)], name='author_index')
articles_collection.create_index([('publication_date', DESCENDING)], name='publication_date_index')

# Retrieve and print indexes
indexes = articles_collection.list_indexes()

for index in indexes:
    print(index)

# Define query criteria
query = {'title': 'The Great Gatsby'}

# Retrieve specific item based on the query
result = articles_collection.find_one(query)

# Print the result
print(result)


# Get the index specifications
index_specs = articles_collection.index_information()

# Print the index specifications
for index_name, index_spec in index_specs.items():
    print(index_spec)

# Close the MongoDB connection
#client.close()

index_specs = [
    {'v': 2, 'key': [('_id', 1)]},
    {'v': 2, 'key': [('_fts', 'text'), ('_ftsx', 1)], 'default_language': 'english', 'language_override': 'language', 'textIndexVersion': 3},
    {'v': 2, 'key': [('author', 1)]},
    {'v': 2, 'key': [('publication_date', -1)]}
]

for index_spec in index_specs:
    print(index_spec)
# Sample aggregation pipeline
pipeline = [
    {"$group": {"_id": "$author", "count": {"$sum": 1}}}
]

# Perform aggregation
result = articles_collection.aggregate(pipeline)

# Print aggregation results
for doc in result: print(doc)