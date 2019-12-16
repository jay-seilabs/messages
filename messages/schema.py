import graphene
import graphql_jwt

import message.schema
import user.schema


class Query(user.schema.Query, message.schema.Query, graphene.ObjectType):
    pass


class Mutation(user.schema.Mutation, message.schema.Mutation, graphene.ObjectType,):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
