import requests, os

response = requests.get("http://mp3quran.net/api/get_json.php")
data = response.json()["language"]

for i in range(0, len(data), 3):
    print("{0}{1} | {2}{3} | {4}{5}".format(
        data[i]["language"].replace("_", "").ljust(15, " "), data[i]["id"].rjust(2, "0"), 
        data[i+1]["language"].replace("_", "").ljust(15, " "), data[i+1]["id"].rjust(2, "0"), 
        data[i+2]["language"].replace("_", "").ljust(15, " "), data[i+2]["id"].rjust(2, "0")))

lang_id = int(input("Enter language's id: ")) - 1

lang_url = data[lang_id]["json"] 
lang_suras = data[lang_id]["sura_name"]
lang_response = requests.get(lang_url)
lang_data = lang_response.json()["reciters"]
lang_sura_response = requests.get(lang_suras)
lang_suras_name = lang_sura_response.json()["Suras_Name"]

for i in range(0, len(lang_data) - 1, 2):
    print("{0}{1} | {2}{3}".format(
        "{0} ({1})".format(lang_data[i]["name"], lang_data[i]["rewaya"]).ljust(70, " "), lang_data[i]["id"].rjust(3, "0"), 
        "{0} ({1})".format(lang_data[i+1]["name"], lang_data[i+1]["rewaya"]).ljust(70, " "), lang_data[i+1]["id"].rjust(3, "0")))

id = input("Enter reciters' id: ")
path = input("Enter path: ")

for i in lang_data:
    if(i["id"] == id):
        r_name = "{0} ({1}) [{2}]".format(i["name"], i["rewaya"], data[lang_id]["language"].replace("_", ""))
        dir_path = "{0}\\{1}".format(path, r_name)
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
        suras = i["suras"].split(",")
        print("({0}) {1}%".format(" " * 100, 0), end="\r", flush=False)
        for n in range(len(suras)):
            name = str(suras[n]).rjust(3, "0")
            file_name = "{0}\\{1} - {2}.mp3".format(dir_path, name, lang_suras_name[int(suras[n]) - 1]["name"].replace("\r\n", ""))
            if not os.path.exists(file_name) or os.stat(file_name).st_size == 0:
                f = open(file_name, "wb")
                f.write(requests.get(i["Server"] + "/" + name + ".mp3").content)
                f.close
            print("({0}{1}) {2}%".format("-" * (n * 100 // len(suras)), " " * ((len(suras) - n) * 100 // len(suras)), n * 100 // len(suras)), end="\r", flush=False)
            