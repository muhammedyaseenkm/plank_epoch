from flask import Flask, jsonify
import redis

app = Flask(__name__)

# Connect to Redis
r = redis.Redis(host='localhost', port=6381, decode_responses=True)

# Route to set and get a key-value pair
@app.route("/")
def redis_example():
    # Set a key-value pair
    r.set('mykey', 'Hello, Redis!')

    # Get the value for a key
    value = r.get('mykey')

    return jsonify({"message": value})

if __name__ == "__main__":
    # Run the Flask app
    app.run(debug=True)
