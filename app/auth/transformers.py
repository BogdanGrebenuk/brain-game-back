from app.utils.transformer import Transformer


class AuthUserTransformer(Transformer):

    async def transform(self, user):
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "number": user.number
        }
