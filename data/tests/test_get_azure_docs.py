import unittest
from unittest.mock import patch
from data.get_azure_docs import fetch_azure_docs


class TestFetchAzureDocs(unittest.TestCase):
    @patch("data.get_azure_docs.requests.get")
    def test_fetch_azure_docs(self, mock_get):
        mock_html = """
        <html>
            <body>
                <a href="/en-us/azure/some-doc">Some Doc</a>
                <a href="/en-us/azure/another-doc">Another Doc</a>
                <a href="/not-azure/doc">Not Azure Doc</a>
            </body>
        </html>
        """
        mock_get.return_value.text = mock_html

        expected_docs = [
            {
                "title": "Some Doc",
                "url": "https://learn.microsoft.com/en-us/azure/some-doc",
            },
            {
                "title": "Another Doc",
                "url": "https://learn.microsoft.com/en-us/azure/another-doc",
            },
        ]

        result = fetch_azure_docs()
        self.assertEqual(result, expected_docs)


if __name__ == "__main__":
    unittest.main()
