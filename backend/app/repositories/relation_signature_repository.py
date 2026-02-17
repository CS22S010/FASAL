from app.models.relation_signature import RelationSignatureModel
from app.models.relation_type import RelationTypeModel
from app.domain.ontology.relation_signature import RelationSignature
from app.repositories.base import BaseRepository
from backend.app.domain.ontology.object_type import ObjectType
from backend.app.domain.ontology.relation_type import RelationType

class RelationSignatureRepository(BaseRepository):

    def __init__(self, session, object_type_repo, relation_type_repo):
        super().__init__(session)
        self.object_type_repo = object_type_repo
        self.relation_type_repo = relation_type_repo

    def save(self, signature_obj):

        if signature_obj.getId() is None:

            model = RelationSignatureModel(
                name=signature_obj.getName(),
                object_type1_id=(
                    signature_obj.getObjectType1().getId()
                    if signature_obj.getObjectType1() else None
                ),
                object_type2_id=(
                    signature_obj.getObjectType2().getId()
                    if signature_obj.getObjectType2() else None
                )
            )

            self.session.add(model)
            self.session.flush()

            signature_obj._RelationSignature__id = model.id

        else:

            model = self.session.get(
                RelationSignatureModel,
                signature_obj.getId()
            )

            model.name = signature_obj.getName()
            model.object_type1_id = (
                signature_obj.getObjectType1().getId()
                if signature_obj.getObjectType1() else None
            )
            model.object_type2_id = (
                signature_obj.getObjectType2().getId()
                if signature_obj.getObjectType2() else None
            )

        return signature_obj

    def get_by_id(self, id):

        model = self.session.get(RelationSignatureModel, id)
        if not model:
            return None

        obj1 = None
        if model.object_type1_id:
            obj1 = ObjectType(
                id=model.object_type1_id,
                repo=self.object_type_repo
            )

        obj2 = None
        if model.object_type2_id:
            obj2 = ObjectType(
                id=model.object_type2_id,
                repo=self.object_type_repo
            )

        return RelationSignature(
            id=model.id,
            name=model.name,
            objectType1=obj1,
            objectType2=obj2,
            repo=self
        )
    
    def get_all(self):

        models = self.session.query(RelationSignatureModel).all()

        signatures = []

        for m in models:

            signatures.append(
                RelationSignature(
                    id=m.id,
                    name=m.name,
                    objectType1=(
                        ObjectType(id=m.object_type1_id)
                        if m.object_type1_id else None
                    ),
                    objectType2=(
                        ObjectType(id=m.object_type2_id)
                        if m.object_type2_id else None
                    ),
                    repo=self
                )
            )

        return signatures
    
    def delete(self, signature_obj):

        model = self.session.get(
            RelationSignatureModel,
            signature_obj.getId()
        )

        if model:
            self.session.delete(model)

    def exists(self, id):

        return self.session.query(
            self.session.query(RelationSignatureModel)
            .filter_by(id=id)
            .exists()
        ).scalar()

    def get_relation_types_by_signature(self, signature_id):

        models = (
            self.session.query(RelationTypeModel)
            .filter_by(signature_id=signature_id)
            .all()
        )

        return [
            RelationType(
                id=m.id,
                name=m.name,
                repo=self.relation_type_repo
            )
            for m in models
        ]

