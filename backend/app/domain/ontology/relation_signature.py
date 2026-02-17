# domain/ontology/relation_signature.py

from typing import Dict, List

from backend.app.models.object_type import ObjectType


class RelationSignature:

    def __init__(self, id=None, name=None, objectType1=None, objectType2=None, repo=None):

        self.__repo = repo
        self.__id = id
        self.__name = name
        self.__objectType1 = objectType1
        self.__objectType2 = objectType2

        # Load from DB if id provided
        if id is not None and repo is not None:

            row = repo.get_by_id(id)

            if row:
                self.__name = row.name

                if row.object_type1_id is not None:
                    self.__objectType1 = ObjectType(row.object_type1_id)

                if row.object_type2_id is not None:
                    self.__objectType2 = ObjectType(row.object_type2_id)

    def getId(self):
        return self.__id
    
    def getName(self):
        return self.__name
    
    def setName(self, name):
        self.__name = name
    
    def getObjectType1(self):
        if self.__objectType1 is None and self.__repo is not None and self.__id is not None:
            row = self.__repo.get_by_id(self.__id)
            if row and row.object_type1_id is not None:
                self.__objectType1 = ObjectType(row.object_type1_id)
        return self.__objectType1
    
    def setObjectType1(self, objectType1):
        self.__objectType1 = objectType1
    
    def getObjectType2(self):
        if self.__objectType2 is None and self.__repo is not None and self.__id is not None:
            row = self.__repo.get_by_id(self.__id)
            if row and row.object_type2_id is not None:
                self.__objectType2 = ObjectType(row.object_type2_id)
        return self.__objectType2
    
    def setObjectType2(self, objectType2):
        self.__objectType2 = objectType2

    def checkState(self):
        inconsistencies = {}
        if self.__objectType1 is not None and not self.__objectType1.existsInDB():
            inconsistencies.setdefault("missing_objectTypes", []).append({
                "objectType": self.__objectType1,
                "priority": "High"
            })
        if self.__objectType2 is not None and not self.__objectType2.existsInDB():
            inconsistencies.setdefault("missing_objectTypes", []).append({
                "objectType": self.__objectType2,
                "priority": "High"
            })
        return inconsistencies
    
    def getAssociatedRelationTypes(self):
        if self.__repo is not None and self.__id is not None:
            return self.__repo.get_relation_types_by_signature(self.__id)
        return []

    def replaceObjectType1(self, objectType: ObjectType) -> Dict[str, List]:
        dependancies = {}
        if self.getAssociatedRelationTypes():
            dependancies['relationTypes'] = self.getAssociatedRelationTypes()
        self.setObjectType1(objectType)
        return dependancies 
    
    def replaceObjectType2(self, objectType: ObjectType) -> Dict[str, List]:
        dependancies = {}
        if self.getAssociatedRelationTypes():
            dependancies['relationTypes'] = self.getAssociatedRelationTypes()
        self.setObjectType2(objectType)
        return dependancies
    
    def matches(self, objectType1: ObjectType, objectType2: ObjectType) -> bool:
        if self.__objectType1 is not None and self.__objectType2 is not None:
            return self.__objectType1 == objectType1 and self.__objectType2 == objectType2
        return False

    def isCompatibleWithProperty(self, property) -> bool:
        if property == "SYMMETRIC":
            if self.__objectType1 is not None and self.__objectType2 is not None:
                return self.__objectType1 == self.__objectType2
        if property == "TRANSITIVE":
            if self.__objectType1 is not None and self.__objectType2 is not None:
                return self.__objectType1 == self.__objectType2
        return True
    
    def __eq__(self, other):
        return isinstance(other, ObjectType) and self.__id == other.getId()

    def __hash__(self):
        return hash(self.__id)




