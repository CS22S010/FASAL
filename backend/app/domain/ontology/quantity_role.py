from .structural_element_type import StructuralElementType

class QuantityRole:

    def __init__(self, id=None, name=None, domain=None, owner=None, repo=None):

        self.__repo = repo
        self.__id = id
        self.__name = name
        self.__domain = domain
        self.__owner = owner

        # Load from DB if id provided
        if id is not None and repo is not None:

            row = repo.get_by_id(id)

            if row:
                self.__name = row.name

                if row.domain_id is not None:
                    self.__domain = repo.get_domain(row.domain_id)
                if row.owner_id is not None:
                    self.__owner = StructuralElementType(row.owner_id)

    def getId(self):
        return self.__id
    
    def getName(self):
        return self.__name
    
    def getOwner(self):
        if self.__owner is None and self.__repo is not None and self.__id is not None:
            row = self.__repo.get_by_id(self.__id)
            if row and row.owner_id is not None:
                self.__owner = StructuralElementType(row.owner_id)
        return self.__owner
    
    def setName(self, name):
        self.__name = name

    def getDomain(self):
        if self.__domain is None and self.__repo is not None and self.__id is not None:
            row = self.__repo.get_by_id(self.__id)
            if row and row.domain_id is not None:
                self.__domain = self.__repo.get_domain(row.domain_id)
        return self.__domain
    
    def setDomain(self, domain):
        self.__domain = domain
    
    def getAssociatedStructuralElements(self):

        rows = self.__repo.get_structural_elements(self.__id)

        return rows
    
    def getAssociatedQRoleMappings(self):

        return self.__repo.get_qrole_mappings(self.__id)

    def checkState(self):

        inconsistencies = {}

        if self.__name is None or self.__name.strip() == "":
            inconsistencies["invalid_name"] = {
                "priority": "High"
            }

        if self.__domain is None or not self.__domain.existsInDB():
            inconsistencies["missing_domain"] = {
                "priority": "High"
            }

        return inconsistencies

    def __eq__(self, other):
        return isinstance(other, QuantityRole) and self.__id == other.getId()

    def __hash__(self):
        return hash(self.__id)
    