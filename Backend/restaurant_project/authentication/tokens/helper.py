def replace_pattern(data):
    data = data.replace("+", "_")
    data = data.replace("/", "_")
    data = data.replace("=", "")

    # print(data + "\n")
    return data
