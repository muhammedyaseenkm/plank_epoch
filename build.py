import os
import subprocess
import shutil
import zipfile

def build_app():
    print("Building the application...")
    
    # Navigate to the project directory
    project_dir = os.path.abspath(os.path.dirname(__file__))
    print("Project directory:", project_dir)
    os.chdir(project_dir)

    # Uninstall the 'typing' package
    print("Uninstalling the 'typing' package...")
    subprocess.run([r"C:\Python\python.exe", "-m", "pip", "uninstall", "typing"])

    # Install Flask dependencies
    print("Installing Flask dependencies...")
    subprocess.run(['pip', 'install', '-r', 'flask-backend/requirements.txt'])

    # Build React frontend
    print("Building React frontend...")
    npm_path = shutil.which('npm')
    if npm_path:
        react_app_dir = os.path.join(project_dir, 'react-frontend', 'my-react-app')
        print("React frontend directory:", react_app_dir)
        os.chdir(react_app_dir)
        os.system('npm install')
        os.system('npm run build')
        os.chdir(project_dir)  # Change back to the project directory
    else:
        print("npm not found. Make sure Node.js is installed and added to the system PATH.")

    # Check if 'dist' directory exists within the project directory
    dist_dir = os.path.join(project_dir, 'dist')
    print("Checking for 'dist' directory at:", dist_dir)
    if os.path.exists(dist_dir):
        print("'dist' directory found.")
        # Package Flask backend using PyInstaller
        print("Packaging Flask backend...")
        subprocess.run(['pyinstaller', '--onefile', 'flask-backend/app.py', '--distpath', dist_dir])

        # Package Electron app using PyInstaller
        print("Packaging Electron app...")
        subprocess.run(['pyinstaller', '--onefile', 'electron-app/main.js', '--distpath', dist_dir])

        # Create zip file containing entire project
        print("Creating zip archive of the project...")
        shutil.make_archive(os.path.join(project_dir, 'your_app'), 'zip', dist_dir)

        # Clean up temporary build directory
        print("Cleaning up temporary build directory...")
        shutil.rmtree(dist_dir)
    else:
        print("'dist' directory not found within the project directory. Please check if the build process completed successfully.")
        print("Contents of the project directory:")
        for item in os.listdir(project_dir):
            print(item)

if __name__ == "__main__":
    build_app()
    