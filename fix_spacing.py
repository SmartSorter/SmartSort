import os
import re

def fix_spacing(content):
    # Fix spaces around dots
    content = re.sub(r'\s*\.\s*', '.', content)
    # Fix spaces before commas and colons
    content = re.sub(r'\s+,', ',', content)
    content = re.sub(r'\s+:', ':', content)
    # Fix spaces around parentheses
    content = re.sub(r'\(\s+', '(', content)
    content = re.sub(r'\s+\)', ')', content)
    # Fix spaces around brackets
    content = re.sub(r'\[\s+', '[', content)
    content = re.sub(r'\s+\]', ']', content)
    # Fix spaces around assignment and comparison (mostly)
    content = re.sub(r'\s*=\s*', '=', content)
    content = re.sub(r'\s*!=\s*', '!=', content)
    content = re.sub(r'\s*==\s*', '==', content)
    content = re.sub(r'\s*>\s*', '>', content)
    content = re.sub(r'\s*<\s*', '<', content)
    # Ensure space after comma
    content = re.sub(r',([^\s])', r', \1', content)
    # Ensure space after colon (in types or dicts)
    content = re.sub(r':([^\s\n])', r': \1', content)
    
    return content

def cleanup_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                print(f"Fixing spacing in {path}...")
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                fixed_content = fix_spacing(content)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)

if __name__ == "__main__":
    cleanup_directory("app")
