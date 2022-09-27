from typing import Dict
from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from modules.action.managers.action_manager import ActionManager
from modules.policy.exceptions.role_group_policy_add_action_exception import RoleGroupPolicyAddActionException
from modules.policy.exceptions.role_group_policy_add_role_exception import RoleGroupPolicyAddRoleException
from modules.policy.exceptions.role_group_policy_delete_action_exception import RoleGroupPolicyDeleteActionException
from modules.policy.exceptions.role_group_policy_delete_role_exception import RoleGroupPolicyDeleteRoleException
from modules.policy.exceptions.role_group_policy_fetch_exception import RoleGroupPolicyFetchException
from modules.policy.managers.role_group_policy_manager import RoleGroupPolicyManager
from modules.policy.objects.role_policy import RolePolicy
from modules.role.managers.role_group_manager import RoleGroupManager
from modules.role.managers.role_manager import RoleManager
from tests.integration.setup.integration_setup import IntegrationSetup


class RoleGroupPolicyManagerTest(IntegrationSetup):
    role_group_policy_manager: RoleGroupPolicyManager = None
    role_group_manager: RoleGroupManager = None
    role_manager: RoleManager = None
    action_manager: ActionManager = None
    connection_manager: ConnectionManager = None

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.role_group_policy_manager = cls.service_locator.get(RoleGroupPolicyManager.__name__)
        cls.role_group_manager = cls.service_locator.get(RoleGroupManager.__name__)
        cls.role_manager = cls.service_locator.get(RoleManager.__name__)
        cls.action_manager = cls.service_locator.get(ActionManager.__name__)
        cls.connection_manager = cls.service_locator.get(ConnectionManager.__name__)

    def setUp(self) -> None:
        self.action = self.action_manager.create("USER:CREATE", "User creation action permission")
        self.role = self.role_manager.create("ADMIN", "Administrative role")
        self.role_group = self.role_group_manager.create("USER_APP_ROLE_GROUP", "Policy group for the user app")

    def test_add_role_adds_role_to_policy(self):
        self.role_group_policy_manager.add_role(self.role_group.get_id(), self.role.get_id())
        role_group_policy = self.role_group_policy_manager.get_role_group_policy(self.role_group.get_id())
        role_policies = role_group_policy.get_role_policies()

        self.assertEqual(1, len(role_policies))
        self.assertEqual(self.role.get_id(), role_policies[0].get_role().get_id())
        self.assertEqual(self.role.get_const(), role_policies[0].get_role().get_const())
        self.assertEqual(self.role.get_description(), role_policies[0].get_role().get_description())
        self.assertEqual(0, len(role_policies[0].get_action_policies()))

    def test_add_role_fails_on_duplicate_role(self):
        self.role_group_policy_manager.add_role(self.role_group.get_id(), self.role.get_id())
        with self.assertRaises(RoleGroupPolicyAddRoleException):
            self.role_group_policy_manager.add_role(self.role_group.get_id(), self.role.get_id())
            self.fail("Did not fail on duplicate role for role group policy")

    def test_add_role_adds_multiple_roles(self):
        new_role = self.role_manager.create("BASIC", "Basic role")
        self.role_group_policy_manager.add_role(self.role_group.get_id(), self.role.get_id())
        self.role_group_policy_manager.add_role(self.role_group.get_id(), new_role.get_id())
        role_group_policy = self.role_group_policy_manager.get_role_group_policy(self.role_group.get_id())
        role_policies = role_group_policy.get_role_policies()

        self.assertEqual(2, len(role_policies))
        self.assertNotEqual(role_policies[0].get_uuid(), role_policies[1].get_uuid())
        self.assertNotEqual(role_policies[0].get_id(), role_policies[1].get_id())
        self.assertNotEqual(role_policies[0].get_role().get_id(), role_policies[1].get_role().get_id())
        self.assertNotEqual(role_policies[0].get_role().get_const(), role_policies[1].get_role().get_const())

    def test_add_action_adds_action_to_policy_role(self):
        role_group_role_id = self.role_group_policy_manager.add_role(self.role_group.get_id(), self.role.get_id())
        self.role_group_policy_manager.add_action(role_group_role_id, self.action.get_id())
        role_policy_group = self.role_group_policy_manager.get_role_group_policy(self.role_group.get_id())
        role_policy = role_policy_group.get_role_policies()[0]
        action_policies = role_policy.get_action_policies()

        self.assertEqual(1, len(action_policies))
        self.assertEqual(self.action.get_id(), action_policies[0].get_action().get_id())
        self.assertEqual(self.action.get_const(), action_policies[0].get_action().get_const())
        self.assertEqual(self.action.get_description(), action_policies[0].get_action().get_description())

    def test_add_action_fails_on_duplicate_action_for_role_policy(self):
        role_group_role_id = self.role_group_policy_manager.add_role(self.role_group.get_id(), self.role.get_id())
        self.role_group_policy_manager.add_action(role_group_role_id, self.action.get_id())
        with self.assertRaises(RoleGroupPolicyAddActionException):
            self.role_group_policy_manager.add_action(role_group_role_id, self.action.get_id())
            self.fail("Did not fail on duplicate actions for role policy in role group")

    def test_add_action_adds_multiple_actions_on_different_roles(self):
        roles = [
            self.role,
            self.role_manager.create("BASIC", "Basic role")
        ]
        actions = [
            self.action,
            self.action_manager.create("USER:DELETE", "Delete user action")
        ]
        first_rp_id = self.role_group_policy_manager.add_role(self.role_group.get_id(), roles[0].get_id())
        second_rp_id = self.role_group_policy_manager.add_role(self.role_group.get_id(), roles[1].get_id())
        self.role_group_policy_manager.add_action(first_rp_id, actions[0].get_id())
        self.role_group_policy_manager.add_action(second_rp_id, actions[1].get_id())
        role_group_policy = self.role_group_policy_manager.get_role_group_policy(self.role_group.get_id())
        role_policies = role_group_policy.get_role_policies()
        role_policy_map: Dict[int, RolePolicy] = {}
        for role_policy in role_policies:
            role_policy_map[role_policy.get_role().get_id()] = role_policy

        self.assertEqual(1, len(role_policy_map[roles[0].get_id()].get_action_policies()))
        self.assertEqual(1, len(role_policy_map[roles[1].get_id()].get_action_policies()))
        self.assertEqual(
            actions[0].get_const(),
            role_policy_map[roles[0].get_id()].get_action_policies()[0].get_action().get_const()
        )
        self.assertEqual(
            actions[1].get_const(),
            role_policy_map[roles[1].get_id()].get_action_policies()[0].get_action().get_const()
        )

    def test_delete_role_deletes_role_from_group_policy(self):
        role_group_role_id = self.role_group_policy_manager.add_role(self.role_group.get_id(), self.role.get_id())
        self.role_group_policy_manager.add_role(self.role_group.get_id(), self.role_manager.create(
            "BASIC",
            "Basic role"
        ).get_id())
        self.role_group_policy_manager.delete_role(role_group_role_id)
        role_group_policy = self.role_group_policy_manager.get_role_group_policy(self.role_group.get_id())

        self.assertEqual(1, len(role_group_policy.get_role_policies()))

    def test_delete_role_fails_on_invalid_role_group_role(self):
        with self.assertRaises(RoleGroupPolicyDeleteRoleException):
            self.role_group_policy_manager.delete_role(1)
            self.fail("Did not fail on invalid role group role id in deletion")

    def test_delete_action_deletes_action_from_role_policy(self):
        role_group_role_id = self.role_group_policy_manager.add_role(self.role_group.get_id(), self.role.get_id())
        role_group_role_action_id = self.role_group_policy_manager.add_action(role_group_role_id, self.action.get_id())
        self.role_group_policy_manager.delete_action(role_group_role_action_id)
        role_group_policy = self.role_group_policy_manager.get_role_group_policy(self.role_group.get_id())

        self.assertEqual(0, len(role_group_policy.get_role_policies()[0].get_action_policies()))

    def test_delete_action_fails_on_invalid_role_group_role_action(self):
        with self.assertRaises(RoleGroupPolicyDeleteActionException):
            self.role_group_policy_manager.delete_action(1)
            self.fail("Did not fail on invalid role group role action id in deletion")

    def test_get_role_group_policy_gets_role_group(self):
        self.role_group_policy_manager.add_role(self.role_group.get_id(), self.role.get_id())
        role_group_policy = self.role_group_policy_manager.get_role_group_policy(self.role_group.get_id())

        self.assertEqual(self.role_group.get_id(), role_group_policy.get_role_group().get_id())
        self.assertEqual(self.role_group.get_uuid(), role_group_policy.get_role_group().get_uuid())
        self.assertEqual(self.role_group.get_const(), role_group_policy.get_role_group().get_const())
        self.assertEqual(self.role_group.get_description(), role_group_policy.get_role_group().get_description())

    def test_get_role_group_policy_fails_on_empty_role_group_policy(self):
        with self.assertRaises(RoleGroupPolicyFetchException):
            self.role_group_policy_manager.get_role_group_policy(1)
            self.fail("Did not fail on empty role group policy")

    def tearDown(self) -> None:
        result = self.connection_manager.query_list([
            "DELETE FROM action WHERE 1=1",
            "DELETE FROM role WHERE 1=1",
            "DELETE FROM role_group WHERE 1=1"
        ])
        if not result.get_status():
            raise Exception(f"Failed to teardown role group policy test instance: {result.get_message()}")
