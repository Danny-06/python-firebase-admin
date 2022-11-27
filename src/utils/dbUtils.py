def dbItemToSerializable(item, keepUID: bool = False):
  itemAsDict = item.__dict__['_data']

  if keepUID:
    itemAsDict['uid'] = item.uid

  return itemAsDict

def dbCollectionToSerializable(iterable, keepUID: bool = False):
  collection = []

  for item in iterable:
    itemAsDict = dbItemToSerializable(item, keepUID)
    collection += [itemAsDict]

  return collection
