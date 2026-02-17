from .structural_element_type import StructuralElementType
from .quantity_role import QuantityRole
from .crelation import CRelation
from .object_type import ObjectType

class RelationType(StructuralElementType):

    def __init__(self, id=None, name=None, parent=None, signature=None, repo=None):

        super().__init__(id=id, repo=repo)
        self.__name = name
        self.__parent = parent
        self.__signature = signature
        self.__properties = None

        # Load from DB if id provided
        if id is not None and repo is not None:

            row = repo.get_by_id(id)

            if row:
                self.__name = row.name

                self.__parent = row.parent_id

                # Load signature
                if row.signature_id is not None:
                    self.__signature = repo.get_signature(row.signature_id)

                self.__properties = repo.get_properties(id)

    def getId(self):
        return self.__id
    def getName(self):
        return self.__name
    def setName(self, name):
        self.__name = name
    def getSignature(self):
        if self.__signature is None and self.__repo is not None and self.__id is not None:
            row = self.__repo.get_by_id(self.__id)
            if row and row.signature_id is not None:
                self.__signature = self.__repo.get_signature(row.signature_id)
        return self.__signature
    def setSignature(self, signature):
        self.__signature = signature
    def deleteSignature(self):
        self.__signature = None
    def getDirectSuperType(self):
        if self.__parent is not None:
            return RelationType(id=self.__parent, repo=self.__repo)
        return None
    def getProperties(self):
        if self.__properties is None and self.__repo is not None and self.__id is not None:
            self.__properties = self.__repo.get_properties(self.__id)
        return self.__properties

    def addProperty(self, property):
        if not self.__signature.isCompatibleWithProperty(property):
            raise ValueError("Property is not compatible with relation signature.")
        self.__properties.add(property)
    
    '''
    def implyProperty(self, property):
        if FUNCTIONAL in self.getProperties() and SYMMETRIC in self.getProperties() and INVERSE_FUNCTIONAL not in self.getProperties():
            self.addProperty(INVERSE_FUNCTIONAL)
        if  FUNCTIONAL in self.getProperties() and INVERSE_FUNCTIONAL in self.getProperties() and UNIQUE not in self.getProperties():
            self.addProperty(UNIQUE)
    '''
            
    def hasProperty(self, property):
        return property in self.getProperties()

    def getAssociatedRoleRelations(self):
        return self.__repo.get_associated_role_relations(self.__id)

    def __eq__(self, other):
        return isinstance(other, ObjectType) and self.__id == other.getId()

    def __hash__(self):
        return hash(self.__id)
