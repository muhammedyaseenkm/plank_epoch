import os
import requests
#os.makedirs('raw_pdf_folder', exist_ok=True)

def download_data(url, output_path, file_name):
    response = requests.get(url)
    if response.status_code == 200:
        full_path = os.path.join(output_path, file_name)
        with open(full_path, 'wb') as file:
            file.write(response.content)
        print(f'The data from {url} was successfully downloaded to {full_path}')
    else:
        print(f'Failed to download data from {url}. Status code: {response.status_code}')

# Example usage:
url = 'https://assets.ey.com/content/dam/ey-sites/ey-com/en_gl/topics/insurance/insurance-pdfs/ey-2021-global-insurance-outlook.pdf'
url = 'https://media.geeksforgeeks.org/wp-content/uploads/20240226121023/GFG.pdf'
file_name = 'research_Paper_1.pdf'
output_path = os.path.join(os.path.curdir)
download_data(url, output_path, file_name)

