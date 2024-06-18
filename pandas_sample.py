'''
The code revolves around two main classes: DataFrameProcessor and SalaryProcessor, along with a supporting class PopulationProcessor. These classes offer functionalities to process and manipulate pandas DataFrames.

    DataFrameProcessor Class: This class provides generic DataFrame processing methods such as sorting, filtering, calculating statistics, adding and dropping columns.

    SalaryProcessor Class (Inherits DataFrameProcessor): This class extends the functionality of DataFrameProcessor with specific methods related to salary data processing, like calculating average salary by city, adding a bonus column, and calculating total income.

    PopulationProcessor Class: This class deals with population-related data. It includes methods to merge DataFrames and save DataFrame contents to a CSV file.

The script generates sample data, creates an instance of SalaryProcessor to process the data, and demonstrates various operations such as sorting, filtering, calculating statistics, adding columns, dropping columns, and merging DataFrames. Finally, it saves the processed DataFrame to a CSV file.

'''

import pandas as pd
import numpy as np

class DataFrameProcessor:
    """
    Class for processing pandas DataFrames.
    """
    def __init__(self, df):
        """
        Initializes the DataFrameProcessor object.

        Args:
            df (DataFrame): Input DataFrame.
        """
        self.df = df
    
    def sort_by_column(self, column, ascending=True):
        """
        Sorts the DataFrame by a specified column.

        Args:
            column (str): Name of the column to sort by.
            ascending (bool, optional): Whether to sort in ascending order. Defaults to True.

        Returns:
            DataFrame: Sorted DataFrame.
        """
        return self.df.sort_values(by=column, ascending=ascending)
    
    def filter_by_column(self, column, value):
        """
        Filters the DataFrame by a specified column and value.

        Args:
            column (str): Name of the column to filter by.
            value: Value to filter on.

        Returns:
            DataFrame: Filtered DataFrame.
        """
        return self.df[self.df[column] == value]
    
    def calculate_statistics(self):
        """
        Calculates statistics for the DataFrame.

        Returns:
            DataFrame: DataFrame containing statistics.
        """
        return self.df.describe()
    
    def add_column(self, name, values):
        """
        Adds a new column to the DataFrame.

        Args:
            name (str): Name of the new column.
            values: Values to populate the new column with.

        Returns:
            DataFrame: DataFrame with the new column added.
        """
        self.df[name] = values
        return self.df
    
    def drop_column(self, column):
        """
        Drops a column from the DataFrame.

        Args:
            column (str): Name of the column to drop.

        Returns:
            DataFrame: DataFrame with the specified column dropped.
        """
        return self.df.drop(columns=[column])

class SalaryProcessor(DataFrameProcessor):
    """
    Class for processing salary-related data.
    """
    def calculate_avg_salary_by_city(self):
        """
        Calculates the average salary by city.

        Returns:
            Series: Series containing average salary by city.
        """
        return self.df.groupby('city')['salary'].mean()
    
    def add_bonus_column(self):
        """
        Adds a bonus column to the DataFrame with random values.

        Returns:
            DataFrame: DataFrame with the bonus column added.
        """
        self.df['bonus'] = np.random.randint(500, 2000, size=len(self.df))
        return self.df
    
    def calculate_total_income(self):
        """
        Calculates total income by adding salary and bonus.

        Returns:
            DataFrame: DataFrame with total income column added.
        """
        self.df['total_income'] = self.df['salary'] + self.df['bonus']
        return self.df

class PopulationProcessor:
    """
    Class for processing population-related data.
    """
    def __init__(self, df):
        """
        Initializes the PopulationProcessor object.

        Args:
            df (DataFrame): Input DataFrame.
        """
        self.df = df
    
    def merge_dataframes(self, other_df, on_column):
        """
        Merges the DataFrame with another DataFrame on a specified column.

        Args:
            other_df (DataFrame): DataFrame to merge with.
            on_column (str): Name of the column to merge on.

        Returns:
            DataFrame: Merged DataFrame.
        """
        return pd.merge(self.df, other_df, on=on_column)
    
    def save_to_csv(self, filename):
        """
        Saves the DataFrame to a CSV file.

        Args:
            filename (str): Name of the CSV file.
        """
        self.df.to_csv(filename, index=False)
        print("DataFrame saved to '{}'".format(filename))

# Generate sample data
data = {
    'name': ['Person{}'.format(i) for i in range(1, 11)],
    'age': np.random.randint(20, 40, size=10),
    'city': ['City{}'.format(np.random.randint(1, 6)) for _ in range(10)],
    'salary': np.random.randint(30000, 80000, size=10)
}

sample_df = pd.DataFrame(data)

# Create SalaryProcessor instance
salary_processor = SalaryProcessor(sample_df)

# Sort by age
sorted_df = salary_processor.sort_by_column('age', ascending=False)

# Filter by age
filtered_df = salary_processor.filter_by_column('age', 25)

# Calculate statistics
stats = salary_processor.calculate_statistics()

# Add bonus column
df_with_bonus = salary_processor.add_bonus_column()

# Calculate total income
df_with_income = salary_processor.calculate_total_income()

# Drop a column
df_dropped_column = salary_processor.drop_column('bonus')

# Merge with another DataFrame
data2 = {
    'city': ['City1', 'City2', 'City3', 'City4', 'City5'],
    'population_millions': [8.4, 3.9, 2.7, 2.3, 0.47]
}
df2 = pd.DataFrame(data2)

population_processor = PopulationProcessor
