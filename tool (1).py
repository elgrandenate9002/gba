import os
import json
import re

def get_title_from_filename(filename):
    filename = os.path.splitext(filename)[0]
    filename = re.sub(r'[_]', ' ', filename)
    return ' '.join([word.capitalize() for word in filename.split()])

def prompt_for_titles(folder):
    games = []
    for filename in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, filename)):
            title = get_title_from_filename(filename)
            user_title = input(f"Enter the title for {filename} [{title}]: ")
            games.append({"title": user_title if user_title else title, "file": filename})
    return games

def create_index_json(folder, games, core):
    index_data = {"games": games, "core": core}
    with open(os.path.join(folder, "index.json"), "w") as index_file:
        json.dump(index_data, index_file, indent=4)

def prompt_for_core(folder):
    core_prompt = input(f"Enter the core for {folder}: ")
    return core_prompt

library_name = input("Please enter the library name: ")

input_titles = input("Would you like to manually input the name of each game? (yes/no): ").lower() == 'yes'

folders = [f for f in os.listdir('.') if os.path.isdir(f)]

data = {
    "name": library_name,
    "consoles": []
}

for folder in folders:
    games = []
    core = prompt_for_core(folder)

    if input_titles:
        games = prompt_for_titles(folder)
    else:
        games = [{"title": get_title_from_filename(filename), "file": filename} for filename in os.listdir(folder) if os.path.isfile(os.path.join(folder, filename))]

    create_index_json(folder, games, core)
    
    data['consoles'].append({"name": folder.upper(), "folder": folder, "core": core})

with open("md.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("Library and games have been saved to md.json and index.json files respectively.")
