import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
import pandas as pd

# MongoDB connection
mongo_client = MongoClient(
    f'mongodb+srv://mr4331:May0509619024@cluster0.xw2wecw.mongodb.net/?retryWrites=true&w=majority')
db = mongo_client['sample_restaurants']
collection = db['restaurants']
collection2 = db['users']


def search(search_term):
    try:
        # Perform a text search on the 'name' field and limit to the top 10 results
        search_results = collection.aggregate([
            {
                "$search": {
                    "index": "sample_restaurants",
                    "text": {
                        "query": search_term,
                        "path": ["name", "cuisine", "borough"],  # Specify the field to search in
                        "fuzzy": {
                            "maxEdits": 2,
                            "prefixLength": 0
                        }
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "name": 1,
                    "borough": 1,
                }
            },
            {
                "$limit": 20
            }
        ])
        results_list = list(search_results)
        return results_list

    except Exception as e:
        print(f"Error searching for restaurants: {e}")
        return jsonify({"error": "An error occurred while searching for restaurants"}), 500


def authenticate_user(email, password):
    user = collection2.find_one({'email': email, 'password': password})
    if user:
        return True
    else:
        return False
