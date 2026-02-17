

from backend.app.domain.ontology.crelation import CRelation
from backend.app.models.crelation import CRelationModel
from backend.app.models.tuple import TupleModel
from backend.app.models.tuple_value import TupleValue
from backend.app.models.value import ValueModel
from backend.app.repositories.base import BaseRepository
from app.domain.ontology.tuple import Tuple
from app.domain.ontology.value import Value


class TupleRepository(BaseRepository):

    def __init__(self, session, value_repo, crelation_repo):
        super().__init__(session)
        self.value_repo = value_repo
        self.crelation_repo = crelation_repo

    def save(self, tuple_obj):

        if tuple_obj.getId() is None:

            model = TupleModel(
                name=tuple_obj.getName(),
                arity=tuple_obj.getArity()
            )

            self.session.add(model)
            self.session.flush()

            tuple_obj._Tuple__id = model.id

        else:

            model = self.session.get(
                TupleModel,
                tuple_obj.getId()
            )

            model.name = tuple_obj.getName()
            model.arity = tuple_obj.getArity()

        # ---- Sync ordered values ----
        self._sync_values(tuple_obj)

        return tuple_obj
    
    def _sync_values(self, tuple_obj):

        tuple_id = tuple_obj.getId()

        # Delete old mappings
        self.session.query(TupleValue)\
            .filter_by(tuple_id=tuple_id)\
            .delete()

        # Insert with correct position
        for position, value in enumerate(tuple_obj.getValues()):

            self.session.add(
                TupleValue(
                    tuple_id=tuple_id,
                    value_id=value.getId(),
                    position=position
                )
            )

    def get_by_id(self, id):

        model = self.session.get(TupleModel, id)
        if not model:
            return None

        values = self.get_values(id)

        return Tuple(
            id=model.id,
            name=model.name,
            arity=model.arity,
            values=values,
            repo=self
        )

    def get_values(self, tuple_id):

        mappings = (
            self.session.query(TupleValue)
            .filter_by(tuple_id=tuple_id)
            .order_by(TupleValue.position)
            .all()
        )

        values = []

        for m in mappings:

            value_model = self.session.get(
                ValueModel,
                m.value_id
            )

            values.append(
                Value(
                    id=value_model.id,
                    value=value_model.value,
                    repo=self.value_repo
                )
            )

        return values
    
    def get_all(self):

        models = self.session.query(TupleModel).all()

        return [
            self.get_by_id(m.id)
            for m in models
        ]

    def delete(self, tuple_obj):

        model = self.session.get(
            TupleModel,
            tuple_obj.getId()
        )

        if model:
            self.session.delete(model)

    def exists(self, id):

        return self.session.query(
            self.session.query(TupleModel)
            .filter_by(id=id)
            .exists()
        ).scalar()

    def get_crelations(self, tuple_id):

        models = (
            self.session.query(CRelationModel)
            .filter_by(tuple_id=tuple_id)
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

    def get_all(self):

        models = self.session.query(CRelationModel).all()

        return [
            self.get_by_id(m.id)
            for m in models
        ]

    def delete(self, crelation_obj):

        model = self.session.get(
            CRelationModel,
            crelation_obj.getId()
        )

        if model:
            self.session.delete(model)

    def exists(self, id):

        return self.session.query(
            self.session.query(CRelationModel)
            .filter_by(id=id)
            .exists()
        ).scalar()

    def get_by_constraint_type(self, constraint_type_id):

        model = (
            self.session.query(CRelationModel)
            .filter_by(type_id=constraint_type_id)
            .first()
        )

        if not model:
            return None

        return self.get_by_id(model.id)

