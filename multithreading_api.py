import requests
import json
from tqdm import tqdm
import time
import threading
import argparse
import os
import dotenv

dotenv.load_dotenv()


with open(
    os.getenv("URLS_FILE") if os.getenv("URLS_FILE") else "url_api.json",
    "r",
    encoding="utf-8",
) as f:
    url_api = json.load(f)
    global api_endpoints_all
    api_endpoints_all = []
    API_ENDPOINTS = {}
    for i, url in enumerate(url_api["urls"]):
        i += 1
        exec(f"API_MAIN_{i} = '{url}'")
        exec(f"API_GET_{i} = '{url}generate-text'")
        exec(f"API_POST_{i} = '{url}generate'")
        API_ENDPOINTS[i] = (f"{url}generate", f"{url}generate-text")
        api_endpoints_all.append(url)


PATH_FODLER = "SRT_FILE/"


language_name = ["English", "Thai", "Japan", "Chinese", "Korean"]


headers = {"Content-Type": "application/json"}


def translate_and_append(path_filename, line, progress_bar, api_point):
    if line.startswith("Dialogue:"):
        list_line = []
        translated_line = translat_with_gpt(
            f"Translate the following subtitle text into {language_name[0]}, but keep the subtitle number and timeline unchanged where the word `Dialogue: ` is inserted as before. :\n{line}",
            api_point,
        )
        if len(translated_line) > 180:
            list_line.append(line)
        else:
            list_line.append(translated_line + "\n")
        with open(f"SRT_FILE/{path_filename}", "a", encoding="utf-8") as f:
            f.writelines(list_line)
    progress_bar.update(1)


def translat_with_gpt(prompt: str, api_point: int):
    post_url, get_url = API_ENDPOINTS.get(api_point, (None, None))

    response = requests.post(
        post_url, data=json.dumps({"text": prompt}), headers=headers
    )
    if response.status_code == 200:
        while True:
            response_get = requests.get(get_url)
            if response_get.json()["text"] != "":
                return response_get.json()["text"]
            time.sleep(5)


def status_api():
    print("STATUS API : {}".format(len(api_endpoints_all)))
    for i in api_endpoints_all:
        if requests.get(i).json().get("Hello") == "GPT-PROJECT":
            print("🟢", i, "- READY !")


def recheck_api_again():
    while True:
        all_responses_valid = True
        for endpoint in api_endpoints_all:
            response = requests.get(endpoint).json()
            if response.get("Hello") != "GPT-PROJECT":
                all_responses_valid = False
                break
        if all_responses_valid:
            break


def loop_file_multithread(path_filename: str):
    global api_endpoints_all
    file_path = path_filename
    filename = os.path.basename(file_path)
    with open(path_filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open(f"SRT_FILE/{filename}", "w", encoding="utf-8") as f:
        f.writelines("")
    for i in lines:
        lst = []
        if not i.startswith("Dialogue:"):
            lst.append(i)
        with open(f"SRT_FILE/{filename}", "a", encoding="utf-8") as f:
            f.writelines(lst)

    status_api()
    # recheck_api_again()

    print("STARTING.....")
    # loop data in file
    with open(path_filename, "r", encoding="utf-8") as file:
        # Count the number of lines in the file
        total_iterations = sum(1 for line in file)
    progress_bar = tqdm(total=total_iterations, unit="line")

    file = open(path_filename, "r", encoding="utf-8")
    lines = file.readlines()
    num_iterations = len(api_endpoints_all)  # total number of iterations

    def t_1():
        for line in lines[:split_in_half]:
            translate_and_append(filename, line, progress_bar, 1)

    def t_2():
        for line in lines[split_in_half : split_in_half * 2]:
            translate_and_append(filename, line, progress_bar, 2)

    def translate_lines(i):
        return lambda: [translate_and_append(filename, line, progress_bar, i) for line in lines[split_in_half * (i-1) : split_in_half * i]]
    
    def translate_lines_end(i):
        return lambda: [translate_and_append(filename, line, progress_bar, {i}) for line in lines[split_in_half * {i} :]]
    for i in range(num_iterations):
        i += 1
        if i > 2:
            globals()[f"t_{i}"] = translate_lines(i)
        elif i == num_iterations:
            globals()[f"t_{i}"] = translate_lines_end(i)

    # Calculate split_in_half dynamically
    split_in_half = len(lines) // num_iterations
    if len(lines) % num_iterations != 0:
        split_in_half += 1

    for i in range(num_iterations):
        i += 1
        exec(f"task_{i} = threading.Thread(target=t_{i})")
    for i in range(num_iterations):
        i += 1
        exec(f"task_{i}.start()")
    for i in range(num_iterations):
        i += 1
        exec(f"task_{i}.join()")

    progress_bar.close()


if __name__ == "__main__":
    path_filename = "G:\FILE_ANIME\ORC-FOR_SUBTTITLE\File_srt\lolsf-14.ass"
    loop_file_multithread(path_filename)
