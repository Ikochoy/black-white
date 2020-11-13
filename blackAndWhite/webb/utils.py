def get_filename(filename):
    new_filename = ""
    for char in filename:
        if char == '/':
            new_filename += "_"
        else:
            new_filename += char
    return new_filename