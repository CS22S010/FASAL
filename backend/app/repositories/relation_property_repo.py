from app.domain.ontology.value import Value
from backend.app.domain.ontology.relation_property import RelationProperty
from backend.app.domain.ontology.relation_type import RelationType
from backend.app.models.relation_property import RelationPropertyModel
from backend.app.models.relation_type import RelationTypeModel
from backend.app.models.relation_type_property import RelationTypeProperty
from backend.app.repositories.base import BaseRepository

class RelationPropertyRepository(BaseRepository):

    def __init__(self, session, relation_type_repo=None):
        super().__init__(session)
        self.relation_type_repo = relation_type_repo

    def save(self, property_obj):

        if property_obj.getId() is None:

            model = RelationPropertyModel(
                name=property_obj.getName()
            )

            self.session.add(model)
            self.session.flush()

            property_obj._RelationProperty__id = model.id

        else:

            model = self.session.get(
                RelationPropertyModel,
                property_obj.getId()
            )

            model.name = property_obj.getName()

        return property_obj

    def get_by_id(self, id):

        model = self.session.get(RelationPropertyModel, id)
        if not model:
            return None

        return RelationProperty(
            id=model.id,
            name=model.name,
            repo=self
        )

    def get_all(self):

        models = self.session.query(RelationPropertyModel).all()

        return [
            RelationProperty(
                id=m.id,
                name=m.name,
                repo=self
            )
            for m in models
        ]

    def delete(self, property_obj):

        model = self.session.get(
            RelationPropertyModel,
            property_obj.getId()
        )

        if model:
            self.session.delete(model)

    def exists(self, id):

        return self.session.query(
            self.session.query(RelationPropertyModel)
            .filter_by(id=id)
            .exists()
        ).scalar()
    
    def get_relation_types_by_property(self, property_id):

        models = (
            self.session.query(RelationTypeModel)
            .join(RelationTypeProperty,
                  RelationTypeModel.id ==
                  RelationTypeProperty.relation_type_id)
            .filter(RelationTypeProperty.property_id == property_id)
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
