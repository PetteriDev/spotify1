from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import subprocess
import json

app = Flask(__name__)
CORS(app)


# Load the config from config.json
with open('config/config.json') as config_file:
    config_data = json.load(config_file)

# Connect to the MongoDB database
client = MongoClient(config_data['database'])
db = client['spotify']
collection = db['search_input']

@app.route('/search-artist', methods=['POST'])
def search_artist():
    artist_name = request.json['artistName']
    print(artist_name)

    # Update the search_input document with the artist name
    collection.update_one({}, {"$set": {"searchInput": artist_name}}, upsert=True)

    # Execute the data.js script
    subprocess.run(['node', 'data.js'])

    response = {
        'artistName': artist_name
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run()