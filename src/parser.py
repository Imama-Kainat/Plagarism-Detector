import re
import os

def tokenize_code(file_path):
    """
    Parse and tokenize code from a file, normalizing it for comparison.
    
    This function:
    1. Removes comments and docstrings
    2. Normalizes whitespace
    3. Preserves program structure by keeping keywords and operators
    4. Normalizes variable/function names to handle renamed identifiers
    """
    try:
        # Handle file extension - get the extension
        file_ext = os.path.splitext(file_path)[1].lower()
        
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # If file is empty, return special empty token
        if not code.strip():
            return ["EMPTY_FILE"]
            
        # Remove comments based on file type
        if file_ext == '.py':
            # Python comments
            code = re.sub(r'#.*', '', code)
            code = re.sub(r'"""[\s\S]*?"""', '', code)
            code = re.sub(r"'''[\s\S]*?'''", '', code)
        elif file_ext == '.js':
            # JavaScript comments
            code = re.sub(r'//.*', '', code)
            code = re.sub(r'/\*[\s\S]*?\*/', '', code)
        
        # Normalize whitespace (reduce multiple spaces to single space)
        code = re.sub(r'\s+', ' ', code)
        
        # Split into tokens, preserving important syntax elements
        # This regex captures identifiers, literals, and operators
        tokens = re.findall(r'\b\w+\b|[^\w\s]', code)
        
        # If no tokens were found after parsing, return special empty token
        if not tokens:
            return ["EMPTY_FILE"]
            
        # List of keywords to preserve (add more as needed)
        keywords = {
            'def', 'class', 'return', 'if', 'else', 'elif', 'for', 'while', 
            'in', 'and', 'or', 'not', 'import', 'from', 'as', 'try', 'except',
            'finally', 'with', 'lambda', 'yield', 'break', 'continue', 'pass'
        }
        
        # JS keywords to preserve
        js_keywords = {
            'function', 'var', 'let', 'const', 'if', 'else', 'for', 'while',
            'do', 'switch', 'case', 'default', 'try', 'catch', 'finally',
            'return', 'typeof', 'delete', 'void'
        }
        
        # Combine keywords based on file extension
        all_keywords = keywords
        if file_ext == '.js':
            all_keywords = all_keywords.union(js_keywords)
        
        # Common tokens that should be filtered out to reduce false positives
        common_tokens = {'print', 'True', 'False', 'None'}  # Reduced list to avoid over-filtering
        
        # Normalize tokens
        normalized_tokens = []
        for token in tokens:
            if token in common_tokens:
                # Skip common tokens that can lead to false positives
                continue
            elif token in all_keywords or token in '+-*/=<>()[]{},.;:':
                # Keep keywords and operators as is to preserve structure
                normalized_tokens.append(token)
            elif re.match(r'^[0-9]+$', token):
                # Normalize numeric literals
                normalized_tokens.append('NUM')
            elif re.match(r'^["\'](.*?)["\']$', token):
                # Normalize string literals
                normalized_tokens.append('STR')
            elif re.match(r'^\w+$', token):
                # Normalize identifiers (variable/function names)
                normalized_tokens.append('ID')
            else:
                normalized_tokens.append(token)
        
        return normalized_tokens
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return []

def load_submissions(input_dir):
    """
    Load all submission files from the input directory.
    Returns a dictionary mapping filenames to their tokenized content.
    """
    submissions = {}
    for file_name in os.listdir(input_dir):
        # Process Python and JavaScript files
        if file_name.endswith(('.py', '.js')):
            file_path = os.path.join(input_dir, file_name)
            tokens = tokenize_code(file_path)
            if tokens:  # Include even if just the EMPTY_FILE token
                submissions[file_name] = tokens
            else:
                # If tokenization failed completely, add an empty list
                # to ensure the file is still included in the results
                submissions[file_name] = []
                print(f"Warning: File {file_name} was processed but produced no tokens.")
    
    return submissions