class RelationProperty:

    def __init__(self, id=None, name=None, repo=None):

        self.__repo = repo
        self.__id = id
        self.__name = name

        # Load from DB if id provided
        if id is not None and repo is not None:

            row = repo.get_by_id(id)

            if row:
                self.__name = row.name

    def getId(self):
        return self.__id

    def getName(self):
        return self.__name
    
    def setName(self, name):
        self.__name = name

    def getAssociatedRelationTypes(self):

        rows = self.__repo.get_relation_types_by_property(self.__id)

        return rows
    
    def checkState(self):

        inconsistencies = {}

        if self.__name is None or self.__name.strip() == "":
            inconsistencies["invalid_name"] = {
                "priority": "High"
            }

        return inconsistencies

    def __eq__(self, other):
        return isinstance(other, RelationProperty) and self.__id == other.getId()

    def __hash__(self):
        return hash(self.__id)

    