from . import RHTestCase


class TestInfo(RHTestCase):
    async def test_get_info(self):
        response = await self.client.request('GET', '/info')
        json = await response.json()
        self.assertEqual(response.status, 200)
        self.assertIn('name', json)
        self.assertIn('version', json)

    async def test_get_info_check(self):
        response = await self.client.request('GET', '/info?check=true')
        self.assertEqual(response.status, 200)
        self.assertIn('ready', await response.json())
