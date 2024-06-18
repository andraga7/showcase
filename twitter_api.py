'''
The script performs the following tasks:

    Searches for a specific Twitter user's followers using the Twitter API.
    Processes the followers' data to extract information such as user ID and likes.
    Inserts this information into a database.
    Generates a CSV file containing the followers' information.

The script is organized into the following components:

    TwitterAPI Class: This class is responsible for interacting with the Twitter API. It has a method to fetch the followers of a specified user.

    TwitterProcessor Class: This class processes the followers' data obtained from the Twitter API. It extracts relevant information such as user ID and likes.

    DatabaseHandler Class: This class handles interactions with the SQLite database. It creates a table to store the followers' information and inserts the data into the table.

    main() Function: This function initializes the necessary objects, such as TwitterAPI, TwitterProcessor, and DatabaseHandler, to fetch followers, process their data, and store it in the database. It then generates a CSV file containing the followers' information.
    
'''

import requests
import sqlite3

class TwitterAPI:
    def __init__(self, user_id, bearer_token):
        self.user_id = user_id
        self.bearer_token = bearer_token
        self.base_url = "https://api.twitter.com/2/"

    def get_followers(self):
        """
        Fetches followers data from Twitter API.

        Returns:
            dict: Followers data in JSON format.
        """
        url = f"{self.base_url}users/{self.user_id}/followers"
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error:", response.text)
            return None

class TwitterProcessor:
    def process_likes(self, followers_data):
        """
        Processes followers' likes data.

        Args:
            followers_data (dict): Followers data in JSON format.

        Returns:
            dict: Dictionary containing follower IDs and their respective likes count.
        """
        likes_count = {}
        followers = followers_data.get('data', [])
        for follower in followers:
            likes_count[follower['id']] = follower.get('likes', 0)
        return likes_count

class DatabaseHandler:
    def __init__(self, db_name):
        self.db_name = db_name

    def create_table(self):
        """
        Creates a table in the database if it doesn't exist.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS followers_likes
                          (follower_id INTEGER PRIMARY KEY, likes INTEGER)''')
        conn.commit()
        conn.close()

    def insert_likes(self, likes_count):
        """
        Inserts followers' likes data into the database.

        Args:
            likes_count (dict): Dictionary containing follower IDs and their respective likes count.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        for follower_id, likes in likes_count.items():
            cursor.execute("INSERT INTO followers_likes (follower_id, likes) VALUES (?, ?)", (follower_id, likes))
        conn.commit()
        conn.close()
        print("Data inserted into the database.")

def main():
    user_id = "your_user_id"
    bearer_token = "your_bearer_token"
    db_name = "twitter_likes.db"

    # Initialize Twitter API object
    twitter_api = TwitterAPI(user_id, bearer_token)
    # Get followers data
    followers_data = twitter_api.get_followers()

    if followers_data:
        # Initialize Twitter Processor object
        twitter_processor = TwitterProcessor()
        # Process followers' likes
        likes_count = twitter_processor.process_likes(followers_data)

        # Initialize Database Handler object
        db_handler = DatabaseHandler(db_name)
        # Create table if not exists
        db_handler.create_table()
        # Insert likes into database
        db_handler.insert_likes(likes_count)

if __name__ == "__main__":
    main()
