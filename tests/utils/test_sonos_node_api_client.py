import unittest

from snipssonos.utils.sonos_node_api_client import SonosNodeAPIClient
from snipssonos.exceptions import APIRequestWrongParams, APIRequestError

class TestSonosNodeAPIClientAPIRequests(unittest.TestCase):
    def setUp(self):
        self.client = SonosNodeAPIClient()

    def test_correct_action_request(self):
        self.assertEqual(self.client.build_action_request("zones"),"http://localhost:5005/zones")

    def test_action_request_empty_action(self):
        empty_action = ""
        with self.assertRaises(APIRequestWrongParams):
            self.client.build_action_request(empty_action)

    def test_action_request_none_action(self):
        empty_action = None
        with self.assertRaises(APIRequestWrongParams):
            self.client.build_action_request(empty_action)



if __name__ == '__main__':
    unittest.main()
