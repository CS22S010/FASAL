class ConstraintSignature:

    def __init__(self, id=None, name=None, domains=None, repo=None):

        self.__repo = repo
        self.__id = id
        self.__name = name
        self.__domains = domains

        # Load from DB if id provided
        if id is not None and repo is not None:

            row = repo.get_by_id(id)

            if row:
                self.__name = row.name
                self.__domains = repo.get_domains(id)  # must preserve order

    def getId(self):
        return self.__id
    
    def getName(self):
        return self.__name
    
    def setName(self, name):
        self.__name = name
    
    def getDomains(self):
        if self.__domains is None and self.__repo is not None and self.__id is not None:
            self.__domains = self.__repo.get_domains(self.__id)
        return self.__domains
    
    def addDomain(self, domain):

        self.__domains.append(domain)

    def removeDomain(self, domain):

        self.__domains = [
            d for d in self.__domains
            if d.getId() != domain.getId()
        ]

    def isCompatibleWithTuple(self, tupleObj):

        values = tupleObj.getValues()

        if len(values) != len(self.__domains):
            return False

        for value, domain in zip(values, self.__domains):

            if not domain.contains(value):
                return False

        return True

    def getAssociatedConstraintTypes(self):

        return self.__repo.get_constraint_types(self.__id)

    def checkState(self):

        inconsistencies = {}

        if self.__name is None or self.__name.strip() == "":
            inconsistencies["invalid_name"] = {
                "priority": "High"
            }

        if not self.__domains or len(self.__domains) == 0 or self.__repo.count_domains(self.__id) == 0:
            inconsistencies["empty_signature"] = {
                "priority": "High"
            }

        return inconsistencies

    def existsInDB(self):
        return self.__id is not None and self.__repo is not None and self.__repo.exists_by_id(self.__id)

    def __eq__(self, other):
        return isinstance(other, ConstraintSignature) and self.__id == other.getId()
    
    def __hash__(self):
        return hash(self.__id)