import matplotlib.pyplot as plt
import numpy as np


def generate_user_statistics(user_info):
    # Extract user data
    requests = user_info.get('requests', 0)
    words = user_info.get('words', 0)
    errors = user_info.get('errors', {})

    # Create a table
    table_data = [
        ['Requests', requests],
        ['Words', words]
    ]
    for mistake_type, count in errors.items():
        table_data.append([f'Total {mistake_type.capitalize()} Mistakes', count])

    # Plot the table
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=table_data, loc='center', cellLoc='center', colLabels=['Statistic', 'Value'])
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.2)

    # Save the table
    plt_path = 'user_statistics_table.png'
    plt.savefig(plt_path)
    plt.close()

    # If grammar errors exist, add them to the plot
    if errors:
        # Error type distribution
        labels = list(user_info['errors'].keys())
        sizes = [user_info['errors'][label] for label in labels]

        plt.figure(figsize=(8, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title('Error Type Distribution')
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        plt.savefig('error_type_distribution.png')
        plt.close()

        # Calculate the average number of errors per word and per sentence
        errors_per_word = user_info['errors']['spelling'] / words * 100
        errors_per_sentence = user_info['errors']['grammar'] / words * 100

        # Plotting the bar chart
        labels = ['Grammar Errors per Sentence', 'Spelling Errors per Word']
        values = [errors_per_sentence, errors_per_word]

        plt.figure(figsize=(8, 6))
        x = np.arange(len(labels))
        plt.bar(x, values, align='center', color=['blue', 'green'])
        plt.xticks(x, labels)
        plt.ylabel('Percentage')
        plt.title('Errors per Sentence and per Word')
        plt.savefig('errors_per_sentence_and_word.png')
        plt.close()

        return {
            'user_statistics': 'user_statistics_table.png',
            'error_type_distribution': 'error_type_distribution.png',
            'errors_per_sentence_and_word': 'errors_per_sentence_and_word.png'
        }

    return {'user_statistics': 'user_statistics.png',
            'error_type_distribution': 'None',
            'errors_per_sentence_and_word': 'None'}



def generate_statistics(response, user_text, user_info):
    # Extract error data from the response
    errors = response.get('errors', [])

    # Extract error types and count occurrences
    error_types = {'grammar': 0, 'spelling': 0}
    total_errors = len(errors)
    for error in errors:
        error_type = error['type']
        if error_type in error_types:
            error_types[error_type] += 1
        user_info['errors'][error_type] = error_types.get(error_type, 0) + 1

    # Error type distribution
    labels = list(error_types.keys())
    sizes = [error_types[label] for label in labels]

    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Error Type Distribution')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.savefig('error_type_distribution.png')
    plt.close()

    # Extracting word and sentence count
    words = len(user_text.split())
    sentences = len(user_text.split('.'))

    # Calculate the average number of errors per word and per sentence
    errors_per_word = error_types['spelling'] / words * 100
    errors_per_sentence = error_types['grammar'] / words * 100

    # Plotting the bar chart
    labels = ['Grammar Errors per Sentence', 'Spelling Errors per Word']
    values = [errors_per_sentence, errors_per_word]

    plt.figure(figsize=(8, 6))
    x = np.arange(len(labels))
    plt.bar(x, values, align='center', color=['blue', 'green'])
    plt.xticks(x, labels)
    plt.ylabel('Percentage')
    plt.title('Errors per Sentence and per Word')
    plt.savefig('errors_per_sentence_and_word.png')
    plt.close()

    return {
        'error_type_distribution': 'error_type_distribution.png',
        'errors_per_sentence_and_word': 'errors_per_sentence_and_word.png'
    }
