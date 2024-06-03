import subprocess
from contextlib import ExitStack
from unstructured.partition.api import partition_multiple_via_api

def execute_pdf(filename, output_file):
    # Define the command for PDF partitioning
    command = f"docker exec -it unstructured python3 -c \"import unstructured.partition.pdf as pdf; elements_pdf = pdf.partition_pdf(filename='{filename}'); print(elements_pdf)\""

    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)

        if result.returncode == 0:
            print("PDF partitioning executed successfully.")
        else:
            print(f"PDF partitioning failed with return code: {result.returncode}")

        with open(output_file, "w") as f:
            f.write(result.stdout)

    except subprocess.CalledProcessError as e:
        print("PDF partitioning failed:", e)
    except Exception as e:
        print("An error occurred during PDF partitioning:", e)


def execute_text(filename, output_file):
    # Define the command for text partitioning
    command = f"docker exec -it unstructured python3 -c \"import unstructured.partition.text as text; elements_text = text.partition_text(filename='{filename}'); print(elements_text)\""

    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)

        if result.returncode == 0:
            print("Text partitioning executed successfully.")
        else:
            print(f"Text partitioning failed with return code: {result.returncode}")

        with open(output_file, "w") as f:
            f.write(result.stdout)

    except subprocess.CalledProcessError as e:
        print("Text partitioning failed:", e)
    except Exception as e:
        print("An error occurred during text partitioning:", e)


def execute_image(filename, output_file, languages=None):
    # Define the command for image partitioning
    if languages:
        language_str = ",".join(languages)
        command = f"docker exec -it unstructured python3 -c \"import unstructured.partition.image as image; elements_image = image.partition_image(filename='{filename}', languages=['{language_str}']); print(elements_image)\""
    else:
        command = f"docker exec -it unstructured python3 -c \"import unstructured.partition.image as image; elements_image = image.partition_image(filename='{filename}'); print(elements_image)\""

    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)

        if result.returncode == 0:
            print("Image partitioning executed successfully.")
        else:
            print(f"Image partitioning failed with return code: {result.returncode}")

        with open(output_file, "w") as f:
            f.write(result.stdout)

    except subprocess.CalledProcessError as e:
        print("Image partitioning failed:", e)
    except Exception as e:
        print("An error occurred during image partitioning:", e)


def execute_api(filenames, output_file=None, metadata_filenames=None):
    try:
        if output_file:
            with open(output_file, "w") as f:
                with ExitStack() as stack:
                    files = [stack.enter_context(open(filename, "rb")) for filename in filenames]
                    documents = partition_multiple_via_api(files=files, metadata_filenames=metadata_filenames)
                    f.write(str(documents))
        else:
            with ExitStack() as stack:
                files = [stack.enter_context(open(filename, "rb")) for filename in filenames]
                documents = partition_multiple_via_api(files=files, metadata_filenames=metadata_filenames)
                print(documents)

    except Exception as e:
        print("An error occurred during API partitioning:", e)



