


from backend.app.domain.ontology.domain import Domain
from backend.app.models.domain import DomainModel
from backend.app.models.domain_value import DomainValue
from backend.app.models.tuple import TupleModel
from backend.app.models.tuple_value import TupleValue
from backend.app.models.value import ValueModel
from backend.app.repositories.base import BaseRepository
from app.domain.ontology.value import Value
from app.domain.ontology.tuple import Tuple



class ValueRepository(BaseRepository):

    def __init__(self, session, domain_repo=None, tuple_repo=None):
        super().__init__(session)
        self.domain_repo = domain_repo
        self.tuple_repo = tuple_repo

    def save(self, value_obj):

        if value_obj.getId() is None:

            model = ValueModel(
                value=value_obj.getValue()
            )

            self.session.add(model)
            self.session.flush()

            value_obj._Value__id = model.id

        else:

            model = self.session.get(
                ValueModel,
                value_obj.getId()
            )

            model.value = value_obj.getValue()

        return value_obj
    
    def get_by_id(self, id):

        model = self.session.get(ValueModel, id)
        if not model:
            return None

        return Value(
            id=model.id,
            value=model.value,
            repo=self
        )

    def get_all(self):

        models = self.session.query(ValueModel).all()

        return [
            Value(
                id=m.id,
                value=m.value,
                repo=self
            )
            for m in models
        ]

    def delete(self, value_obj):

        model = self.session.get(
            ValueModel,
            value_obj.getId()
        )

        if model:
            self.session.delete(model)

    def exists(self, id):

        return self.session.query(
            self.session.query(ValueModel)
            .filter_by(id=id)
            .exists()
        ).scalar()

    def get_domains(self, value_id):

        models = (
            self.session.query(DomainModel)
            .join(DomainValue,
                  DomainModel.id ==
                  DomainValue.domain_id)
            .filter(DomainValue.value_id == value_id)
            .all()
        )

        return [
            Domain(
                id=m.id,
                name=m.name,
                repo=self.domain_repo
            )
            for m in models
        ]

    def get_tuples(self, value_id):

        mappings = (
            self.session.query(TupleValue)
            .filter_by(value_id=value_id)
            .order_by(TupleValue.position)
            .all()
        )

        tuples = []

        for m in mappings:

            tuple_model = self.session.get(
                TupleModel,
                m.tuple_id
            )

            tuples.append(
                Tuple(
                    id=tuple_model.id,
                    name=tuple_model.name,
                    arity=tuple_model.arity,
                    repo=self.tuple_repo
                )
            )

        return tuples

