import unittest
from unittest.mock import patch, Mock
from handlers.commands import *

class TestAutoCorrection(unittest.TestCase):

    #Simulating the case with the corrected text.
    @patch('requests.get') #simulating HTTP request without making any network calls.
    def test_correct_text(self, mock_get):
        # Mock the API response
        mock_response = Mock()
        #mocking the http response, if the response was successful it should return None.
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            'status': True,
            'response': {
                'corrected': 'Hello, world! I will become a developer.'
            }
        }
        mock_get.return_value = mock_response

        # Call the function with the mocked requests.get
        result = correct_text('Hellou world! I will becomee a develper', 'api_key')

        # Assert the function returned the corrected text
        self.assertEqual(result, 'Hello, world! I will become a developer.')


    #Simulating the case when there is nothing to correct.
    @patch('requests.get')
    def test_correct_text_no_errors(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            'status': True,
            'response': {
                'corrected': ''
            }
        }
        mock_get.return_value = mock_response

        result = correct_text('Hello, world!', 'api_key')
        self.assertEqual(result, 'No errors detected.')

    @patch('requests.get')
    def test_correct_text_failed_request(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException('Network error')
        result = correct_text('Hello, world!', 'api_key')
        self.assertTrue('Failed to correct text' in result)

    @patch('requests.get')
    def test_check_text_success(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            'response': {
                'grammar': {
                    'errors': [
                        {
                            'bad': 'Hellou',
                            'description': 'Spelling mistake',
                            'better': ['Hello'],
                            'type': 'spelling'
                        }
                    ]
                }
            }
        }
        mock_get.return_value = mock_response

        result = check_text('Hellou world!', 'api_key')
        self.assertIn('response', result)

    def test_parse_response_valid(self):
        result = {
            'response': {
                'grammar': {
                    'errors': [
                        {
                            'bad': 'Hellou',
                            'description': 'Spelling mistake',
                            'better': ['Hello'],
                            'type': 'spelling'
                        }
                    ]
                }
            }
        }
        parsed_result = parse_response(result)
        self.assertTrue(parsed_result['status'])
        self.assertEqual(len(parsed_result['errors']), 1)
        self.assertEqual(parsed_result['errors'][0]['bad'], 'Hellou')

    def test_parse_response_invalid(self):
        result = {}
        parsed_result = parse_response(result)
        self.assertFalse(parsed_result['status'])

if __name__ == '__main__':
    unittest.main()
