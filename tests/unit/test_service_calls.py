from app.service_calls import SingleClientIP
from . import RHTestCase


class TestServiceCalls(RHTestCase):

    def test_client_ip_valid(self):
        valid_request = {'client_ip': '192.168.0.0, 35.190.0.0, 35.191.10.0'}
        spoofed_request = {'client_ip': '200.30.20.10, 192.168.0.0, 35.190.0.0, 35.191.10.0'}
        spoofed_request_ipv6 = \
            {'client_ip': '2001:db8:3333:4444:CCCC:DDDD:EEEE:FFFF, 192.168.0.0, 35.190.0.0, 35.191.10.0'}
        unknown_request = {'client_ip': 'unknown, 192.168.0.0, 35.190.0.0, 35.191.10.0'}
        expected_valid = '192.168.0.0'
        self.assertEqual(SingleClientIP.single_client_ip(valid_request), expected_valid)
        self.assertEqual(SingleClientIP.single_client_ip(spoofed_request), expected_valid)
        self.assertEqual(SingleClientIP.single_client_ip(spoofed_request_ipv6), expected_valid)
        self.assertEqual(SingleClientIP.single_client_ip(unknown_request), expected_valid)

    def test_client_ip_invalid_single(self):
        request = {'client_id': '36be6b97-b4de-4718-8a74-8b27fb03ca8c', 'trace': '105445aa7843bc8bf206b12000100000'}
        single_ip_request = {'client_ip': '35.191.10.0'}
        single_ip_request.update(request)
        expected_empty = ''
        with self.assertLogs('respondent-home', 'WARN') as cm:
            self.assertEqual(SingleClientIP.single_client_ip(single_ip_request), expected_empty)
            self.assertLogEvent(cm, 'clientIP failed validation. Provided IP - ' + single_ip_request['client_ip'],
                                client_id=request['client_id'], trace=request['trace'])

    def test_client_ip_invalid_ipv6(self):
        request = {'client_id': '36be6b97-b4de-4718-8a74-8b27fb03ca8c', 'trace': '105445aa7843bc8bf206b12000100000'}
        invalid_request_ipv6 = {'client_ip': '2001:db8:3333:4444:CCCC:DDDD:EEEE:FFFF, 35.190.0.0, 35.191.10.0'}
        invalid_request_ipv6.update(request)
        expected_empty = ''
        with self.assertLogs('respondent-home', 'WARN') as cm:
            self.assertEqual(SingleClientIP.single_client_ip(invalid_request_ipv6), expected_empty)
            self.assertLogEvent(cm, 'clientIP failed validation. Provided IP - ' + invalid_request_ipv6['client_ip'],
                                client_id=request['client_id'], trace=request['trace'])
