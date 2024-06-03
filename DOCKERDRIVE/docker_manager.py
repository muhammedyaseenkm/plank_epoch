import subprocess
import logging
import asyncio
import os

class DockerManager:
    def __init__(self):
        self.image_name = os.getenv("DOCKER_IMAGE_NAME")
        self.container_name = os.getenv("DOCKER_CONTAINER_NAME")
        self.python_commands_file = os.getenv("PYTHON_COMMANDS_FILE")

    def pull_image(self):
        # Pull Docker image
        try:
            subprocess.run(['docker', 'pull', self.image_name], check=True)
            logging.info(f"Successfully pulled Docker image: {self.image_name}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to pull Docker image: {self.image_name}. Command returned non-zero exit status {e.returncode}.")
    
    def check_container_exists(self):
        # Check if container with the same name already exists
        result = subprocess.run(['docker', 'ps', '-a', '--filter', f'name={self.container_name}', '--format', '{{.Names}}'], capture_output=True)
        existing_containers = result.stdout.decode().splitlines()
        return self.container_name in existing_containers

    def create_container(self):
        if self.check_container_exists():
            print("Container already exists. Skipping container creation.")
            return
        
        # Create and start Docker container
        subprocess.run(['docker', 'run', '-dt', '--name', self.container_name, self.image_name], check=True)
        logging.info(f"Successfully created and started container: {self.container_name}")
        return self.container_name
        
    """
    async def execute_commands_in_container(self):
        # Execute commands in container
        proc = await asyncio.create_subprocess_shell(f'docker exec -it {self.container_name} python3 -c "import python_commands; python_commands.execute()"')
        await proc.communicate()
        logging.info(f"Executed commands in container: {self.container_name}")
    """
    async def execute_commands_in_container(self):
    # Execute commands in container
        proc = await asyncio.create_subprocess_shell(f'docker exec -it {self.container_name} python3 -c "import {self.python_commands_file[:-3]}; results = {self.python_commands_file[:-3]}.execute(); print(results)"')
        await proc.communicate()
        logging.info(f"Executed commands in container: {self.container_name}")
