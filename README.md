# Messages
The purpose of this is to learn how to use GraphQL by building a messages API

# Setup
This makes use of Django + Postgres + Docker for the backend
To run this, first install Docker
To get this running on localhost with the correct DB migrations, run
```
docker-compose build
docker-compose up -d
docker-compose exec web python manage.py migrate
```
If everything went well, you should be able to navigate to
`http://localhost:8000/graphql/` to use GraphiQL

Under the hood, this is running Postgres on a docker container, and the
rest of the code (with the installed dependencies) on another docker 
container. 

# Functionality
To use this, you will need to issue POST requests to 
```
http://localhost:8000/graphql/
```
I would also recommend using Insomnia (https://insomnia.rest/graphql/)
or some other GraphQL client. Insomnia allows authentication tokens to be
sent via the header.

Firstly, we can create a new user. This user will be created with an
email, username, and password. This makes use of Django default models
to encrypt and store the password. 

```
mutation {
  createUser(username: "test", email:"test", password:"test") {
    user {
      id
      email
    }
  }
} 
```

Next, we can login with user credentials. This requires creating a
new token as shown below. 
```
mutation {
  tokenAuth(username:"test", password:"test") {
    token
  }
}
```
(Obviously) if incorrect credentials are passed in, then this raise
an error. 
This makes use of https://github.com/flavors/django-graphql-jwt
Once the token is created, it will be used for all logic requiring a
user to be authenticated. 

Next, we can create a message as a user. Since we only want the message
to be associated with the authenticated user, a auth token is required in
the header. 

This follows the format
`Authorization: JWT {token}`

For example, it will be something like
```
Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJleHAiOjE1NzY0NTQ5MTIsIm9yaWdJYXQiOjE1NzY0NTQ2MTJ9.a8KDVcDJE2R80CMRdbpoEhCtjZP2RD3pC3SlPKs-D_s
```

Once the auth token is added to the header, creating a message is as follows
```
mutation {
  createMessage(text: "hello world user 1") {
    message {
      id
      text
      user {
        username
        id
        email
      }
    }
  }
}
```

Lastly, we can retreive all messages posted by the authenticated user. First,
add the token as shown above. Then, the following query
```
query {
  messages {
    id
    text
    createdAt
  }
}
```
will return the messages posted by the authenticated user. This means that
it will not return all messages -- only the ones posted by that user

Note that the messages query currently doesn't allow for user A to see all
messages from user B. This is logic that can be added in the future. 
