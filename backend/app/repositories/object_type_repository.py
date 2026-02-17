from sqlalchemy import select
from app.models.object_type import ObjectTypeModel
from app.models.relation_signature import RelationSignatureModel
from backend.app.domain.ontology.relation_signature import RelationSignature
from .base import BaseRepository
from app.domain.ontology.object_type import ObjectType

class ObjectTypeRepository(BaseRepository):

    def __init__(self, session, signature_repo):
        super().__init__(session)
        self.signature_repo = signature_repo

    def save(self, domain_obj):

        model = ObjectTypeModel(
            name=domain_obj.getName(),
            parent_id=domain_obj.getDirectSuperType().getId()
            if domain_obj.getDirectSuperType() else None
        )

        self.session.add(model)
        self.session.flush()

        domain_obj._id = model.id
        return domain_obj

    def get_by_id(self, id):

        model = self.session.get(ObjectTypeModel, id)
        if not model:
            return None

        return ObjectType(
            id=model.id,
            name=model.name,
            parent=model.parent_id,
            repo=self
        )
    

    def get_children(self, parent_id):

        models = self.session.query(ObjectTypeModel)\
            .filter_by(parent_id=parent_id)\
            .all()

        return [
            ObjectType(
                id=m.id,
                name=m.name,
                repo=self
            )
            for m in models
        ]

    def delete(self, domain_obj):

        model = self.session.get(ObjectTypeModel, domain_obj.getId())
        if model:
            self.session.delete(model)

    def exists(self, id):

        return self.session.query(
            self.session.query(ObjectTypeModel)
            .filter_by(id=id)
            .exists()
        ).scalar()

    def get_associated_signatures(self, object_type_id):

        models = (
            self.session.query(RelationSignatureModel)
            .filter(
                (RelationSignatureModel.object_type1_id == object_type_id) |
                (RelationSignatureModel.object_type2_id == object_type_id)
            )
            .all()
        )

        signatures = []

        for m in models:

            # Load object types for domain object
            obj1 = ObjectType(
                id=m.object_type1_id,
                repo=self
            )

            obj2 = ObjectType(
                id=m.object_type2_id,
                repo=self
            )

            signatures.append(
                RelationSignature(
                    id=m.id,
                    name=m.name,
                    objectType1=obj1,
                    objectType2=obj2,
                    repo=self.signature_repo
                )
            )

        return signatures

    def get_associated_object_roles(self, object_type_id):

        # Placeholder for now, as object roles are not yet implemented
        return []