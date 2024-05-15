#!/usr/bin/env python3
'''Insert a document in Python'''


def insert_school(mongo_collection, **kwargs):
    """
    Insert a new document in a collection based on kwargs.

    Args:
        mongo_collection: PyMongo collection object.
        **kwargs: Keyword arguments representing the fields and values of the new document.

    Returns:
        The new _id of the inserted document.
    """
    new_document = kwargs
    result = mongo_collection.insert_one(new_document)
    return result.inserted_id
