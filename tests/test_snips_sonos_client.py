import unittest

from snipssonos.snipssonos_node import SnipsSonosClient
from snipssonos.exceptions import APIRequestWrongParams

class TestSnipsSonosClientAPIRequests(unittest.TestCase):
    def setUp(self):
        self.client = SnipsSonosClient()

    def test_correct_request(self):
        device = "device"
        action = "play"
        self.assertEqual(self.client.build_request(device, action), "http://localhost:5005/device/play")

    def test_correct_request_with_params(self):
        device = "device"
        action = "volume"
        param = "+15"
        self.assertEqual(self.client.build_request(device, action, param), "http://localhost:5005/device/volume/+15")

    def test_with_missing_argument_device(self):
        action = "volume"
        with self.assertRaises(APIRequestWrongParams):
            self.client.build_request(None, action)

    def test_with_missing_argument_device_empty_string(self):
        action = "volume"
        with self.assertRaises(APIRequestWrongParams):
            self.client.build_request("", action)


    def test_with_missing_argument_action(self):
        device = "device"
        with self.assertRaises(APIRequestWrongParams):
            self.client.build_request(device, None)

    def test_with_missing_argument_action_empty(self):
        device = "device"
        with self.assertRaises(APIRequestWrongParams):
            self.client.build_request(device, "")


    def test_with_missing_argument_param_1(self):
        device = "device"
        action = "volume"

        with self.assertRaises(APIRequestWrongParams):
            self.client.build_request(device, action, None)

    def test_with_missing_argument_param_2(self):
        device = "device"
        action = "volume"

        with self.assertRaises(APIRequestWrongParams):
            self.client.build_request(device, action, "")


if __name__ == '__main__':
    unittest.main()
