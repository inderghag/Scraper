import os
import json


#If file exists, load it and join it with incoming array and
#then dump back into file, else create file and dump array
def write_file(item_array, file_name):

    if os.path.exists(file_name):
        print("In if")
        with open(file_name) as file:
            load_data = json.load(file)
            file.close()

        full_list = load_data + item_array

        with open(file_name, "w") as file:
            json.dump(full_list, file, indent=2)
            file.close()
    else:
        print("In else")
        with open(file_name, "w") as file:
            json.dump(item_array, file, indent=2)
            file.close()

