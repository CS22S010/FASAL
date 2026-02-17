class CRelation:

    def __init__(self, id=None, name=None, type=None, tuples=None, repo=None):

        self.__repo = repo
        self.__id = id
        self.__name = name
        self.__type = type
        self.__tuples = tuples if tuples is not None else []

        # Load from DB if id provided
        if id is not None and repo is not None:

            row = repo.get_by_id(id)

            if row:
                self.__name = row.name

                if row.type_id is not None:
                    self.__type = repo.get_constraint_type(row.type_id)

                self.__tuples = repo.get_tuples(id)

    def getId(self):
        return self.__id
    
    def getName(self):
        return self.__name
    
    def setName(self, name):
        self.__name = name

    def getType(self):
        if self.__type is None and self.__repo is not None and self.__id is not None:
            row = self.__repo.get_by_id(self.__id)
            if row and row.type_id is not None:
                self.__type = self.__repo.get_constraint_type(row.type_id)
        return self.__type
    
    def setType(self, type):
        self.__type = type

    def getTuples(self):
        if not self.__tuples and self.__repo is not None and self.__id is not None:
            self.__tuples = self.__repo.get_tuples(self.__id)
        return self.__tuples
    
    def addTuple(self, tupleObj):
        self.__tuples.append(tupleObj)

    def removeTuple(self, tupleObj):
        self.__tuples = [
            t for t in self.__tuples
            if t != tupleObj
        ]
    
    def deleteTuples(self, tupleObjs):
        for tupleObj in tupleObjs:
            self.removeTuple(tupleObj)

    def contains(self, tupleObj):

        return tupleObj in self.__tuples
    
    
    def getAssociatedConstraintTypes(self):

        return self.__repo.get_constraint_types(self.__id)

    def checkState(self):

        inconsistencies = {}

        if self.__name is None or self.__name.strip() == "":
            inconsistencies["invalid_name"] = {
                "priority": "High"
            }

        if self.__type is None or not self.__type.existsInDB():
            inconsistencies["missing_constraint_type"] = {
                "priority": "High"
            }

        for tupleObj in self.__tuples:
            if not tupleObj.existsInDB():
                inconsistencies["missing_tuples"] = {
                    "priority": "High"
                }
                break

        return inconsistencies

    def __eq__(self, value):
        return isinstance(value, CRelation) and self.__id == value.getId()
    
    def __hash__(self):
        return hash(self.__id)