from . import RHTestCase


class TestInfo(RHTestCase):
    async def test_get_info(self):
        response = await self.client.request('GET', '/info')
        json = await response.json()
        self.assertEqual(response.status, 200)
        self.assertIn('name', json)
