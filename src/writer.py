import csv
import os
from typing import List, Dict, Any

class CSVWriter:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def write_batch(self, data: List[Dict[str, Any]]):
        """
        Writes a batch of data to the CSV file. 
        Automatically handles header creation if the file is new.
        """
        if not data:
            return

        # Check if file exists to determine if we need to write the header
        file_exists = os.path.isfile(self.file_path)
        
        try:
            # Using 'a' (append) mode
            # encoding='utf-8-sig' handles Excel's UTF-8 quirks
            with open(self.file_path, mode='a', newline='', encoding='utf-8-sig') as f:
                # Use the keys from the first dictionary as fieldnames (schema)
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                
                if not file_exists:
                    writer.writeheader()
                
                writer.writerows(data)
                
        except IOError as e:
            print(f" File Error: Could not write to {self.file_path}. {e}")

    def clear_file(self):
        """Optionally clear the file before starting a new run."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

if __name__ == "__main__":
    test_data = [{"id": 1, "name": "test"}, {"id": 2, "name": "demo"}]
    writer = CSVWriter("data/test_output.csv")
    writer.clear_file()  # Start fresh
    writer.write_batch(test_data)
    print(" Test file 'data/test_output.csv' created successfully.")