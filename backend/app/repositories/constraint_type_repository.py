


from backend.app.domain.ontology.constraint_signature import ConstraintSignature
from backend.app.domain.ontology.constraint_type import ConstraintType
from backend.app.domain.ontology.crelation import CRelation
from backend.app.models.constraint_signature import ConstraintSignatureModel
from backend.app.models.constraint_type import ConstraintTypeModel
from backend.app.models.crelation import CRelationModel
from backend.app.repositories.base import BaseRepository


class ConstraintTypeRepository(BaseRepository):

    def __init__(self, session, domain_repo, constraint_signature_repo, crelation_repo):
        super().__init__(session)
        self.domain_repo = domain_repo
        self.constraint_signature_repo = constraint_signature_repo
        self.crelation_repo = crelation_repo

    def save(self, constraint_obj):

        if constraint_obj.getId() is None:

            model = ConstraintTypeModel(
                name=constraint_obj.getName(),
                signature_id=(
                    constraint_obj.getSignature().getId()
                    if constraint_obj.getSignature() else None
                )
            )

            self.session.add(model)
            self.session.flush()

            constraint_obj._ConstraintType__id = model.id

        else:

            model = self.session.get(
                ConstraintTypeModel,
                constraint_obj.getId()
            )

            model.name = constraint_obj.getName()
            model.signature_id = (
                constraint_obj.getSignature().getId()
                if constraint_obj.getSignature() else None
            )

        return constraint_obj

    def get_by_id(self, id):

        model = self.session.get(ConstraintTypeModel, id)
        if not model:
            return None

        # Load signature
        signature = None
        if model.signature_id:
            signature_model = self.session.get(
                ConstraintSignatureModel,
                model.signature_id
            )

            signature = ConstraintSignature(
                id=signature_model.id,
                name=signature_model.name,
                repo=self.constraint_signature_repo
            )

        # Load CRelation (if exists)
        crelation_model = (
            self.session.query(CRelationModel)
            .filter_by(type_id=id)
            .first()
        )

        crelation = None
        if crelation_model:
            crelation = CRelation(
                id=crelation_model.id,
                name=crelation_model.name,
                repo=self.crelation_repo
            )

        return ConstraintType(
            id=model.id,
            name=model.name,
            signature=signature,
            cRelation=crelation,
            repo=self
        )

    def get_all(self):

        models = self.session.query(ConstraintTypeModel).all()

        return [
            self.get_by_id(m.id)
            for m in models
        ]

    def delete(self, constraint_obj):

        model = self.session.get(
            ConstraintTypeModel,
            constraint_obj.getId()
        )

        if model:
            self.session.delete(model)

    def exists(self, id):

        return self.session.query(
            self.session.query(ConstraintTypeModel)
            .filter_by(id=id)
            .exists()
        ).scalar()

    def get_crelation(self, constraint_type_id):

        model = (
            self.session.query(CRelationModel)
            .filter_by(type_id=constraint_type_id)
            .first()
        )

        if not model:
            return None

        return CRelation(
            id=model.id,
            name=model.name,
            repo=self.crelation_repo
        )
    
    def get_crelations(self, constraint_type_id):

        models = (
            self.session.query(CRelationModel)
            .filter_by(type_id=constraint_type_id)
            .all()
        )

        return [
            CRelation(
                id=m.id,
                name=m.name,
                repo=self.crelation_repo
            )
            for m in models
        ]

    def get_qrole_constraints(self, constraint_type_id):

        #TBD after ProcessTypeLibrary is implemented
        return []

