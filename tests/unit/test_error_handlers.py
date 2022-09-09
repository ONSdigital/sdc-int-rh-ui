from . import RHTestCase


class TestErrorHandlers(RHTestCase):

    async def test_partial_path_redirects_to_index_en(self):
        with self.assertLogs('respondent-home', 'DEBUG') as cm:
            response = await self.client.request('GET', str(self.get_start_en).rstrip('/'))
        self.assertLogEvent(cm, 'redirecting to index')
        self.assertEqual(response.status, 200)
        contents = await response.content.read()
        self.assertIn('Start study', str(contents))
        self.assertEqual(contents.count(b'input--text'), 1)
        self.assertIn(b'type="submit"', contents)

    async def test_404_renders_template(self):
        response = await self.client.request('GET', '/unknown-path')
        self.assertEqual(response.status, 404)
        contents = str(await response.content.read())
        self.assertIn('Page not found', contents)
