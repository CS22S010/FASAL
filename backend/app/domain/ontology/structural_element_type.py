from abc import ABC, abstractmethod


class StructuralElementType(ABC):

    def __init__(self, id=None, repo=None):

        self._repo = repo
        self._id = id
        self.__quantity_roles = set()
    # ---- Interface methods ----

    def getId(self):
        return self._id

    def getQuantityRoles(self):
        return self._repo.get_quantity_roles(self._id)

    def addQuantityRole(self, quantityRole):

        if not self.isQRoleNameUnique(quantityRole.getName()):
            raise Exception("QuantityRole name must be unique within StructuralElementType")

        self._repo.link_quantity_role(self._id, quantityRole.getId())
    
    def isQRoleNameUnique(self, name):
        existing_roles = self.getQuantityRoles()
        for role in existing_roles:
            if role.getName() == name:
                return False
        return True
    
    @abstractmethod
    def getDirectSuperType(self):
        pass

    @abstractmethod
    def getAllSuperTypes(self):
        pass

    @abstractmethod
    def getDirectSubTypes(self):
        pass

    @abstractmethod
    def getAllSubTypes(self):
        pass

    @abstractmethod
    def checkState(self):
        pass

