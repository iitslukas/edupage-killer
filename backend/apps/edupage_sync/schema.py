import strawberry


@strawberry.type
class Query:
    @strawberry.field
    def placeholder_edupage_sync(self) -> bool:
        return True


@strawberry.type
class Mutation:
    @strawberry.mutation
    def placeholder_edupage_sync_mutation(self) -> bool:
        return True
