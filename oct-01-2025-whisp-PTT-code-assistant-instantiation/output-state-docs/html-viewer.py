import webbrowser
import os
import sys

def view_html(html_path_or_content, is_file=True):
    if is_file:
        # Open local file in default browser
        if os.path.exists(html_path_or_content):
            webbrowser.open(f'file://{os.path.abspath(html_path_or_content)}')
        else:
            print(f"File not found: {html_path_or_content}")
    else:
        # Save temp file for content and open
        with open('temp_view.html', 'w', encoding='utf-8') as f:
            f.write(html_path_or_content)
        webbrowser.open('file://temp_view.html')
        # Optional: Clean up temp file after delay
        # import time; time.sleep(1); os.remove('temp_view.html')

# Example usage:
# From file: view_html(r'C:\example.html', is_file=True)
# From string: html = '<html><body><h1>Hello World!</h1></body></html>'; view_html(html, is_file=False)

if __name__ == '__main__':
    # sys.argv[0] is the script name ('html-viewer.py')
    # sys.argv[1] is the first argument (the HTML file path)
    if len(sys.argv) > 1:
        # Get the file path from the command line argument
        file_path = sys.argv[1]
        print(f"Attempting to open file: {file_path}")
        view_html(file_path, is_file=True)
    else:
        print("Error: No HTML file path provided.")
        print("Usage: python html-viewer.py <path_to_html_file>")