from unittest.mock import patch, mock_open, MagicMock
import base64
import os
import sys
import unittest
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '../src'
        )
    )
)

import src.packages.infrastructure.azureoai_imgsummarizer as azureoai_imgsummarizer

class TestAzureOaiImgSummarizer(unittest.TestCase):
    @patch.dict(os.environ, {
        'AZURE_OPENAI_API_KEY': 'fake_key',
        'AZURE_OPENAI_ENDPOINT': 'fake_endpoint',
        'AZURE_OPENAI_API_VERSION': 'fake_version',
        'AZURE_OPENAI_DEPLOYMENT': 'fake_deployment'
    })
    @patch('builtins.open', new_callable=mock_open, read_data='test_image_data')
    @patch('base64.b64encode', return_value=b'base64_encoded_image')
    @patch('langchain_openai.chat_models.AzureChatOpenAI')
    def test_summarize(self, mock_azure_chat_openai, mock_b64encode, mock_open):
        # Given
        mock_llm = MagicMock()
        mock_llm.invoke.return_value.content = "summarized_content"
        mock_azure_chat_openai.return_value = mock_llm

        summarizer = azureoai_imgsummarizer.AzureOaiImgSummarizer()

        # When
        result = summarizer.summarize('fake_image_path.png')

        # Then
        self.assertEqual(result, "summarized_content")
        mock_open.assert_called_once_with('fake_image_path.png', 'rb')
        mock_b64encode.assert_called_once_with(b'test_image_data')
        mock_azure_chat_openai.assert_called_once_with(
            azure_endpoint='fake_endpoint',
            azure_deployment='fake_deployment',
            openai_api_version='fake_version'
        )
        mock_llm.invoke.assert_called_once()

if __name__ == '__main__':
    unittest.main()