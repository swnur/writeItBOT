import matplotlib.pyplot as plt
import numpy as np


def generate_user_statistics(user_info):
    # Extract user data
    requests = user_info.get('requests', 0)
    words = user_info.get('words', 0)
    grammar_errors = user_info.get('errors', {'grammar': 0, 'spelling': 0, 'punctuation': 0})

    # Plot statistics
    labels = ['Requests', 'Words']
    values = [requests, words]

    plt.figure(figsize=(8, 6))
    x = np.arange(len(labels))
    plt.bar(x, values, align='center')
    plt.xticks(x, labels)
    plt.xlabel('Statistics')
    plt.ylabel('Count')
    plt.title('User Statistics')
    plt.tight_layout()

    # Save the plot
    plt_path = 'user_statistics.png'
    plt.savefig(plt_path)
    plt.close()

    # If grammar errors exist, add them to the plot
    if grammar_errors:
        error_labels = list(grammar_errors.keys())
        error_counts = [grammar_errors[label] for label in error_labels]

        plt.figure(figsize=(8, 6))
        x = np.arange(len(error_labels))
        plt.bar(x, error_counts, align='center')
        plt.xticks(x, error_labels)
        plt.xlabel('Error Type')
        plt.ylabel('Count')
        plt.title('Grammar Error Types')
        plt.tight_layout()

        # Save the plot
        plt_path_grammar = 'grammar_errors.png'
        plt.savefig(plt_path_grammar)
        plt.close()

        return {'error_type_distribution': 'error_type_distribution.png',
                'percentage_chance_of_mistake': 'percentage_chance_of_mistake.png'}

    return {'error_type_distribution': 'error_type_distribution.png',
            'percentage_chance_of_mistake': 'None'}


def generate_statistics(response, user_text, user_info):
    # Extract error data from the response
    errors = response.get('errors', [])

    # Extract error types and count occurrences
    error_types = {}
    total_errors = len(errors)
    for error in errors:
        error_type = error['type']
        error_types[error_type] = error_types.get(error_type, 0) + 1

    # Error type distribution
    labels = list(error_types.keys())
    sizes = [error_types[label] for label in labels]

    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Error Type Distribution')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.savefig('error_type_distribution.png')
    plt.close()

    # Overall percentage chance of making each type of mistake
    error_probabilities = {label: count / total_errors * 100 for label, count in error_types.items()}

    plt.figure(figsize=(8, 6))
    x = np.arange(len(error_probabilities))
    plt.bar(x, error_probabilities.values(), align='center')
    plt.xticks(x, error_probabilities.keys())
    plt.xlabel('Error Type')
    plt.ylabel('Percentage Chance')
    plt.title('Overall Percentage Chance of Making Each Type of Mistake')
    plt.savefig('percentage_chance_of_mistake.png')
    plt.close()

    return {'error_type_distribution': 'error_type_distribution.png',
            'percentage_chance_of_mistake': 'percentage_chance_of_mistake.png'}
