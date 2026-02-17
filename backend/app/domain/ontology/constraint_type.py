class ConstraintType:

    def __init__(self, id=None, name=None, signature=None, cRelation=None, repo=None):

        self.__repo = repo
        self.__id = id
        self.__name = name
        self.__signature = signature
        self.__cRelation = cRelation

        # Load from DB if id provided
        if id is not None and repo is not None:

            row = repo.get_by_id(id)

            if row:
                self.__name = row.name

                if row.signature_id is not None:
                    self.__signature = repo.get_signature(row.signature_id)

                if row.id is not None:
                    self.__cRelation = repo.get_crelation(row.id)

    def getId(self):
        return self.__id
    
    def getName(self):
        return self.__name
    
    def setName(self, name):
        self.__name = name

    def signature(self):
        if self.__signature is None and self.__repo is not None and self.__id is not None:
            row = self.__repo.get_by_id(self.__id)
            if row and row.signature_id is not None:
                self.__signature = self.__repo.get_signature(row.signature_id)
        return self.__signature
    
    def setSignature(self, signature):
        self.__signature = signature

    def deleteSignature(self):
        self.__signature = None

    def cRelation(self):
        if self.__cRelation is None and self.__repo is not None and self.__id is not None:
            row = self.__repo.get_by_id(self.__id)
            if row and row.id is not None:
                self.__cRelation = self.__repo.get_crelation(row.id)
        return self.__cRelation
    
    def setCRelation(self, cRelation):
        self.__cRelation = cRelation

    def removeCRelation(self):
        self.__cRelation = None

    def isTupleAllowed(self, tupleObj):

        if self.__signature is None:
            return False

        # Step 1 — Signature compatibility
        if not self.__signature.isCompatibleWithTuple(tupleObj):
            return False

        # Step 2 — If no CRelation defined, allow
        if self.__cRelation is None:
            return True

        # Step 3 — Check membership in CRelation
        return self.__cRelation.contains(tupleObj)
    
    def getAssociatedQRoleConstraints(self):

        return self.__repo.get_qrole_constraints(self.__id)

    def checkState(self):

        inconsistencies = {}

        if self.__name is None or self.__name.strip() == "":
            inconsistencies["invalid_name"] = {
                "priority": "High"
            }

        if self.__signature is None or not self.__signature.existsInDB():
            inconsistencies["missing_signature"] = {
                "priority": "High"
            }

        return inconsistencies

    def existsInDB(self):
        return self.__id is not None and self.__repo is not None and self.__repo.exists_by_id(self.__id)
    
    def __eq__(self, value):
        return isinstance(value, ConstraintType) and self.__id == value.getId()
    
    def __hash__(self):
        return hash(self.__id)


        