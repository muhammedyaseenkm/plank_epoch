def partition_text(filename):
    elements = []
    with open(filename, 'r') as file:
        text = file.read()
        # Depending on your requirements, you might want to further process the text
        elements.append(text)
    return elements
