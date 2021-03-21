def remove_string_first_line(string):
    split_string = string.split("\n")[1:]
    result = []
    for string in split_string:
        if string != "":
            result.append(string)

    return result
