from backend.app.models.relation_type_quantity_role import RelationTypeQuantityRole
from .base import BaseRepository
from app.models.object_type import ObjectTypeModel
from app.models.quantity_role import QuantityRoleModel
from app.models.object_type_quantity_role import ObjectTypeQuantityRole
from app.models.relation_type import RelationTypeModel
from app.domain.ontology.quantity_role import QuantityRole
from app.domain.ontology.object_type import ObjectType
from app.domain.ontology.relation_type import RelationType
from app.domain.ontology.domain import Domain


class QuantityRoleRepository(BaseRepository):

    def __init__(self, session, domain_repo, object_type_repo, relation_type_repo):
        super().__init__(session)
        self.domain_repo = domain_repo
        self.object_type_repo = object_type_repo
        self.relation_type_repo = relation_type_repo


    def save(self, qrole_obj):

        if qrole_obj.getId() is None:

            model = QuantityRoleModel(
                name=qrole_obj.getName(),
                domain_id=(
                    qrole_obj.getDomain().getId()
                    if qrole_obj.getDomain() else None
                )
            )

            self.session.add(model)
            self.session.flush()

            qrole_obj._QuantityRole__id = model.id

        else:

            model = self.session.get(
                QuantityRoleModel,
                qrole_obj.getId()
            )

            model.name = qrole_obj.getName()
            model.domain_id = (
                qrole_obj.getDomain().getId()
                if qrole_obj.getDomain() else None
            )

        return qrole_obj

    def get_by_id(self, id):

        model = self.session.get(QuantityRoleModel, id)
        if not model:
            return None

        domain = None
        if model.domain_id:
            domain = Domain(
                id=model.domain_id,
                repo=self.domain_repo
            )

        return QuantityRole(
            id=model.id,
            name=model.name,
            domain=domain,
            repo=self
        )

    def get_all(self):

        models = self.session.query(QuantityRoleModel).all()

        return [
            QuantityRole(
                id=m.id,
                name=m.name,
                domain=Domain(id=m.domain_id) if m.domain_id else None,
                repo=self
            )
            for m in models
        ]

    def delete(self, qrole_obj):

        model = self.session.get(
            QuantityRoleModel,
            qrole_obj.getId()
        )

        if model:
            self.session.delete(model)

    def exists(self, id):

        return self.session.query(
            self.session.query(QuantityRoleModel)
            .filter_by(id=id)
            .exists()
        ).scalar()

    def get_structural_elements(self, qrole_id):

        object_models = (
            self.session.query(ObjectTypeModel)
            .join(ObjectTypeQuantityRole,
                  ObjectTypeModel.id ==
                  ObjectTypeQuantityRole.object_type_id)
            .filter(ObjectTypeQuantityRole.quantity_role_id == qrole_id)
            .all()
        )

        relation_models = (
            self.session.query(RelationTypeModel)
            .join(RelationTypeQuantityRole,
                  RelationTypeModel.id ==
                  RelationTypeQuantityRole.relation_type_id)
            .filter(RelationTypeQuantityRole.quantity_role_id == qrole_id)
            .all()
        )

        objects = [
            ObjectType(id=m.id, name=m.name, repo=self.object_type_repo)
            for m in object_models
        ]

        relations = [
            RelationType(id=m.id, name=m.name, repo=self.relation_type_repo)
            for m in relation_models
        ]

        return objects + relations

    def get_qrole_mappings(self, qrole_id):

        # Placeholder for now - implement after process type library

        return []
