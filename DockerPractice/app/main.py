import subprocess
from app.partition.pdf import partition_pdf
from app.partition.text import partition_text

def check_docker_container_existence(container_name):
    command = f"docker ps -aqf name={container_name}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return bool(result.stdout.strip())  # Check if stdout has any output

def stop_and_remove_container(container_name):
    print(f"Stopping and removing existing container '{container_name}'...")
    stop_command = f"docker stop {container_name}"
    remove_command = f"docker rm {container_name}"
    subprocess.run(stop_command, shell=True)
    subprocess.run(remove_command, shell=True)
    print(f"Existing container '{container_name}' stopped and removed successfully.")

def start_docker_container(container_name):
    print("Starting Docker container...")
    command = f"docker run -dt --name {container_name} downloads.unstructured.io/unstructured-io/unstructured:latest"
    subprocess.run(command, shell=True)
    container_id_command = f"docker ps -qf name={container_name}"
    result = subprocess.run(container_id_command, shell=True, capture_output=True, text=True)
    container_id = result.stdout.strip()
    print("Docker container started successfully.")
    return container_id

def interact_with_python(container_name):
    print("Interacting with Python inside the Docker container...")
    command = f"docker exec -it {container_name} python3"
    subprocess.run(command, shell=True)

def start_shell_session(container_id):
    try:
        # Start a shell session inside the container
        subprocess.run(["docker", "exec", "-it", container_id, "/bin/bash"], check=True)
    except subprocess.CalledProcessError as e:
        print("Error:", e)

def install_package_inside_container(container_id):
    try:
        # Install the package using pip inside the container
        subprocess.run(["docker", "exec", container_id, "pip", "install", "unstructured-inference"], check=True)
    except subprocess.CalledProcessError as e:
        print("Error:", e)

def install_packages_from_requirements(container_id, requirements_file):
    try:
        # Install packages from requirements file inside the container
        command = ["docker", "exec", container_id, "pip", "install", "-r", requirements_file]
        subprocess.run(command, check=True)
        print(f"Packages from '{requirements_file}' installed successfully inside container '{container_id}'.")
    except subprocess.CalledProcessError as e:
        print("Error:", e)

def main():
    container_name = "unstructured"

    if check_docker_container_existence(container_name):
        print(f"A Docker container with the name '{container_name}' already exists.")
        action = input("Do you want to stop and remove it before starting a new one? (yes/no): ").lower()
        if action == "yes":
            stop_and_remove_container(container_name)
        elif action == "no":
            print("Skipping container removal.")
            container_id = start_docker_container(container_name)
            install_package_inside_container(container_id)
            requirements_file = "requirements.txt"  # Path to your requirements file
            install_packages_from_requirements(container_id, requirements_file)
        else:
            print("Invalid input. Exiting script.")
            exit()

    container_id = start_docker_container(container_name)
    interact_with_python(container_name)
    start_shell_session(container_id)
    install_package_inside_container(container_id)
    requirements_file = "requirements.txt"  # Path to your requirements file
    install_packages_from_requirements(container_id, requirements_file)

    # Partitioning example documents
    pdf_elements = partition_pdf("example-docs/layout-parser-paper-fast.pdf")
    text_elements = partition_text("example-docs/fake-text.txt")

    # You can now use pdf_elements and text_elements as needed

if __name__ == "__main__":
    main()
