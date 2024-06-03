from pymongo import MongoClient
import tabulate

# I have created this by usning the docker-compose up   

# Replace the following with your MongoDB connection string
client = MongoClient("mongodb://localhost:27017/")

# Replace 'stock_data' with your database name
db = client.stock_data

# Replace 'prices' with your collection name
collection = db.prices

# Sample data
sample_data = [
    {
        "symbol": "AAPL",
        "date": "2024-05-20",
        "open": 172.50,
        "close": 173.00,
        "high": 174.00,
        "low": 171.50,
        "volume": 75000000
    },
    {
        "symbol": "GOOGL",
        "date": "2024-05-20",
        "open": 2850.00,
        "close": 2875.00,
        "high": 2880.00,
        "low": 2830.00,
        "volume": 1200000
    },
    {
        "symbol": "MSFT",
        "date": "2024-05-20",
        "open": 310.00,
        "close": 315.00,
        "high": 316.00,
        "low": 308.00,
        "volume": 40000000
    },
    {
        "symbol": "TSLA",
        "date": "2024-05-20",
        "open": 750.00,
        "close": 760.00,
        "high": 765.00,
        "low": 740.00,
        "volume": 20000000
    },
    {
        "symbol": "AMZN",
        "date": "2024-05-20",
        "open": 3300.00,
        "close": 3325.00,
        "high": 3340.00,
        "low": 3290.00,
        "volume": 3000000
    }
]

# Insert data into MongoDB collection
#collection.insert_many(sample_data)
#print("Sample data inserted successfully")

# Retrieve all documents in the collection
all_docs = collection.find()
headers = all_docs[0].keys() if all_docs else []

value_under_each_header = lambda doc: list(doc.values())
table_data = list(map(value_under_each_header, all_docs))
print(tabulate.tabulate(table_data, headers=headers, tablefmt="grid"))


# Find all records for a specific stock symbol
print('\n printing apple stock details')
aapl_docs = collection.find({"symbol": "AAPL"})

for doc in aapl_docs:
    headers = list(doc.keys())
    values = list(doc.values())
    table_data = [values]
    print(tabulate.tabulate(table_data, headers=headers, tablefmt="grid"))


# Calculate the average closing price for each stock symbol
avg_close_pipeline = [
    {
        "$group": {
            "_id": "$symbol",
            "averageClose": {"$avg": "$close"}
        }
    }
]


# Highest closing price of each stock
highest_close_pipeline = [
    {
        "$group": {
            "_id": "$symbol",
            "highestClose": {"$max": "$close"}
        }
    }
]

daily_range_pipeline = [
    {
        "$project": {
            "symbol": 1,
            "date": 1,
            "dailyRange": {"$subtract": ["$high", "$low"]}
        }
    }
]

total_volume_pipeline = [
    {
        "$group": {
            "_id": "$symbol",
            "totalVolume": {"$sum": "$volume"}
        }
    }
]

daily_avg_close_pipeline = [
    {
        "$group": {
            "_id": "$date",
            "averageClose": {"$avg": "$close"}
        }
    }
]

prices = collection

print('\n average closing price for each stock')
avg_close_result = prices.aggregate(total_volume_pipeline)
combined_output = []
for result in avg_close_result:
    table_data = list(result.values())
    combined_output.append(table_data)
headers = list(result.keys()) if combined_output else []

# Print the combined results using tabulate
print(tabulate.tabulate(combined_output, headers=headers, tablefmt="grid"))