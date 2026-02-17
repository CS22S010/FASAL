from .structural_element_type import StructuralElementType
from .object_type import ObjectType
from .relation_signature import RelationSignature
from .relation_type import RelationType
from .quantity_role import QuantityRole
from .domain import Domain
from .value import Value
from .constraint_signature import ConstraintSignature
from .constraint_type import ConstraintType
from .tuple import Tuple
from .crelation import CRelation


class Ontology:

    def __init__(
        self,
        object_repo,
        relation_repo,
        signature_repo,
        quantity_role_repo,
        domain_repo,
        value_repo,
        constraint_signature_repo,
        constraint_type_repo,
        tuple_repo,
        crelation_repo
    ):
        self.object_repo = object_repo
        self.relation_repo = relation_repo
        self.signature_repo = signature_repo
        self.quantity_role_repo = quantity_role_repo
        self.domain_repo = domain_repo
        self.value_repo = value_repo
        self.constraint_signature_repo = constraint_signature_repo
        self.constraint_type_repo = constraint_type_repo
        self.tuple_repo = tuple_repo
        self.crelation_repo = crelation_repo

    def createObjectType(self, name: str, parentId: int | None):

        obj = ObjectType(name=name, parentId=parentId)

        self.object_repo.save(obj)

        return obj

    def deleteObjectType(self, objectType):

        dependencies = {}

        subTypes = objectType.getDirectSubTypes()
        if subTypes:
            dependencies["subTypes"] = subTypes

        roles = objectType.getAssociatedObjectRoles()
        if roles:
            dependencies["objectRoles"] = roles

        signatures = objectType.getAssociatedSignatures()
        if signatures:
            dependencies["relationSignatures"] = signatures

        self.object_repo.delete(objectType)

        return dependencies

    def getAllObjectTypes(self):

        rows = self.object_repo.get_all()

        return [
            ObjectType(id=row.id, name=row.name, parentId=row.parent_id)
            for row in rows
        ]

    def createRelationType(self, name: str, parentId: int | None, signature):

        rel = RelationType(name=name, parentId=parentId, signature=signature)

        self.relation_repo.save(rel)

        return rel

    def deleteRelationType(self, relationType):

        dependencies = {}

        roleRelations = relationType.getAssociatedRoleRelations()
        if roleRelations:
            dependencies["roleRelations"] = roleRelations

        quantityRoles = relationType.getQuantityRoles()
        if quantityRoles:
            dependencies["quantityRoles"] = quantityRoles

        self.relation_repo.delete(relationType)

        return dependencies

    def getAllRelationTypes(self):

        rows = self.relation_repo.get_all()

        return [
            RelationType(id=row.id, name=row.name, parentId=row.parent_id, signature=row.signature)
            for row in rows
        ]
    
    def createRelationSignature(self, name: str, objectType1, objectType2):

        signature = RelationSignature(
            name=name,
            objectType1=objectType1,
            objectType2=objectType2
        )

        self.signature_repo.save(signature)

        return signature
    
    def deleteRelationSignature(self, signature):

        dependencies = {}

        relationTypes = signature.getAssociatedRelationTypes()
        if relationTypes:
            dependencies["relationTypes"] = relationTypes

        self.signature_repo.delete(signature)

        return dependencies
    

    def getAllRelationSignatures(self):

        rows = self.signature_repo.get_all()

        return [
            RelationSignature(id=row.id, name=row.name, objectType1=row.object_type1, objectType2=row.object_type2)
            for row in rows
        ]
    
    def createDomain(self, name: str, values: list):

        domain = Domain(name=name, values=values)

        self.domain_repo.save(domain)

        return domain

    def deleteDomain(self, domain):

        dependencies = {}

        qRoles = domain.getAssociatedQuantityRoles()
        if qRoles:
            dependencies["quantityRoles"] = qRoles

        self.domain_repo.delete(domain)

        return dependencies
    
    def getAllDomains(self):

        rows = self.domain_repo.get_all()

        return [
            Domain(id=row.id, name=row.name, values=row.values)
            for row in rows
        ]
    
    def createValue(self, value: str):

        val = Value(name=value)

        self.value_repo.save(val)

        return val

    def deleteValue(self, value):

        dependencies = {}

        domains = value.getAssociatedDomains()
        if domains:
            dependencies["domains"] = domains

        self.value_repo.delete(value)

        return dependencies
    
    def getAllValues(self):

        rows = self.value_repo.get_all()

        return [
            Value(id=row.id, name=row.name)
            for row in rows
        ]
    
    def createConstraintSignature(self, name: str, domains: list):

        signature = ConstraintSignature(name=name, domains=domains)

        self.constraint_signature_repo.save(signature)

        return signature

    def deleteConstraintSignature(self, signature):

        dependencies = {}

        constraintTypes = signature.getAssociatedConstraintTypes()
        if constraintTypes:
            dependencies["constraintTypes"] = constraintTypes

        self.constraint_signature_repo.delete(signature)

        return dependencies

    def getAllConstraintSignatures(self):

        rows = self.constraint_signature_repo.get_all()

        return [
            ConstraintSignature(id=row.id, name=row.name, domains=row.domains)
            for row in rows
        ]
    
    def createConstraintType(self, name: str, signature, cRel):

        ct = ConstraintType(name=name, signature=signature, cRelation=cRel)

        self.constraint_type_repo.save(ct)

        return ct

    def deleteConstraintType(self, constraintType):

        dependencies = {}

        qRoleConstraints = constraintType.getAssociatedQuantityRoleConstraints()
        if qRoleConstraints:
            dependencies["qRoleConstraints"] = qRoleConstraints

        self.constraint_type_repo.delete(constraintType)

        return dependencies
    
    def getAllConstraintTypes(self):

        rows = self.constraint_type_repo.get_all()

        return [
            ConstraintType(id=row.id, name=row.name, signature=row.signature, cRelation=row.c_relation)
            for row in rows
        ]
    
    def createTuple(self, name: str, values: list, arity: int):

        tup = Tuple(name=name, values=values, arity=arity)

        self.tuple_repo.save(tup)

        return tup

    def deleteTuple(self, tupleObj):

        dependencies = {}

        cRels = tupleObj.getAssociatedCRelations()
        if cRels:
            dependencies["cRelations"] = cRels

        self.tuple_repo.delete(tupleObj)

        return dependencies
    
    def getAllTuples(self):

        rows = self.tuple_repo.get_all()

        return [
            Tuple(id=row.id, name=row.name, values=row.values, arity=row.arity)
            for row in rows
        ]

    def createCRelation(self, name: str, tupleObj, typeObj):

        cRel = CRelation(name=name, tuples=[tupleObj], type=typeObj)

        self.crelation_repo.save(cRel)

        return cRel

    def deleteCRelation(self, cRel):

        dependencies = {}

        constraintTypes = cRel.getAssociatedConstraintTypes()
        if constraintTypes:
            dependencies["constraintTypes"] = constraintTypes

        self.crelation_repo.delete(cRel)

        return dependencies
    
    def getAllCRelations(self):

        rows = self.crelation_repo.get_all()

        return [
            CRelation(id=row.id, name=row.name, tuples=row.tuples, type=row.type)
            for row in rows
        ]
    

def createQuantityRole(self, name: str, domain, seType):

    qRole = QuantityRole(
        name=name,
        domain=domain,
        owner=seType
    )

    self.quantity_role_repo.save(qRole)

    return qRole

def deleteQuantityRole(self, qRole):

    dependencies = {}


    mappings = qRole.getAssociatedQRoleMappings()
    if mappings:
        dependencies["qRoleMappings"] = mappings

    self.quantity_role_repo.delete(qRole)

    return dependencies

def getAllQuantityRoles(self):

    rows = self.quantity_role_repo.get_all()

    return [
        QuantityRole(id=row.id, name=row.name, domain=row.domain, owner=row.owner)
        for row in rows
    ]

def checkHierarchyConsistency(self):
    """
    Returns True if:
    - ObjectType hierarchy is acyclic
    - RelationType hierarchy is acyclic
    - No self-parent relationships
    """

    if not self.__checkObjectTypeHierarchy():
        return False

    if not self.__checkRelationTypeHierarchy():
        return False

    return True

def __checkObjectTypeHierarchy(self):

    allObjects = self.getAllObjectTypes()

    visited = set()
    recursionStack = set()

    def dfs(obj):

        if obj in recursionStack:
            return False  # cycle detected

        if obj in visited:
            return True

        visited.add(obj)
        recursionStack.add(obj)

        parent = obj.getDirectSuperType()

        if parent is not None:

            if parent == obj:
                return False  # self-parent

            if not dfs(parent):
                return False

        recursionStack.remove(obj)
        return True

    for obj in allObjects:
        if obj not in visited:
            if not dfs(obj):
                return False

    return True

def __checkRelationTypeHierarchy(self):

    allRelations = self.getAllRelationTypes()

    visited = set()
    recursionStack = set()

    def dfs(rel):

        if rel in recursionStack:
            return False  # cycle detected

        if rel in visited:
            return True

        visited.add(rel)
        recursionStack.add(rel)

        parent = rel.getDirectSuperType()

        if parent is not None:

            if parent == rel:
                return False  # self-parent

            if not dfs(parent):
                return False

        recursionStack.remove(rel)
        return True

    for rel in allRelations:
        if rel not in visited:
            if not dfs(rel):
                return False

    return True




