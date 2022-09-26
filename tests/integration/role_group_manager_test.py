from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from modules.role.exceptions.role_group_create_exception import RoleGroupCreateException
from modules.role.exceptions.role_group_delete_exception import RoleGroupDeleteException
from modules.role.managers.role_group_manager import RoleGroupManager
from tests.integration.setup.integration_setup import IntegrationSetup


class RoleGroupManagerTest(IntegrationSetup):
    role_group_manager: RoleGroupManager = None
    connection_manager: ConnectionManager = None

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.role_group_manager = cls.service_locator.get(RoleGroupManager.__name__)
        cls.connection_manager = cls.service_locator.get(ConnectionManager.__name__)

    def test_create_creates_role_group(self):
        const = "ROLE_GROUP"
        description = "Some description"
        role_group = self.role_group_manager.create(const, description)

        fetched_role_group = self.role_group_manager.search(
            search=const
        ).get_role_groups()[0]

        self.assertEqual(role_group.get_id(), fetched_role_group.get_id())
        self.assertEqual(role_group.get_uuid(), fetched_role_group.get_uuid())
        self.assertEqual(role_group.get_const(), fetched_role_group.get_const())
        self.assertEqual(role_group.get_description(), fetched_role_group.get_description())

    def test_create_fails_on_duplicate_constant(self):
        const = "ROLE_GROUP"
        description = "Some description"
        self.role_group_manager.create(const, description)
        with self.assertRaises(RoleGroupCreateException):
            self.role_group_manager.create(const, description)
            self.fail("Did not fail on duplicate role group constant")

    def test_delete_deletes_role_group(self):
        const = "ROLE_GROUP"
        description = "Some description"
        role_group = self.role_group_manager.create(const, description)
        self.role_group_manager.delete(role_group.get_id())
        result = self.role_group_manager.search(search=const)
        self.assertEqual(0, len(result.get_role_groups()))

    def test_delete_fails_on_invalid_id(self):
        with self.assertRaises(RoleGroupDeleteException):
            self.role_group_manager.delete(3)
            self.fail("Did not fail on invalid role group ID on delete")

    def test_search_searches_role_groups(self):
        searched_const = "ROLE_GROUP_SECOND"
        searched_description = "Second description"
        self.role_group_manager.create("ROLE_GROUP_FIRST", "Some description")
        self.role_group_manager.create(searched_const, searched_description)
        self.role_group_manager.create("ROLE_GROUP_THIRD", "Some description")

        result = self.role_group_manager.search(search="second")
        role_groups = result.get_role_groups()

        self.assertEqual(1, len(role_groups))
        role_group = role_groups[0]

        self.assertEqual(searched_const, role_group.get_const())
        self.assertEqual(searched_description, role_group.get_description())

    def test_search_paginates_result(self):
        offset_const = "ROLE_GROUP_SECOND"
        self.role_group_manager.create("ROLE_GROUP_FIRST", "Some description")
        self.role_group_manager.create(offset_const, "Some description")
        self.role_group_manager.create("ROLE_GROUP_THIRD", "Some description")

        result = self.role_group_manager.search(
            search="some description",
            limit=1,
            offset=1
        )

        self.assertEqual(3, result.get_total_count())
        role_groups = result.get_role_groups()
        self.assertEqual(1, len(role_groups))
        self.assertEqual(offset_const, role_groups[0].get_const())

    def tearDown(self) -> None:
        result = self.connection_manager.query(f"""
            DELETE FROM role_group WHERE 1=1
        """)
        if not result.get_status():
            raise Exception(f"Failed to teardown role group test instance: {result.get_message()}")
