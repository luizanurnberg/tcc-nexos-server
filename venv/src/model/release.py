from datetime import datetime

class ReleaseModel:
    def __init__(
        self,
        id,
        title,
        total_budget,
        description,
        hours_to_generate,
        created_at,
        created_by_id,
        requirement,
        client,
        status,
    ):
        self.ID = id
        self.TITLE = title
        self.TOTAL_BUDGET = total_budget
        self.DESCRIPTION = description
        self.HOURS_TO_GENERATE = hours_to_generate
        self.CREATED_AT = created_at
        self.CREATED_BY_ID = created_by_id
        self.REQUIREMENT = requirement
        self.REQUIREMENT_TO_IMPLEMENT = None
        self.CLIENT = client
        self.CLIENT_CHOSEN = None
        self.STATUS = status

    @classmethod
    def from_dict(cls, data, instance):
        requirements = [
            {
                "ID": req.get("id"),
                "NAME": req.get("name"),
                "VALUE": req.get("budget"),
                "DESCRIPTION": req.get("description"),
                "CLIENT": req.get("client"),
                "WEIGHT": req.get("requirementImportance"),
                "DEPENDENTS": cls.filter_dependents(req, instance),
            }
            for req in data.get("requirements", [])
        ]

        clients = [
            {
                "ID": client.get("clientId"),
                "NAME": client.get("client"),
                "WEIGHT": client.get("clientImportance"),
            }
            for client in data.get("requirements", [])
        ]

        return cls(
            id=data.get("projectId"),
            title=data.get("projectName"),
            total_budget=data.get("projectBudget"),
            description=data.get("projectDescription"),
            hours_to_generate=data.get("projectSelectTime"),
            created_at=datetime.utcnow(),
            created_by_id=data.get("user"),
            requirement=requirements,
            client=clients,
            status=data.get("status"),
        )

    @staticmethod
    def filter_dependents(requirement, instance):
        # Filtra os requisitos dependentes com base no 'P' definido na instância do algoritmo.
        req_id = requirement.get("id")
        dependents = [
            {"ID": pair[1]} for pair in instance.get("P", []) if pair[0] == req_id
        ]
        return dependents

    def to_dict(self):
        return self.__dict__
