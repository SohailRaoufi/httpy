import os
def generate_directory_listing(directory_path, req_path):
    try:
        files = os.listdir(directory_path)  # Get list of files and directories
        files_html = "".join(f'<li><a href="{req_path.rstrip('/') + '/' + file}">{file}</a></li>' for file in files)  # Generate HTML links

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Index of {directory_path}</title>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 20px; }}
                ul {{ list-style: none; padding: 0; }}
                li {{ margin: 5px 0; }}
                a {{ text-decoration: none; color: #007bff; }}
                a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <h2>Index of {directory_path}</h2>
            <ul>
                {files_html}
            </ul>
        </body>
        </html>
        """

        return html_content
    except Exception as e:
        print(e)
        return None
