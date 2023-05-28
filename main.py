from multithreading_api import *
from single_process_api import *
import os


def main(path_filename, mode):
    print()
    print("Starting...")
    print()
    if mode == "s":
        loop_file(path_filename)
    elif mode == "m":
        loop_file_multithread(path_filename)


def remove_whitespace(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for i, line in enumerate(lines):
        if i > 19:
            new_line = line.strip()  # remove leading/trailing whitespaces
        else:
            new_line = line
        if new_line:  # only add non-empty lines
            new_lines.append(new_line)

    # overwrite the original file with the cleaned up subtitles
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines))


def recheck_fix_error_sub(path_filename: str):
    with open(path_filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
        lst = []
        for i in lines:
            if i.startswith("Dialogue:") and i[49] != ",":
                string_list = list(i)
                string_list.insert(49, ",")
                i = modified_string = "".join(string_list)
                lst.append(i + "\n")
            else:
                lst.append(i)
    with open(path_filename, "w", encoding="utf-8") as f:
        f.writelines(lst)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", type=str, required=True)
    parser.add_argument(
        "--mode", type=str, default="s"
    )  # s : single thread, m : multi thread
    args = parser.parse_args()
    path_filename = args.filename
    mode = args.mode
    for filename in os.listdir("SRT_FILE"):
        file_path = os.path.join("SRT_FILE", filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    main(path_filename, mode)

    remove_whitespace("SRT_FILE" + "/" + os.path.basename(args.filename))
    recheck_fix_error_sub("SRT_FILE" + "/" + os.path.basename(args.filename))
    print()
    print(
        "Done! Check the result in : SRT_FILE/{}".format(
            os.path.basename(args.filename)
        )
    )
    print()
