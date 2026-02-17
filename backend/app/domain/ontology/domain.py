class Domain:

    def __init__(self, id=None, name=None, values=None, repo=None):

        self.__repo = repo
        self.__id = id
        self.__name = name
        self.__values = values if values is not None else []

        # Load from DB if id provided
        if id is not None and repo is not None:

            row = repo.get_by_id(id)

            if row:
                self.__name = row.name
                self.__values = repo.get_values(id)

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

    def addValueToDomain(self, value):

        if self.contains(value):
            raise Exception("Value already exists in domain")

        self.__values.append(value)

    def addValues(self, values):

        for value in values:
            self.addValueToDomain(value)


    def removeValue(self, value):

        if not self.contains(value):
            raise Exception("Value does not exist in domain")

        self.__values.remove(value)


    def deleteValues(self, values):
        for value in values:
            self.removeValue(value)

    def contains(self, value):

        return value in self.getValues()
    
    def getAssociatedQuantityRoles(self):

        return self.__repo.get_quantity_roles(self.__id)

    def getAssociatedConstraintSignatures(self):

        return self.__repo.get_constraint_signatures(self.__id)

    def checkState(self):

        inconsistencies = {}

        if self.__name is None or self.__name.strip() == "":
            inconsistencies["invalid_name"] = {
                "priority": "High"
            }

        if not self.__values or len(self.__values) == 0 or self.__repo.count_values(self.__id) == 0:
            inconsistencies["empty_domain"] = {
                "priority": "Medium"
            }

        return inconsistencies
    
    def __eq__(self, other):
        return isinstance(other, Domain) and self.__id == other.getId()

    def __hash__(self):
        return hash(self.__id)




