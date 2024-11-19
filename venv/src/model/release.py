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
        requirement_to_implement,
        client,
        client_chosen,
    ):
        self.ID = id
        self.TITLE = title
        self.TOTAL_BUDGET = total_budget
        self.DESCRIPTION = description
        self.HOURS_TO_GENERATE = hours_to_generate
        self.CREATED_AT = created_at
        self.CREATED_BY_ID = created_by_id
        self.REQUIREMENT = requirement
        self.REQUIREMENT_TO_IMPLEMENT = requirement_to_implement
        self.CLIENT = client
        self.CLIENT_CHOSEN = client_chosen

    @classmethod
    def from_dict(cls, data):
        print("DATA",data)
        requirements = [
            {
                "ID": req.get("id"),
                "NAME": req.get("name"),
                "VALUE": req.get("budget"),
                "DESCRIPTION": req.get("description"),
                "CLIENT": req.get("client"),
                "WEIGHT": req.get("requirementImportance"),
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
            id=data.get("ID"),
            title=data.get("projectName"),
            total_budget=data.get("projectBudget"),
            description=data.get("projectDescription"),
            hours_to_generate=data.get("projectSelectTime"),
            created_at=data.get("CREATED_AT"),
            created_by_id=data.get("CREATED_BY_ID"),
            requirement=requirements,
            requirement_to_implement=data.get("REQUIREMENT_TO_IMPLEMENT", []),
            client=clients,
            client_chosen=data.get("CLIENT_CHOSEN", []),
        )

    def to_dict(self):
        return self.__dict__
