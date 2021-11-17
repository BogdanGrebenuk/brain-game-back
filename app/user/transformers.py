from app.user.domain.entity import User
from app.utils.transformer import Transformer


class UserTransformer(Transformer):

    async def transform(self, user: User):
        return {
            "id": user.id,
            "firstName": user.first_name,
            "lastName": user.last_name,
            "patronymic": user.patronymic,
            "email": user.email,
            "role": user.role
        }