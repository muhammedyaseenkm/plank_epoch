import asyncio
import os
from dotenv import load_dotenv
from docker_manager import DockerManager
from database_manager import DatabaseManager

# Load environment variables from .env file
load_dotenv()


python_commands_file = os.getenv('PYTHON_COMMANDS_FILE')
if python_commands_file:
    try:
        python_commands = __import__(python_commands_file[:-3])  # Remove the ".py" extension
    except ImportError:
        print(f"Error: Unable to import {python_commands_file}")
        exit(1)
else:
    print("Error: PYTHON_COMMANDS_FILE environment variable is not set")
    exit(1)


async def main():
    # Initialize Docker manager
    docker_manager = DockerManager()

    # Pull Docker image
    docker_manager.pull_image()

    # Create and start Docker container
    container_id = docker_manager.create_container()

    # Execute commands in container
#    docker_manager.execute_commands_in_container()
    await docker_manager.execute_commands_in_container()


    # Initialize Database manager
    db_manager = DatabaseManager()

    # Connect to database
    db_manager.connect()

    # Insert data into database
    db_manager.insert_data()

    # Close database connection
    db_manager.close_connection()

if __name__ == "__main__":
    asyncio.run(main())
