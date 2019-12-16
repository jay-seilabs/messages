import graphene
from graphene_django import DjangoObjectType

from .models import Message


class MessageType(DjangoObjectType):
    class Meta:
        model = Message


class Query(graphene.ObjectType):
    messages = graphene.List(MessageType)

    def resolve_messages(self, info, **kwargs):
        return Message.objects.filter(user=info.context.user)


class CreateMessage(graphene.Mutation):
    message = graphene.Field(MessageType)

    class Arguments:
        text = graphene.String()

    def mutate(self, info, text):
        message = Message.objects.create(
            text=text,
            user=info.context.user,
        )
        return CreateMessage(message=message)


class Mutation(graphene.ObjectType):
    create_message = CreateMessage.Field()
