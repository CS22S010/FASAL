from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.models.relation_type import RelationTypeModel
from app.domain.ontology.relation_type import RelationType
from app.domain.ontology.quantity_role import QuantityRole
from app.domain.ontology.relation_signature import RelationSignature
from app.models.relation_signature import RelationSignatureModel
from app.models.relation_property import RelationPropertyModel
from app.models.relation_type_property import RelationTypeProperty
from app.models.relation_type_quantity_role import RelationTypeQuantityRole
from backend.app.domain.ontology.relation_property import RelationProperty
from backend.app.models.quantity_role import QuantityRoleModel
from .base import BaseRepository


class RelationTypeRepository(BaseRepository):

    def __init__(self, session, quantity_role_repo, signature_repo, relation_property_repo):
        super().__init__(session)
        self.quantity_role_repo = quantity_role_repo
        self.signature_repo = signature_repo
        self.relation_property_repo = relation_property_repo

    def save(self, relation_obj):

        if relation_obj.getId() is None:

            model = RelationTypeModel(
                name=relation_obj.getName(),
                parent_id=relation_obj.getDirectSuperType().getId()
                if relation_obj.getDirectSuperType() else None,
                signature_id=relation_obj.getSignature().getId()
                if relation_obj.getSignature() else None
            )

            self.session.add(model)
            self.session.flush()

            relation_obj._id = model.id

        else:

            model = self.session.get(
                RelationTypeModel,
                relation_obj.getId()
            )

            model.name = relation_obj.getName()
            model.parent_id = (
                relation_obj.getDirectSuperType().getId()
                if relation_obj.getDirectSuperType() else None
            )
            model.signature_id = (
                relation_obj.getSignature().getId()
                if relation_obj.getSignature() else None
            )

        # ---- Sync M:N mappings ----
        self._sync_properties(relation_obj)
        self._sync_quantity_roles(relation_obj)

        return relation_obj

    def _sync_properties(self, relation_obj):

        relation_id = relation_obj.getId()

        existing = {
            m.property_id
            for m in self.session.query(RelationTypeProperty)
            .filter_by(relation_type_id=relation_id)
            .all()
        }

        desired = {
            p.getId()
            for p in relation_obj.getProperties()
        }

        # Insert new
        for property_id in desired - existing:

            self.session.add(
                RelationTypeProperty(
                    relation_type_id=relation_id,
                    property_id=property_id
                )
            )

        # Delete removed
        for property_id in existing - desired:

            self.session.query(RelationTypeProperty)\
                .filter_by(
                    relation_type_id=relation_id,
                    property_id=property_id
                ).delete()

    def _sync_quantity_roles(self, relation_obj):

        relation_id = relation_obj.getId()

        existing = {
            m.quantity_role_id
            for m in self.session.query(RelationTypeQuantityRole)
            .filter_by(relation_type_id=relation_id)
            .all()
        }

        desired = {
            qr.getId()
            for qr in relation_obj.getQuantityRoles()
        }

        # Insert new
        for qrole_id in desired - existing:

            self.session.add(
                RelationTypeQuantityRole(
                    relation_type_id=relation_id,
                    quantity_role_id=qrole_id
                )
            )

        # Delete removed
        for qrole_id in existing - desired:

            self.session.query(RelationTypeQuantityRole)\
                .filter_by(
                    relation_type_id=relation_id,
                    quantity_role_id=qrole_id
                ).delete()

    def get_by_id(self, id):

        model = self.session.get(RelationTypeModel, id)
        if not model:
            return None

        signature = None
        if model.signature_id:
            signature_model = self.session.get(
                RelationSignatureModel,
                model.signature_id
            )

            signature = RelationSignature(
                id=signature_model.id,
                name=signature_model.name,
                repo=self.signature_repo
            )

        parent = None
        if model.parent_id:
            parent = RelationType(
                id=model.parent_id,
                repo=self
            )

        return RelationType(
            id=model.id,
            name=model.name,
            parent=parent,
            signature=signature,
            repo=self
        )

    def get_all(self):

        models = self.session.query(RelationTypeModel).all()

        return [
            RelationType(
                id=m.id,
                name=m.name,
                repo=self
            )
            for m in models
        ]

    def get_children(self, parent_id):

        models = (
            self.session.query(RelationTypeModel)
            .filter_by(parent_id=parent_id)
            .all()
        )

        return [
            RelationType(
                id=m.id,
                name=m.name,
                repo=self
            )
            for m in models
        ]

    def delete(self, relation_obj):

        model = self.session.get(
            RelationTypeModel,
            relation_obj.getId()
        )

        if model:
            self.session.delete(model)

    def exists(self, id):

        return self.session.query(
            self.session.query(RelationTypeModel)
            .filter_by(id=id)
            .exists()
        ).scalar()

    def get_properties(self, relation_id):

        models = (
            self.session.query(RelationPropertyModel)
            .join(RelationTypeProperty,
                  RelationPropertyModel.id ==
                  RelationTypeProperty.property_id)
            .filter(RelationTypeProperty.relation_type_id == relation_id)
            .all()
        )

        return [
            RelationProperty(
                id=m.id,
                name=m.name,
                repo=self.relation_property_repo
            )
            for m in models
        ]

    def add_property(self, relation_id, property_id):

        mapping = RelationTypeProperty(
            relation_type_id=relation_id,
            property_id=property_id
        )

        self.session.add(mapping)

    def remove_property(self, relation_id, property_id):

        self.session.query(RelationTypeProperty)\
            .filter_by(
                relation_type_id=relation_id,
                property_id=property_id
            ).delete()

    def get_quantity_roles(self, relation_id):

        models = (
            self.session.query(QuantityRoleModel)
            .join(RelationTypeQuantityRole,
                  QuantityRoleModel.id ==
                  RelationTypeQuantityRole.quantity_role_id)
            .filter(RelationTypeQuantityRole.relation_type_id == relation_id)
            .all()
        )

        return [
            QuantityRole(
                id=m.id,
                name=m.name,
                repo=self.quantity_role_repo
            )
            for m in models
        ]
    
    def get_associated_role_relations(self, relation_id):

        #placeholder since role relations are not yet implemented
        return []


