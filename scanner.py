import re

# Define regular expressions for tokens (including all C keywords)
patterns = {
    'keyword': r'\b(auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while)\b',
    'identifier': r'\b(?!comment\b)[a-zA-Z_]\w*\b',  # Excludes 'comment' as an identifier
    'operator': r'[-+*/=<>!&|^%]',
    'constant': r'\b\d+(\.\d+)?(e[+-]?\d+)?\b|\b\d*\.\d+(e[+-]?\d+)?\b',
    'string_literal': r'"([^"\\]|\\.)*"',  # Handles escape sequences within strings
    'special_character': r'[()\[\]{};:,]',
    'whitespace': r'\s+'
}

def remove_comments(input_string):
    # Remove single-line comments
    input_string = re.sub(r'//.*', '', input_string)
    # Remove multi-line comments
    input_string = re.sub(r'/\*(.|\n)*?\*/', '', input_string)
    return input_string

def tokenize(input_string):
    input_string = remove_comments(input_string)
    tokens = []
    regex_patterns = {token_type: re.compile(pattern, re.DOTALL) for token_type, pattern in patterns.items()}

    while input_string:
        found = False
        for token_type, regex in regex_patterns.items():
            match = regex.match(input_string)
            if match:
                found = True
                token = match.group(0)
                if token_type != 'whitespace':
                    tokens.append(f"{token_type.capitalize()}: {token}")
                input_string = input_string[len(token):]
                break

        if not found:
            print(f"Unknown token: {input_string[0]}")
            input_string = input_string[1:]

    return tokens

def write_tokens_to_file(tokens):
    with open("tokens.txt", "w") as file:
        for token in tokens:
            file.write(token + "\n")

def read_tokens_file():
    try:
        with open("tokens.txt", "r") as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print("Tokens file not found.")

def tokenize_and_display(input_string):
    tokens = tokenize(input_string)
    write_tokens_to_file(tokens)
    read_tokens_file()

# Example input string
input_string = " for (e = 1.3e-2 ; i = 5.1e3; i = i + 1) fun1 "

# Tokenize the input string and display the tokens
tokenize_and_display(input_string)
