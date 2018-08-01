# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import current_app
from google.cloud import datastore


builtin_list = list


def init_app(app):
    pass


def get_client():
    return datastore.Client(current_app.config['PROJECT_ID'])


# [START from_datastore]
def from_datastore(entity):
    """Translates Datastore results into the format expected by the
    application.

    Datastore typically returns:
        [Entity{key: (kind, id), prop: val, ...}]

    This returns:
        {id: id, prop: val, ...}
    """
    if not entity:
        return None
    if isinstance(entity, builtin_list):
        entity = entity.pop()

    entity['id'] = entity.key.id
    return entity
# [END from_datastore]


# [START list]
def list(table, limit=100000, cursor=None):
    ds = get_client()
    if table == "Spolunteer":
        query = ds.query(kind=table, order=['firstname'])
    elif table == "Interest":
        query = ds.query(kind=table, order=['name'])
    query_iterator = query.fetch(limit=limit, start_cursor=cursor)
    page = next(query_iterator.pages)

    entities = builtin_list(map(from_datastore, page))
    next_cursor = (
        query_iterator.next_page_token.decode('utf-8')
        if query_iterator.next_page_token else None)

    return entities, next_cursor
# [END list]

# [START download]
def download_as_csv(table):
    ds = get_client()
    if table == "Spolunteer":
        query = ds.query(kind=table, order=['firstname'])
    elif table == "Interest":
        query = ds.query(kind=table, order=['name'])
    else:
        raise Exception("invalid table")
    query_iterator = query.fetch(limit=None, start_cursor=None)
    page = next(query_iterator.pages)

    entities = builtin_list(map(from_datastore, page))

    return entities

# [START list_by_operation]
def list_by_operation(table, operation):
    ds = get_client()
    if table == "Spolunteer":
        order = ['firstname']
    elif table == "Interest":
        order = ['name']
    if operation:
        query = ds.query(kind=table)
        query.add_filter('operation', '=', operation)
    else:
        query = ds.query(kind=table, order=order)

    query_iterator = query.fetch()
    page = next(query_iterator.pages)

    entities = builtin_list(map(from_datastore, page))

    return entities
# [END list_by_operation]

def role(email):
    ds = get_client()
    query = ds.query(kind='Greyshirt')
    query.add_filter('email', '=', email)
    results = query.fetch()
    for result in results:
        return result['role']
    return 'spolunteer'


def list_by_user(table, user_id, limit=1000000, cursor=None):
    ds = get_client()
    query = ds.query(
        kind=table,
        filters=[
            ('createdById', '=', user_id)
        ]
    )

    query_iterator = query.fetch(limit=limit, start_cursor=cursor)
    page = next(query_iterator.pages)

    entities = builtin_list(map(from_datastore, page))
    next_cursor = (
        query_iterator.next_page_token.decode('utf-8')
        if query_iterator.next_page_token else None)

    return entities, next_cursor

def read(table, id):
    ds = get_client()
    key = ds.key(table, int(id))
    results = ds.get(key)
    return from_datastore(results)


# [START update]
def update(table, data, id=None):
    ds = get_client()
    if id:
        key = ds.key(table, int(id))
    else:
        key = ds.key(table)

    entity = datastore.Entity(
        key=key,
        exclude_from_indexes=['description'])

    entity.update(data)
    ds.put(entity)
    return from_datastore(entity)


create = update
# [END update]


def delete(table, id):
    ds = get_client()
    key = ds.key(table, int(id))
    ds.delete(key)


def getInterest(id=None):
    ds = get_client()
    if id:
        key = ds.key('Interest', int(id))
    else:
        key = ds.key('Interest')

    key = ds.key('Interest')
    query = ds.query(kind='Interest')
    query_iterator = query.fetch(limit=1000000, start_cursor=None)
    page = next(query_iterator.pages)
    entities = builtin_list(map(from_datastore, page))
    #entities = ds.get(key)
    return entities

def createInterest(data):
    ds = get_client()
    key = ds.key('Interest')
    entity = datastore.Entity(key=key)
    entity.update(data)
    ds.put(entity)
    return from_datastore(entity)

def deleteInterest(id):
    ds = get_client()
    key = ds.key('Interest', int(id))
    ds.delete(key)

def delete_all(entries):
    ds = get_client()
    ds.delete_multi(entries)