import requests
import json

def parse_response(result):
    parsed_result = {}
    if 'response' in result:
        parsed_result['status'] = True
        parsed_result['errors'] = []
        for error in result['response']['grammar']['errors']:
            parsed_error = {
                'bad': error['bad'],
                'description': error['description'],
                'better': error['better'],
                'type': error['type']
            }
            parsed_result['errors'].append(parsed_error)
    else:
        parsed_result['status'] = False
    return parsed_result


def check_text(text, api_key):
    url = 'https://api.textgears.com/analyze'
    params = {
        'key': api_key,
        'text': text,
        'language': 'en-US',
        'ai': 'true'  # Enable AI for better quality analysis
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad HTTP status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None


def process_text(text, api_key):
    result = check_text(text, api_key)

    if result:
        try:
            parsed_result = parse_response(result)
            print(parsed_result)
            return parsed_result
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            return None
    else:
        return "Failed to check the text."


def correct_text(data, api_key):
    try:
        response = requests.get('https://api.textgears.com/correct', params={'text': data, 'key': api_key})
        response.raise_for_status()  # Raise an error for bad HTTP status codes

        response_data = response.json()

        if response_data.get('status', False):
            corrected_text = response_data['response'].get('corrected')
            if corrected_text:
                return corrected_text
            else:
                return "No errors detected."
        else:
            return "No errors detected."
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return f"Failed to correct text. Error: {str(e)}"
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return None
