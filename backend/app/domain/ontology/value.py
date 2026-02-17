class Value:

    def __init__(self, id=None, value=None, repo=None):

        self.__repo = repo
        self.__id = id
        self.__value = value

        # Load from DB if id provided
        if id is not None and repo is not None:

            row = repo.get_by_id(id)

            if row:
                self.__value = row.value

    def getId(self):
        return self.__id
    
    def getValue(self):
        if self.__value is None and self.__repo is not None and self.__id is not None:
            row = self.__repo.get_by_id(self.__id)
            if row:
                self.__value = row.value
        return self.__value 
    
    def setValue(self, value):
        self.__value = value

    def getAssociatedDomains(self):

        return self.__repo.get_domains(self.__id)

    def getAssociatedTuples(self):

        return self.__repo.get_tuples(self.__id)

    def checkState(self):

        inconsistencies = {}

        if self.__value is None or str(self.__value).strip() == "":
            inconsistencies["invalid_value"] = {
                "priority": "High"
            }

        return inconsistencies

    def __eq__(self, other):
        return isinstance(other, Value) and self.__id == other.getId()
    
    def __hash__(self):
        return hash(self.__id)