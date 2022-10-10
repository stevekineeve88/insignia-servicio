from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from modules.role.exceptions.role_create_exception import RoleCreateException
from modules.role.exceptions.role_delete_exception import RoleDeleteException
from modules.role.managers.role_manager import RoleManager
from tests.integration.setup.integration_setup import IntegrationSetup


class RoleManagerTest(IntegrationSetup):
    role_manager: RoleManager = None
    connection_manager: ConnectionManager = None

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.role_manager = cls.service_locator.get(RoleManager.__name__)
        cls.connection_manager = cls.service_locator.get(ConnectionManager.__name__)

    def test_create_creates_role(self):
        const = "ROLE"
        description = "Some description"
        role = self.role_manager.create(const, description)

        fetched_role = self.role_manager.search(
            search=const
        ).get_roles()[0]

        self.assertEqual(role.get_id(), fetched_role.get_id())
        self.assertEqual(role.get_const(), fetched_role.get_const())
        self.assertEqual(role.get_description(), fetched_role.get_description())

    def test_create_fails_on_duplicate_constant(self):
        const = "ROLE"
        description = "Some description"
        self.role_manager.create(const, description)
        with self.assertRaises(RoleCreateException):
            self.role_manager.create(const, description)
            self.fail("Did not fail on duplicate role constant")

    def test_delete_deletes_role(self):
        const = "ROLE"
        description = "Some description"
        role = self.role_manager.create(const, description)
        self.role_manager.delete(role.get_uuid())
        result = self.role_manager.search(search=const)
        self.assertEqual(0, len(result.get_roles()))

    def test_delete_fails_on_invalid_id(self):
        with self.assertRaises(RoleDeleteException):
            self.role_manager.delete("sdfsdf")
            self.fail("Did not fail on invalid role ID on delete")

    def test_search_searches_roles(self):
        searched_const = "ROLE_SECOND"
        searched_description = "Second description"
        self.role_manager.create("ROLE_FIRST", "Some description")
        self.role_manager.create(searched_const, searched_description)
        self.role_manager.create("ROLE_THIRD", "Some description")

        result = self.role_manager.search(search="second")
        roles = result.get_roles()

        self.assertEqual(1, len(roles))
        role = roles[0]

        self.assertEqual(searched_const, role.get_const())
        self.assertEqual(searched_description, role.get_description())

    def test_search_paginates_result(self):
        offset_const = "ROLE_SECOND"
        self.role_manager.create("ROLE_FIRST", "Some description")
        self.role_manager.create(offset_const, "Some description")
        self.role_manager.create("ROLE_THIRD", "Some description")

        result = self.role_manager.search(
            search="some description",
            limit=1,
            offset=1
        )

        self.assertEqual(3, result.get_total_count())
        roles = result.get_roles()
        self.assertEqual(1, len(roles))
        self.assertEqual(offset_const, roles[0].get_const())

    def tearDown(self) -> None:
        result = self.connection_manager.query(f"""
            DELETE FROM role WHERE 1=1
        """)
        if not result.get_status():
            raise Exception(f"Failed to teardown role test instance: {result.get_message()}")
