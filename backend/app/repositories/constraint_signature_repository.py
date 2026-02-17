


from backend.app.domain.ontology.constraint_signature import ConstraintSignature
from backend.app.domain.ontology.constraint_type import ConstraintType
from backend.app.domain.ontology.domain import Domain
from backend.app.models.constraint_signature import ConstraintSignatureModel
from backend.app.models.constraint_signature_domain import ConstraintSignatureDomain
from backend.app.models.constraint_type import ConstraintTypeModel
from backend.app.models.domain import DomainModel
from backend.app.repositories.base import BaseRepository



class ConstraintSignatureRepository(BaseRepository):

    def __init__(self, session, domain_repo, constraint_type_repo):
        super().__init__(session)
        self.domain_repo = domain_repo
        self.constraint_type_repo = constraint_type_repo

    def save(self, signature_obj):

        if signature_obj.getId() is None:

            model = ConstraintSignatureModel(
                name=signature_obj.getName()
            )

            self.session.add(model)
            self.session.flush()

            signature_obj._ConstraintSignature__id = model.id

        else:

            model = self.session.get(
                ConstraintSignatureModel,
                signature_obj.getId()
            )

            model.name = signature_obj.getName()

        # ---- Sync ordered domains ----
        self._sync_domains(signature_obj)

        return signature_obj

    def _sync_domains(self, signature_obj):

        signature_id = signature_obj.getId()

        # Delete existing mappings
        self.session.query(ConstraintSignatureDomain)\
            .filter_by(constraint_signature_id=signature_id)\
            .delete()

        # Reinsert in correct order
        for position, domain in enumerate(signature_obj.getDomains()):

            self.session.add(
                ConstraintSignatureDomain(
                    constraint_signature_id=signature_id,
                    domain_id=domain.getId(),
                    position=position
                )
            )

    def get_by_id(self, id):

        model = self.session.get(ConstraintSignatureModel, id)
        if not model:
            return None

        domains = self.get_domains(id)

        return ConstraintSignature(
            id=model.id,
            name=model.name,
            domains=domains,
            repo=self
        )

    def get_domains(self, signature_id):

        mappings = (
            self.session.query(ConstraintSignatureDomain)
            .filter_by(constraint_signature_id=signature_id)
            .order_by(ConstraintSignatureDomain.position)
            .all()
        )

        domains = []

        for m in mappings:

            domain_model = self.session.get(
                DomainModel,
                m.domain_id
            )

            domains.append(
                Domain(
                    id=domain_model.id,
                    name=domain_model.name,
                    repo=self.domain_repo
                )
            )

        return domains

    def get_all(self):

        models = self.session.query(ConstraintSignatureModel).all()

        signatures = []

        for m in models:

            signatures.append(
                ConstraintSignature(
                    id=m.id,
                    name=m.name,
                    domains=self.get_domains(m.id),
                    repo=self
                )
            )

        return signatures

    def delete(self, signature_obj):

        model = self.session.get(
            ConstraintSignatureModel,
            signature_obj.getId()
        )

        if model:
            self.session.delete(model)

    def exists(self, id):

        return self.session.query(
            self.session.query(ConstraintSignatureModel)
            .filter_by(id=id)
            .exists()
        ).scalar()

    def get_constraint_types(self, signature_id):

        models = (
            self.session.query(ConstraintTypeModel)
            .filter_by(signature_id=signature_id)
            .all()
        )

        return [
            ConstraintType(
                id=m.id,
                name=m.name,
                repo=self.constraint_type_repo
            )
            for m in models
        ]

