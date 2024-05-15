#!/usr/bin/env python3
'''Where can I learn Python'''


def schools_by_topic(mongo_collection, topic):
    """
    Return the list of schools having a specific topic.

    Args:
        mongo_collection: PyMongo collection object.
        topic (string): The topic searched.

    Returns:
        A list of schools with the specified topic.
    """
    schools = mongo_collection.find({"topics": topic})
    return list(schools)
