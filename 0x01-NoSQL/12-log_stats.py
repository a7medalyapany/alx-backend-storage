#!/usr/bin/env python3
'''Log stats'''
from pymongo import MongoClient


def log_stats():
    '''Connect to MongoDB'''
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    '''Pipeline for aggregation'''
    pipeline = [
        {"$group": {"_id": "$method", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]

    '''Execute aggregation'''
    results = collection.aggregate(pipeline)

    '''Print total logs'''
    total_logs = sum(doc['count'] for doc in results)
    print(f"{total_logs} logs")

    '''Print methods count'''
    results = collection.aggregate([
        {"$group": {"_id": "$method", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ])
    for doc in results:
        print(f"\tmethod {doc['_id']}: {doc['count']}")

    '''Print status check count'''
    status_check_count = collection.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")


if __name__ == "__main__":
    log_stats()
