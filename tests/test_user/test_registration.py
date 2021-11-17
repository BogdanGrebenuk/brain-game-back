import uuid

from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from marshmallow import ValidationError

from app.exceptions.application import DomainException
from app.main import create_app
from app.user.auth.dto import CreateUserDto
from app.user.domain.entity import User


NON_EXISTENT_EMAIL = "test_email_non_existent@test.com"

EXISTENT_USER = User(
    id="test_id",
    first_name="kabab",
    last_name="kabab",
    patronymic="kabab",
    email="test_email_existent@test.com",
    password="Test@123",
    role="user"
)


class MockedUserMapper:

    async def find_one_by(self, **kwargs):
        email = kwargs.get("email")
        if email is None:
            raise ValueError("Expected 'email' argument")
        if email == EXISTENT_USER.email:
            return EXISTENT_USER
        return None


class RegistrationTests(AioHTTPTestCase):

    async def get_application(self):
        return create_app()

    async def setUpAsync(self):
        self.app.container.mappers.user_mapper.override(MockedUserMapper())

    async def tearDownAsync(self):
        self.app.container.mappers.user_mapper.reset_override()

    @unittest_run_loop
    async def test_successful_case(self):
        registrar = self.app.container.user.registrar()

        user = await registrar.register(
            CreateUserDto(
                id=str(uuid.uuid4()),
                email=NON_EXISTENT_EMAIL,
                password="test",
                last_name="test",
                first_name="test",
                patronymic="test",
                role="user"
            )
        )

        self.assertIsInstance(user, User)

    @unittest_run_loop
    async def test_existent_email_case(self):
        registrar = self.app.container.user.registrar()

        with self.assertRaises(DomainException):
            await registrar.register(
                CreateUserDto(
                    id=str(uuid.uuid4()),
                    email=EXISTENT_USER.email,
                    password="test",
                    last_name="test",
                    first_name="test",
                    patronymic="test",
                    role="user"
                )
            )

    @unittest_run_loop
    async def test_data_not_provided_case(self):
        registrar = self.app.container.user.registrar()

        with self.assertRaises(ValidationError) as cm:
            await registrar.register(
                CreateUserDto(
                    id=None,
                    email=None,
                    password=None,
                    last_name=None,
                    first_name=None,
                    patronymic=None,
                    role=None
                )
            )

        exception = cm.exception
        self.assertEqual(
            len(exception.messages), len(CreateUserDto.__dataclass_fields__)
        )
