import subprocess

def execute():
    python_commands = [
        'from unstructured.partition.pdf import partition_pdf',
        'pdf_elements = partition_pdf(filename="example-docs/layout-parser-paper-fast.pdf")',
        'from unstructured.partition.text import partition_text',
        'text_elements = partition_text(filename="example-docs/fake-text.txt")',
        'print(pdf_elements)',
        'print(text_elements)'
    ]
    return python_commands

def check_container_exists(container_name):
    # Check if container with the same name already exists
    result = subprocess.run(['docker', 'ps', '-a', '--filter', f'name={container_name}', '--format', '{{.Names}}'], capture_output=True)
    existing_containers = result.stdout.decode().splitlines()
    return container_name in existing_containers

def pull_docker_image(image_name):
    subprocess.run(['docker', 'pull', image_name], check=True)

def create_container(image_name, container_name):
    if check_container_exists(container_name):
        print("Container already exists. Skipping container creation.")
        return
    else:
        subprocess.run(['docker', 'run', '-dt', '--name', container_name, image_name], check=True)
        print(f"Successfully created and started container: {container_name}")

def exec_shell_in_container(container_name):
    subprocess.run(['docker', 'exec', '-it', container_name, 'bash'], check=True)


def execute_python_commands(container_name, python_commands):
    for command in python_commands:
        subprocess.run(['docker', 'exec', '-it', container_name, 'python3', '-c', command], check=True)


def main():
    # Define Docker image and container names
    image_name = 'downloads.unstructured.io/unstructured-io/unstructured:latest'
    container_name = 'unstructured'

    # Pull the Docker image
    pull_docker_image(image_name)

    # Create and start the Docker container
    create_container(image_name, container_name)

    # Access the container's shell
    exec_shell_in_container(container_name)

    # Get Python commands from app.py
    python_commands = execute()

    # Execute Python commands inside the container
    execute_python_commands(container_name, python_commands)

if __name__ == "__main__":
    main()
