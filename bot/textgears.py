import requests

API_KEY = 'j1mNmf33oEaxpHh1'

def parse_errors(response):
    errors_dict = {}
    if response.get('status', False) and response.get('response'):
        errors = response['response'].get('errors', [])
        for error_info in errors:
            error_id = error_info.get('id')
            offset = error_info.get('offset')
            length = error_info.get('length')
            bad_word = error_info.get('bad')
            suggestions = error_info.get('better', [])
            error_type = error_info.get('type')
            errors_dict[error_id] = {
                'offset': offset,
                'length': length,
                'bad_word': bad_word,
                'suggestions': suggestions,
                'error_type': error_type
            }
    return errors_dict

def grammar_check(text):
    # Make a request to the TextGears API for grammar checking
    response = requests.get('https://api.textgears.com/grammar', params={'text': text, 'key': API_KEY})
    # Process the response and extract grammar errors
    # For simplicity, let's assume the response is in JSON format
    if response.status_code == 200:
        # Process the response and extract grammar errors
        # For simplicity, let's assume the response is in JSON format
        dict_err = parse_errors(response)
        # Return the number of grammar errors found
        return f"Grammar errors found: {len(dict_err)}"
    else:
        # If the request failed, return an error message
        return f"Failed to check grammar. Error code: {response.status_code}"

def spell_check(text):
    # Make a request to the TextGears API for spell checking
    response = requests.get('https://api.textgears.com/check.php', params={'text': text, 'key': 'YOUR_TEXTGEARS_API_KEY', 'language': 'en-US'})
    # Process the response and extract spelling errors
    # For simplicity, let's assume the response is in JSON format
    errors = response.json().get('errors', [])
    return f"Spelling errors found: {len(errors)}"

def analyze_text(text):
    # Make a request to the TextGears API for text analysis
    response = requests.get('https://api.textgears.com/check.php', params={'text': text, 'key': 'YOUR_TEXTGEARS_API_KEY', 'language': 'en-US'})
    # Process the response and extract analysis data
    # For simplicity, let's assume the response is in JSON format
    analysis = response.json().get('analysis', {})
    return f"Text analysis: {analysis}"
