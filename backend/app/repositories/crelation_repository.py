

from backend.app.domain.ontology.constraint_type import ConstraintType
from backend.app.domain.ontology.crelation import CRelation
from backend.app.domain.ontology.tuple import Tuple
from backend.app.models.crelation import CRelationModel
from backend.app.models.tuple import TupleModel
from backend.app.repositories.base import BaseRepository


class CRelationRepository(BaseRepository):

    def __init__(self, session, constraint_type_repo, tuple_repo):
        super().__init__(session)
        self.constraint_type_repo = constraint_type_repo
        self.tuple_repo = tuple_repo

    def save(self, crelation_obj):

        if crelation_obj.getId() is None:

            model = CRelationModel(
                name=crelation_obj.getName(),
                type_id=(
                    crelation_obj.getType().getId()
                    if crelation_obj.getType() else None
                ),
                tuple_id=(
                    crelation_obj.getTuple().getId()
                    if crelation_obj.getTuple() else None
                )
            )

            self.session.add(model)
            self.session.flush()

            crelation_obj._CRelation__id = model.id

        else:

            model = self.session.get(
                CRelationModel,
                crelation_obj.getId()
            )

            model.name = crelation_obj.getName()
            model.type_id = (
                crelation_obj.getType().getId()
                if crelation_obj.getType() else None
            )
            model.tuple_id = (
                crelation_obj.getTuple().getId()
                if crelation_obj.getTuple() else None
            )

        return crelation_obj

    def get_by_id(self, id):

        model = self.session.get(CRelationModel, id)
        if not model:
            return None

        constraint_type = None
        if model.type_id:
            constraint_type = ConstraintType(
                id=model.type_id,
                repo=self.constraint_type_repo
            )

        tuple_obj = None
        if model.tuple_id:
            tuple_model = self.session.get(
                TupleModel,
                model.tuple_id
            )

            tuple_obj = Tuple(
                id=tuple_model.id,
                name=tuple_model.name,
                arity=tuple_model.arity,
                repo=self.tuple_repo
            )

        return CRelation(
            id=model.id,
            name=model.name,
            type=constraint_type,
            tuple=tuple_obj,
            repo=self
        )

