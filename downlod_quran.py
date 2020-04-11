import os
import requests

response = requests.get("http://mp3quran.net/api/get_json.php")
data = response.json()["language"]


def get_formatted_lang(i):
    # Remove the underscore, and capitalize the first letter. (Original format: _arabic)
    lang_name = data[i]["language"].replace("_", "").capitalize()
    lang_id = data[i]["id"]
    return lang_name.ljust(15, " ") + lang_id.rjust(2, "0")


def get_formatted_reciter(i):
    rec_name = reciters_data[i]["name"]
    rec_rewaya = reciters_data[i]["rewaya"]
    rec_id = reciters_data[i]["id"]
    return "{0} ({1})".format(rec_name, rec_rewaya).ljust(70, " ") + rec_id.rjust(3, "0")


# Print a formatted table of the available languages
for r in range(0, len(data), 3):
    print("{0} | {1} | {2}".format(
        get_formatted_lang(r),
        get_formatted_lang(r + 1),
        get_formatted_lang(r + 2)
    ))

lang_index = int(input("Enter language's id: ")) - 1

reciters_link = data[lang_index]["json"]
suras_link = data[lang_index]["sura_name"]

reciters_response = requests.get(reciters_link)
reciters_data = reciters_response.json()["reciters"]

suras_response = requests.get(suras_link)
suras_data = suras_response.json()["Suras_Name"]

for r in range(0, len(reciters_data) - 1, 2):
    print("{0} | {1}".format(
        get_formatted_reciter(r),
        get_formatted_reciter(r + 1)
    ))

# Convert input to int, then to string to remove any trailing zeros.
reciter_id = str(int(input("Enter reciters' id: ")))
path = input("Enter path: ")

for r in reciters_data:
    if r["id"] == reciter_id:
        r_name = "{0} ({1})".format(r["name"], r["rewaya"])
        dir_path = "{0}\\{1}".format(path, r_name)

        # Check if dir_path exist, and create it otherwise.
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)

        suras = r["suras"].split(",")
        print("({0}) {1}%".format(" " * 100, 0), end="\r", flush=False)  # Print an empty loading bar.

        for n in range(len(suras)):
            number = str(suras[n]).rjust(3, "0")
            file_name = "{0}\\{1} - {2}.mp3".format(dir_path, number,
                                                    suras_data[int(suras[n]) - 1]["name"].replace("\r\n", ""))
            if not os.path.exists(file_name) or os.stat(file_name).st_size == 0:
                f = open(file_name, "wb")
                f.write(requests.get(r["Server"] + "/" + number + ".mp3").content)
                f.close()
            print("({0}{1}) {2}%".format("-" * (n * 100 // len(suras)), " " * ((len(suras) - n) * 100 // len(suras)),
                                         n * 100 // len(suras)), end="\r", flush=False)
