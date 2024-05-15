import matplotlib.pyplot as plt
import numpy as np
import os

def generate_statistics(response, user_text):
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
    error_type_distribution_path = 'error_type_distribution.png'
    plt.savefig(error_type_distribution_path)
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
    percentage_chance_of_mistake_path = 'percentage_chance_of_mistake.png'
    plt.savefig(percentage_chance_of_mistake_path)
    plt.close()

    return {'error_type_distribution': error_type_distribution_path,
            'percentage_chance_of_mistake': percentage_chance_of_mistake_path}
