from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from modules.action.exceptions.action_create_exception import ActionCreateException
from modules.action.exceptions.action_delete_exception import ActionDeleteException
from modules.action.managers.action_manager import ActionManager
from tests.integration.setup.integration_setup import IntegrationSetup


class ActionManagerTest(IntegrationSetup):
    action_manager: ActionManager = None
    connection_manager: ConnectionManager = None

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.action_manager = cls.service_locator.get(ActionManager.__name__)
        cls.connection_manager = cls.service_locator.get(ConnectionManager.__name__)

    def test_create_creates_action(self):
        const = "ENTITY:ACTION"
        description = "Some description"
        action = self.action_manager.create(const, description)

        fetched_action = self.action_manager.search(
            search=const
        ).get_actions()[0]

        self.assertEqual(action.get_id(), fetched_action.get_id())
        self.assertEqual(action.get_const(), fetched_action.get_const())
        self.assertEqual(action.get_description(), fetched_action.get_description())

    def test_create_fails_on_duplicate_constant(self):
        const = "ENTITY:ACTION"
        description = "Some description"
        self.action_manager.create(const, description)
        with self.assertRaises(ActionCreateException):
            self.action_manager.create(const, description)
            self.fail("Did not fail on duplicate action constant")

    def test_delete_deletes_action(self):
        const = "ENTITY:ACTION"
        description = "Some description"
        action = self.action_manager.create(const, description)
        self.action_manager.delete(action.get_id())
        result = self.action_manager.search(search=const)
        self.assertEqual(0, len(result.get_actions()))

    def test_delete_fails_on_invalid_id(self):
        with self.assertRaises(ActionDeleteException):
            self.action_manager.delete(3)
            self.fail("Did not fail on invalid action ID on delete")

    def test_search_searches_actions(self):
        searched_const = "ENTITY:SECOND"
        searched_description = "Second description"
        self.action_manager.create("ENTITY:FIRST", "Some description")
        self.action_manager.create(searched_const, searched_description)
        self.action_manager.create("ENTITY:THIRD", "Some description")

        result = self.action_manager.search(search="second")
        actions = result.get_actions()

        self.assertEqual(1, len(actions))
        action = actions[0]

        self.assertEqual(searched_const, action.get_const())
        self.assertEqual(searched_description, action.get_description())

    def test_search_paginates_result(self):
        offset_const = "ENTITY:SECOND"
        self.action_manager.create("ENTITY:FIRST", "Some description")
        self.action_manager.create(offset_const, "Some description")
        self.action_manager.create("ENTITY:THIRD", "Some description")

        result = self.action_manager.search(
            search="some description",
            limit=1,
            offset=1
        )

        self.assertEqual(3, result.get_total_count())
        actions = result.get_actions()
        self.assertEqual(1, len(actions))
        self.assertEqual(offset_const, actions[0].get_const())

    def tearDown(self) -> None:
        result = self.connection_manager.query(f"""
            DELETE FROM action WHERE 1=1
        """)
        if not result.get_status():
            raise Exception(f"Failed to teardown action test instance: {result.get_message()}")
