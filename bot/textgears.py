import requests
import json

def grammar_check(parsed_result):
    if parsed_result['status']:
        grammar_errors = [error for error in parsed_result['errors'] if error['type'] == 'grammar']
        if grammar_errors:
            message = 'Grammar mistakes found:\n'
            for error in grammar_errors:
                message += f"{error['bad']}, suggested {', '.join(error['better'])}. Description: {error['description']['en']}\n"
            return message
        else:
            return 'No grammar mistakes found.'
    else:
        return 'Failed to check grammar. Please try again later.'

def spell_check(parsed_result):
    if parsed_result['status']:
        spell_errors = [error for error in parsed_result['errors'] if error['type'] == 'spelling']
        if spell_errors:
            message = 'Spelling mistakes found:\n'
            for error in spell_errors:
                message += f"{error['bad']}, suggested {', '.join(error['better'])}. Description: {error['description']['en']}\n"
            return message
        else:
            return 'No spelling mistakes found.'
    else:
        return 'Failed to check spelling. Please try again later.'

def analyze_text(parsed_result):
    if parsed_result['status']:
        # Implement analysis logic based on the parsed result here
        return 'Analysis completed.'
    else:
        return 'Failed to analyze text. Please try again later.'

def correct_text(data):
    # Make a request to the TextGears API for text analysis
    response = requests.get('https://api.textgears.com/correct', params={'text': text, 'key': API_KEY})

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON
        response_data = response.json()

        # Check the status of the response
        if response_data.get('status', False):
            # If there are corrections, return the corrected text
            corrected_text = response_data['response'].get('corrected')
            if corrected_text:
                return corrected_text
            else:
                return "No errors detected."
        else:
            # If there are no corrections, return a message indicating no errors detected
            return "No errors detected."
    else:
        # If the request failed, return an error message
        return f"Failed to correct text. Error code: {response.status_code}"