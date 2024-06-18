'''
The script is designed to perform the following tasks:

Search through a folder and its subfolders recursively until it finds a specific file specified by the user.
Once the target file is found, it copies the file to another location.
It then retrieves a list of files from the location where the target file was copied to.
It generates a JSON object containing information about each file, including the file path, size, and type (file or directory).
The JSON object is then inserted into a pandas DataFrame.
Finally, the DataFrame is saved as a CSV file.

'''

import os
import shutil
import json
import pandas as pd

class FileSearch:
    def __init__(self, start_path, target_file):
        """
        Initialize the FileSearch object.

        Args:
            start_path (str): The root path to start the search.
            target_file (str): The name of the file to search for.
        """
        self.start_path = start_path
        self.target_file = target_file
        self.found_file_path = None

    def __call__(self):
        """
        Performs the file search and returns the list of files as JSON if the target file is found.

        Returns:
            str or None: JSON string containing file properties or None if target file is not found.
        """
        self._search_file(self.start_path)
        if self.found_file_path:
            files_list = self._get_files_list(self.found_file_path)
            return self._generate_json(files_list)
        else:
            print(f"File '{self.target_file}' not found.")
            return None

    def _search_file(self, path):
        """
        Recursively searches for the target file starting from the given path.

        Args:
            path (str): The path to start the search.
        """
        for root, dirs, files in os.walk(path):
            if self.target_file in files:
                self.found_file_path = os.path.join(root, self.target_file)
                break

    def _get_files_list(self, path):
        """
        Generates a list of files with their properties (path, size, type).

        Args:
            path (str): The path to search for files.

        Returns:
            list: List of dictionaries containing file properties.
        """
        files_list = []
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                file_stat = os.stat(file_path)
                file_info = {
                    'path': file_path,
                    'size': file_stat.st_size,
                    'type': 'file' if os.path.isfile(file_path) else 'directory'
                }
                files_list.append(file_info)
        return files_list

    def _generate_json(self, files_list):
        """
        Generates JSON from the list of files.

        Args:
            files_list (list): List of dictionaries containing file properties.

        Returns:
            str: JSON string containing file properties.
        """
        return json.dumps(files_list, indent=4)

def main():
    # Specify the root path to start the search
    start_path = "/path/to/search"
    # Specify the target file to search for
    target_file = "target_file.txt"

    # Create a FileSearch object
    file_search = FileSearch(start_path, target_file)
    # Perform the file search and get files information as JSON
    files_json = file_search()

    if files_json:
        # Load JSON into pandas DataFrame
        df = pd.read_json(files_json)

        # Save DataFrame to CSV
        df.to_csv('files_info.csv', index=False)
        print("CSV file 'files_info.csv' generated successfully.")

if __name__ == "__main__":
    main()
