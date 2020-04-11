import os
import requests
import sys

print("Loading languages...\n")

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

print("\nNOTE: The different languages are for the names of downloaded files only,\n"
      "the recitation itself will be in Arabic language.")

lang_index = int(input("Enter language's id: ")) - 1

if not (0 <= lang_index < len(data)):
    print("{0} is not a valid language id.".format(lang_index + 1))
    sys.exit()

print("Loading reciters...\n")

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

reciter_found = False

for r in reciters_data:
    if r["id"] == reciter_id:
        reciter_found = True

        r_name = "{0} ({1})".format(r["name"], r["rewaya"])
        suras = r["suras"].split(",")
        answer = input("{0} Suras available for {1}. Continue? [Y/N]\n".format(len(suras), r_name))
        if answer.lower() == "n":
            sys.exit()
        elif not answer.lower() == "y":
            print("Your answer is not valid. Exiting...")
            sys.exit()

        path = input("Enter path: ")
        dir_path = os.path.join(path, r_name)

        # Check if dir_path exist, and create it otherwise.
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)

        for n in range(len(suras)):
            sura_number = str(suras[n]).rjust(3, "0")
            sura_name = suras_data[int(suras[n]) - 1]["name"].replace("\r\n", "")
            name = "{0} - {1}.mp3".format(sura_number, sura_name)
            file_name = os.path.join(dir_path, name)

            # Check if Sura has already been downloaded, and download it otherwise.
            if not os.path.exists(file_name) or os.stat(file_name).st_size == 0:
                print("Downloading {0}...".format(name))
                f = open(file_name, "wb")
                f.write(requests.get(r["Server"] + "/" + sura_number + ".mp3").content)
                f.close()

        print("Finished Downloading.")

if not reciter_found:
    print("{0} is not a valid reciter id.".format(reciter_id))
