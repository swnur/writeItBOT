from textgears import grammar_check, spell_check, analyze_text

def process_command(command):
    # Mapping of commands to their respective functions
    command_functions = {
        '/grammar': grammar_check,
        '/spell': spell_check,
        '/analyze': analyze_text
    }

    # Extract the command and text
    for cmd, func in command_functions.items():
        if command.startswith(cmd):
            text = command[len(cmd):].strip()
            if len(text) >= 4000:
                return "Sorry, the text length cannot exceed 4,000 characters."
            return func(text)

    return "Unknown command"
