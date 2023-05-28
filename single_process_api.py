import requests
import json
from tqdm import tqdm
import time
import argparse
import os


with open("url_api.json", "r", encoding="utf-8") as f:
    url_api = json.load(f)["urls"][0]
    exec(f"API_MAIN = '{url_api}'")
    exec(f"API_GET = '{url_api}generate-text'")
    exec(f"API_POST = '{url_api}generate'")

API_MAIN = "https://srttranslategptapi--wk18k.repl.co/"
API_GET = API_MAIN + "generate-text"
API_POST = API_MAIN + "generate"
PATH_FODLER = "SRT_FILE/"


language_name = ["English", "Thai", "Japan", "Chinese", "Korean"]


headers = {"Content-Type": "application/json"}


def translat_with_gpt(prompt: str):
    response = requests.post(
        API_POST,
        data=json.dumps({"text": prompt}),
        headers=headers,
    )

    if response.status_code == 200:
        # Request was successful
        response_get = requests.get(
            API_GET,
        )
        while response_get.json()["text"] == "":
            response_get = requests.get(API_GET)
        return response_get.json()["text"]


def loop_file(path_filename: str):
    file_path = path_filename
    filename = os.path.basename(file_path)
    response_get = requests.get(API_GET)
    # loop data in file
    with open(path_filename, "r", encoding="utf-8") as file:
        # Count the number of lines in the file
        total_iterations = sum(1 for line in file)
    progress_bar = tqdm(total=total_iterations, unit="line")

    file = open(path_filename, "r", encoding="utf-8")
    with open(f"SRT_FILE/{path_filename}", "w", encoding="utf-8") as f:
        f.writelines("")
    for i, line in enumerate(file):
        list_line = []
        if line.startswith("Dialogue:"):
            list_line.append(
                translat_with_gpt(
                    f"Translate the following subtitle text into {language_name[0]}, but keep the subtitle number and timeline unchanged where the word `Dialogue: ` is inserted as before. :: \n{line}"
                )
                + "\n"
            )
            # print(list_line)
            # break
            time.sleep(1)

        else:
            list_line.append(line)
            time.sleep(0.1)
        with open(f"SRT_FILE/{filename}", "a", encoding="utf-8") as f:
            f.writelines(list_line)
        progress_bar.update(1)

    progress_bar.close()
    # with open(f"SRT_FILE/{path_filename}", "w", encoding="utf-8") as f:
    #     f.writelines(list_line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", type=str, required=True)
    args = parser.parse_args()
    path_filename = args.filename
    with open(path_filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open(f"SRT_FILE/{path_filename}", "w", encoding="utf-8") as f:
        f.writelines("")
    for i in lines:
        lst = []
        if not i.startswith("Dialogue:"):
            lst.append(i)
        with open(f"SRT_FILE/{path_filename}", "a", encoding="utf-8") as f:
            f.writelines(lst)
    loop_file(path_filename)
