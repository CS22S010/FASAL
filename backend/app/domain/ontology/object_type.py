# domain/ontology/object_type.py
from structural_element_type import StructuralElementType

class ObjectType(StructuralElementType):

    def __init__(self, name=None, parent=None, id=None, repo=None):

        super().__init__(id=id, repo=repo)

        if id is not None and repo is not None:
            row = repo.get_by_id(id)

            if row:
                self.__name = row.name
                self._parent = row.parent_id
        else:
            self.__name = None
            self.__parent = None

            if parent is not None:
                self.__parent = parent

            if name is not None:
                self.__name = name




    
    def getId(self):
        return self.__id

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = name


    def checkState(self):

        inconsistencies = {}
        missing = []

        for superClass in self.getAllSuperTypes():

            if not self.__repo.exists(superClass.getId()):
                missing.append({
                    "object": superClass.getName(),
                    "priority": "High"
                })

        if missing:
            inconsistencies["missing_superclasses"] = missing

        return inconsistencies
    
    def getDirectSuperType(self):
        if self._parent is not None:
            return ObjectType(id=self._parent, repo=self.__repo)
        return None
    
    def getAllSuperTypes(self):

        result = []
        current = self.getDirectSuperType()

        while current is not None:
            result.append(current)
            current = current.getDirectSuperType()

        return result

    def getDirectSubTypes(self):

        rows = self.__repo.get_children(self.__id)

        return [
            ObjectType(id=row.id, repo=self.__repo)
            for row in rows
        ]

    def getAllSubTypes(self):

        result = []
        queue = self.getDirectSubTypes()

        while queue:

            current = queue.pop(0)
            result.append(current)

            children = current.getDirectSubTypes()
            queue.extend(children)

        return result
    
    def getAssociatedSignatures(self):

        return self.__repo.get_associated_signatures(self.__id)
    
    def getAssociatedObjectRoles(self):

        return self.__repo.get_associated_object_roles(self.__id)

    def addSuperType(self, parent):

        old_parent = self.__parent
        self.__parent = parent

    def deleteSuperType(self):

        #old_parent = self.__parent
        self.__parent = None

        #We are just removing the parent link, not the parent itself.
        '''
        oldParent = None
        if old_parent is not None:
            oldParent = ObjectType(id=old_parent, repo=self.__repo)


        dependencies = {}

        if oldParent is not None:

            subTypes = oldParent.getDirectSubTypes()
            if subTypes:
                dependencies["subTypes"] = subTypes

            objectRoles = oldParent.getAssociatedObjectRoles()
            if objectRoles:
                dependencies["objectRoles"] = objectRoles

            signatures = oldParent.getAssociatedSignatures()
            if signatures:
                dependencies["relationSignatures"] = signatures

        return dependencies
        '''
    
    def addSubType(self, child):

        old_parent = child.getDirectSuperType()
        child.__parent = self.getId()

    #Removed - child.deleteSuperType() should be called instead to remove the parent link.
    '''
    def deleteSubType(self, child):

        child.__parent = None
        self.__repo.save(child)
    '''
    
    def existsInDB(self):
        return self.__id is not None and self.__repo is not None and self.__repo.exists(self.__id)


    def __eq__(self, other):
        return isinstance(other, ObjectType) and self.__id == other.getId()

    def __hash__(self):
        return hash(self.__id)




