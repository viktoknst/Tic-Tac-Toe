This is a TicTacToe game created in python which has two gamemodes - multiplayer and singleplayer.

1. Features:

 - The user can play against an AI bot
 - The user can play against a friend
 - The user can chose how big the grid should be

MongoDB Atlas plays a crucial role as the central database that stores and synchronizes game moves between players in multiplayer mode

2. Installation:
 - Clone the git repo
   
 - Poetry:
   Install poetry using the following guide: ``https://python-poetry.org/docs/``
   After the installation is complete run:
   ``poetry shell``
   in the terminal and after that is complete run main.py in the src folder
   
 - Tkinter:
   To install tkinter just type in this command:
   ``sudo apt install python3-tk``

3. MongoDB Atlas:
   The project uses MongoDB Atlas as the database. To start it successfully sign up for their web site at ``https://www.mongodb.com/cloud/atlas/register``
   and follow the steps for creating a cluster, database and collection. After that create a .env file in you Tic_tac_toe folder that contains the specific url you get from the cluster and add your      connection string into your application code. Name the url in your .env file ``MONGODB_URI`` as this is the name used in the game class. Also the database's name is "tic_tac_toe_db" and the name      of the collection is "game_state"

        ``MONGODB_URI = os.getenv("MONGODB_URI")
          self.mongo_client = MongoClient(MONGODB_URI)
          self.db = self.mongo_client["tic_tac_toe_db"]
          self.collection = self.db["game_state"]``

4. After these steps the game should be operational. Enjoy!
