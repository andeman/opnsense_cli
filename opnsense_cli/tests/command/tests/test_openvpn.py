import unittest
from unittest.mock import patch
from click.testing import CliRunner
from opnsense_cli.api.client import ApiClient
from opnsense_cli.command.openvpn import openvpn


class TestOpenvpnCommands(unittest.TestCase):
    def setUp(self):
        self._api_data_fixtures_providers = {
            "2": {
                "name": "OpenVPN Server UDP:1194",
                "mode": "server_tls",
                "vpnid": "2",
                "hostname": "vpn.example.com",
                "template": "PlainOpenVPN",
                "local_port": "1194",
                "random_local_port": "1",
                "validate_server_cn": "1",
                "cryptoapi": "",
                "auth_nocache": "",
                "plain_config": ""
            },
        }
        self._api_data_fixtures_templates = {
            "ArchiveOpenVPN": {
                "name": "Archive",
                "supportedOptions": ["plain_config", "p12_password", "random_local_port", "auth_nocache", "cryptoapi"]
            },
            "PlainOpenVPN": {
                "name": "File Only",
                "supportedOptions": ["plain_config", "random_local_port", "auth_nocache", "cryptoapi"]
            },
            "TheGreenBow": {
                "name": "TheGreenBow",
                "supportedOptions": []
            },
            "ViscosityVisz": {
                "name": "Viscosity (visz)",
                "supportedOptions": ["plain_config", "p12_password", "random_local_port", "auth_nocache", "cryptoapi"]
            },
        }
        self._api_data_fixtures_accounts = {
            "57194c007be18": {
                "description": "vpnuser1", "users": []
            },
            "57194c17cab84": {
                "description": "vpnuser2", "users": []
            },
        }
        self._api_data_fixtures_download = {
            "result": "ok",
            "changed": "false",
            "filename": "OpenVPN_Server_vpnuser1.ovpn",
            "filetype": "text/plain",
            "content": "T3BlblZQTiBjZXJ0aWZpY2F0ZQo="
        }
        self._api_client_args_fixtures = [
            'api_key',
            'api_secret',
            'https://127.0.0.1/api',
            True,
            '~/.opn-cli/ca.pem',
            60
        ]

    @patch('opnsense_cli.command.openvpn.ApiClient.execute')
    def test_providers(self, api_response_mock):
        api_response_mock.return_value = self._api_data_fixtures_providers
        client_args = self._api_client_args_fixtures
        client = ApiClient(*client_args)

        runner = CliRunner()
        result = runner.invoke(openvpn, ['providers'], obj=client)

        self.assertIn(
            "2 OpenVPN Server UDP:1194 server_tls 2 vpn.example.com PlainOpenVPN 1194\n",
            result.output
        )
        self.assertEqual(0, result.exit_code)

    @patch('opnsense_cli.command.openvpn.ApiClient.execute')
    def test_templates(self, api_response_mock):
        api_response_mock.return_value = self._api_data_fixtures_templates
        client_args = self._api_client_args_fixtures
        client = ApiClient(*client_args)

        runner = CliRunner()
        result = runner.invoke(openvpn, ['templates'], obj=client)

        self.assertIn(
            "ArchiveOpenVPN Archive ['plain_config', 'p12_password', 'random_local_port', 'auth_nocache', 'cryptoapi']\n" +
            "PlainOpenVPN File Only ['plain_config', 'random_local_port', 'auth_nocache', 'cryptoapi']\n"
            "TheGreenBow TheGreenBow []\n"
            "ViscosityVisz Viscosity (visz) ['plain_config', 'p12_password', 'random_local_port', 'auth_nocache', 'cryptoapi']\n",
            result.output
        )
        self.assertEqual(0, result.exit_code)

    @patch('opnsense_cli.command.openvpn.ApiClient.execute')
    def test_accounts(self, api_response_mock):
        api_response_mock.return_value = self._api_data_fixtures_accounts
        client_args = self._api_client_args_fixtures
        client = ApiClient(*client_args)

        runner = CliRunner()
        result = runner.invoke(openvpn, ['accounts', '2'], obj=client)

        self.assertIn(
            "57194c007be18 vpnuser1 []\n" +
            "57194c17cab84 vpnuser2 []\n",
            result.output
        )
        self.assertEqual(0, result.exit_code)

    @patch('opnsense_cli.command.openvpn.ApiClient.execute')
    def test_download(self, api_response_mock):
        api_response_mock.return_value = self._api_data_fixtures_download
        client_args = self._api_client_args_fixtures
        client = ApiClient(*client_args)

        runner = CliRunner()
        result = runner.invoke(openvpn, ['download', '2', '57194c007be18'], obj=client)

        self.assertIn(
            "OpenVPN_Server_vpnuser1.ovpn T3BlblZQTiBjZXJ0aWZpY2F0ZQo=\n",
            result.output
        )
        self.assertEqual(0, result.exit_code)