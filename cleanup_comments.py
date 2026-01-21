import tokenize
import os
import io

def remove_comments_surgically(content):
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(content).readline))
    except Exception:
        return content # Skip files with syntax errors

    # Filter out comments
    comment_token_coords = []
    for tok in tokens:
        if tok.type == tokenize.COMMENT:
            comment_token_coords.append((tok.start, tok.end))
    
    if not comment_token_coords:
        return content

    # Sort comments in reverse order to remove them without affecting previous indices
    comment_token_coords.sort(key=lambda x: x[0], reverse=True)
    
    lines = content.splitlines(keepends=True)
    for start, end in comment_token_coords:
        s_row, s_col = start
        e_row, e_col = end
        
        # Rows are 1-indexed
        idx = s_row - 1
        line = lines[idx]
        
        # Remove comment part
        # If it's a whole line comment, remove the line if it becomes empty
        if line.strip().startswith("#"):
             lines[idx] = "" # Keep indices consistent for now, we'll join later
        else:
             # Inline comment
             lines[idx] = line[:s_col].rstrip() + line[e_col:]
             # If we just removed to the end of line, add newline back if it was there
             if not lines[idx].endswith('\n') and line.endswith('\n'):
                 lines[idx] += '\n'

    return "".join(lines)

def cleanup_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                print(f"Surgically processing {path}...")
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                cleaned_content = remove_comments_surgically(content)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)

if __name__ == "__main__":
    cleanup_directory("app")
