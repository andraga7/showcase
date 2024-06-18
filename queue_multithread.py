'''
The script is designed to perform the following tasks:

    Generate random sample data with attributes like name, age, city, and salary.
    Utilize multithreading to speed up the data generation process.
    Write the generated data to a CSV file.

The script is organized into the following components:

    DataGenerator Class: This class generates random sample data using multiple threads. It divides the data generation task among the specified number of threads, and each thread generates a portion of the data independently. The generated data is stored in a queue for further processing.

    CSVWriter Class: This class writes the generated data to a CSV file. It takes the data from the queue and writes it to a CSV file using the csv module.

    main() Function: This function is the entry point of the script. It initializes the DataGenerator class, generates random sample data, and writes it to a CSV file using the CSVWriter class.
    
'''

import threading
import queue
import random
import io
import csv

class DataGenerator:
    def __init__(self, num_threads, num_records):
        """
        Initialize the DataGenerator object.

        Args:
            num_threads (int): Number of threads to use for data generation.
            num_records (int): Total number of records to generate.
        """
        self.num_threads = num_threads
        self.num_records = num_records

    def generate_data(self):
        """
        Generates random sample data using multiple threads.

        Returns:
            list: List of dictionaries containing sample data.
        """
        data_queue = queue.Queue()

        # Create and start worker threads
        threads = []
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self._generate_worker, args=(data_queue,))
            thread.start()
            threads.append(thread)

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        # Collect data from queue
        data = []
        while not data_queue.empty():
            data.append(data_queue.get())

        return data

    def _generate_worker(self, data_queue):
        """
        Worker function for generating random sample data.

        Args:
            data_queue (Queue): Queue to store generated data.
        """
        for _ in range(self.num_records // self.num_threads):
            data = {
                'name': self._generate_name(),
                'age': random.randint(20, 50),
                'city': self._generate_city(),
                'salary': random.randint(30000, 100000)
            }
            data_queue.put(data)

    def _generate_name(self):
        """
        Generates a random name.

        Returns:
            str: Random name.
        """
        names = ['Alice', 'Bob', 'Charlie', 'David', 'Eve']
        return random.choice(names)

    def _generate_city(self):
        """
        Generates a random city.

        Returns:
            str: Random city.
        """
        cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Miami']
        return random.choice(cities)

class CSVWriter:
    def __init__(self, data):
        """
        Initialize the CSVWriter object.

        Args:
            data (list): List of dictionaries containing data to write to CSV.
        """
        self.data = data

    def write_to_csv(self, filename):
        """
        Writes data to a CSV file.

        Args:
            filename (str): Name of the CSV file.
        """
        with io.open(filename, 'w', newline='') as csvfile:
            fieldnames = ['name', 'age', 'city', 'salary']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in self.data:
                writer.writerow(row)

def main():
    num_threads = 4
    num_records = 100
    filename = 'sample_data.csv'

    # Generate random sample data
    data_generator = DataGenerator(num_threads, num_records)
    data = data_generator.generate_data()

    # Write data to CSV file
    csv_writer = CSVWriter(data)
    csv_writer.write_to_csv(filename)
    print(f"Sample data written to {filename}")

if __name__ == "__main__":
    main()
