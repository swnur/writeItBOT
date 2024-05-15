# from textgears import grammar_check, spell_check, analyze_text, correct_text

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

def check_text(text):
    api_key = '7fFGgE6Nm4jKqxrX'
    url = 'https://api.textgears.com/analyze'
    params = {
        'key': api_key,
        'text': text,
        'language': 'en-US',
        'ai': 'true'  # Enable AI for better quality analysis
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        result = response.json()
        return result
    else:
        print("Error:", response.status_code)
        return None

def process_text(command):

    result = check_text(text)

    if result:
        parsed_result = parse_response(result)
        print(parsed_result)

        return parsed_result
    else:
        return "Failed to check the text."


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