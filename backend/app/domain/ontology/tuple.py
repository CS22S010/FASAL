class Tuple:

    def __init__(self, id=None, name=None, values=None, arity=None, repo=None):

        self.__repo = repo
        self.__id = id
        self.__name = name
        self.__values = values if values is not None else []
        self.__arity = arity

        # Load from DB if id provided
        if id is not None and repo is not None:

            row = repo.get_by_id(id)

            if row:
                self.__name = row.name
                self.__arity = row.arity
                self.__values = repo.get_values(id)  # must preserve order

    def getId(self):
        return self.__id
    
    def getName(self):
        return self.__name
    
    def setName(self, name):
        self.__name = name

    def getValues(self):
        if self.__values is None and self.__repo is not None and self.__id is not None:
            self.__values = self.__repo.get_values(self.__id)
        return self.__values
    
    def getArity(self):
        if self.__arity is None and self.__repo is not None and self.__id is not None:
            row = self.__repo.get_by_id(self.__id)
            if row:
                self.__arity = row.arity
        return self.__arity
    
    def setValues(self, values):
        self.__values = values
        self.__arity = len(values)

    def setArity(self, arity):
        self.__arity = arity

    def deleteArity(self):
        self.__arity = None

    def addValue(self, value):

        if self.__arity is not None and len(self.__values) >= self.__arity:
            raise Exception("Tuple arity exceeded")

        self.__values.append(value)

    def removeValue(self, value):

        self.__values = [
            v for v in self.__values
            if v != value
        ]

    def contains(self, value):

        return value in self.getValues()

    def isArityValid(self):

        if self.__arity is None:
            return True

        return len(self.__values) == self.__arity

    def getAssociatedCRelations(self):

        return self.__repo.get_crelations(self.__id)

    def checkState(self):

        inconsistencies = {}

        if self.__name is None or self.__name.strip() == "":
            inconsistencies["invalid_name"] = {
                "priority": "High"
            }

        if self.__arity is None:
            inconsistencies["missing_arity"] = {
                "priority": "High"
            }

        if not self.isArityValid():
            inconsistencies["arity_mismatch"] = {
                "priority": "High"
            }

        for value in self.__values:
            if value is None or (isinstance(value, str) and value.strip() == ""):
                inconsistencies["invalid_value"] = {
                    "priority": "High"
                }
            if self.__repo is not None and not self.__repo.value_exists(value):
                if "missing_values" not in inconsistencies:
                    inconsistencies["missing_values"] = []
                inconsistencies["missing_values"].append({
                    "value": value,
                    "priority": "High"
                })

        return inconsistencies

    def existsInDB(self):
        return self.__id is not None and self.__repo is not None and self.__repo.exists_by_id(self.__id)
    
    def __eq__(self, other):
        return isinstance(other, Tuple) and self.__id == other.getId()

    def __hash__(self):
        return hash(self.__id)

