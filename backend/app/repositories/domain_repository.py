

from backend.app.domain.ontology.constraint_signature import ConstraintSignature
from backend.app.domain.ontology.domain import Domain
from backend.app.domain.ontology.quantity_role import QuantityRole
from backend.app.domain.ontology.value import Value
from backend.app.models.constraint_signature import ConstraintSignatureModel
from backend.app.models.constraint_signature_domain import ConstraintSignatureDomain
from backend.app.models.domain import DomainModel
from backend.app.models.domain_value import DomainValue
from backend.app.models.quantity_role import QuantityRoleModel
from backend.app.models.value import ValueModel
from backend.app.repositories.base import BaseRepository


class DomainRepository(BaseRepository):

    def __init__(self, session, value_repo, quantity_role_repo, constraint_signature_repo):
        super().__init__(session)
        self.value_repo = value_repo
        self.quantity_role_repo = quantity_role_repo
        self.constraint_signature_repo = constraint_signature_repo


    def save(self, domain_obj):

        if domain_obj.getId() is None:

            model = DomainModel(
                name=domain_obj.getName()
            )

            self.session.add(model)
            self.session.flush()

            domain_obj._Domain__id = model.id

        else:

            model = self.session.get(
                DomainModel,
                domain_obj.getId()
            )

            model.name = domain_obj.getName()

        # ---- Sync M:N mappings ----
        self._sync_values(domain_obj)

        return domain_obj

    def _sync_values(self, domain_obj):

        domain_id = domain_obj.getId()

        existing = {
            m.value_id
            for m in self.session.query(DomainValue)
            .filter_by(domain_id=domain_id)
            .all()
        }

        desired = {
            v.getId()
            for v in domain_obj.getValues()
        }

        # Insert new mappings
        for value_id in desired - existing:

            self.session.add(
                DomainValue(
                    domain_id=domain_id,
                    value_id=value_id
                )
            )

        # Delete removed mappings
        for value_id in existing - desired:

            self.session.query(DomainValue)\
                .filter_by(
                    domain_id=domain_id,
                    value_id=value_id
                ).delete()

    def get_by_id(self, id):

        model = self.session.get(DomainModel, id)
        if not model:
            return None

        values = self.get_values(id)

        return Domain(
            id=model.id,
            name=model.name,
            values=values,
            repo=self
        )

    def get_all(self):

        models = self.session.query(DomainModel).all()

        domains = []

        for m in models:

            domains.append(
                Domain(
                    id=m.id,
                    name=m.name,
                    values=self.get_values(m.id),
                    repo=self
                )
            )

        return domains

    def delete(self, domain_obj):

        model = self.session.get(
            DomainModel,
            domain_obj.getId()
        )

        if model:
            self.session.delete(model)

    def exists(self, id):

        return self.session.query(
            self.session.query(DomainModel)
            .filter_by(id=id)
            .exists()
        ).scalar()

    def get_values(self, domain_id):

        models = (
            self.session.query(ValueModel)
            .join(DomainValue,
                  ValueModel.id ==
                  DomainValue.value_id)
            .filter(DomainValue.domain_id == domain_id)
            .all()
        )

        return [
            Value(
                id=m.id,
                value=m.value,
                repo=self.value_repo
            )
            for m in models
        ]
    
    def get_quantity_roles(self, domain_id):

        models = (
            self.session.query(QuantityRoleModel)
            .filter_by(domain_id=domain_id)
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

    def get_constraint_signatures(self, domain_id):

        mappings = (
            self.session.query(ConstraintSignatureDomain)
            .filter_by(domain_id=domain_id)
            .all()
        )

        signatures = []

        for m in mappings:

            signature_model = self.session.get(
                ConstraintSignatureModel,
                m.constraint_signature_id
            )

            signatures.append(
                ConstraintSignature(
                    id=signature_model.id,
                    name=signature_model.name,
                    repo=self.constraint_signature_repo
                )
            )

        return signatures

