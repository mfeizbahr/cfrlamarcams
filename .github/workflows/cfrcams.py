import requests
import json
from datetime import datetime
import ftplib

# List of BASE_URLs
BASE_URLS = [
 "https://flashflood.info:8282/352753090666023",
"https://flashflood.info:8282/352753092238656",
"https://flashflood.info:8282/352753090707306",
"https://flashflood.info:8282/352753091900173",
"https://flashflood.info:8282/352753092209608",
"https://flashflood.info:8282/352753092187234",
"https://flashflood.info:8282/352753092228871",
"https://flashflood.info:8282/352753093314530",
"https://flashflood.info:8282/352753092208295",
"https://flashflood.info:8282/356211690491942",
"https://flashflood.info:8282/352753092288131",
"https://flashflood.info:8282/352753092009768",
"https://flashflood.info:8282/352753092010261",
"https://flashflood.info:8282/352753090912385",
"https://flashflood.info:8282/352753092214897",
"https://flashflood.info:8282/352753092272424",
"https://flashflood.info:8282/352753092228947",
"https://flashflood.info:8282/352753092224631",
"https://flashflood.info:8282/355523767551510",
"https://flashflood.info:8282/352753090725365",
"https://flashflood.info:8282/355523767566690",
"https://flashflood.info:8282/356726104221007",
"https://flashflood.info:8282/355523767560420",
"https://flashflood.info:8282/355523767560420",
"https://flashflood.info:8282/352596142406744",
"https://flashflood.info:8282/355523767513213",
"https://flashflood.info:8282/356211690491850",
"https://flashflood.info:8282/355523769791460",
"https://flashflood.info:8282/352596143208784",
"https://flashflood.info:8282/355523768232656",
"https://flashflood.info:8282/356726104297130",
"https://flashflood.info:8282/355523767513122",
"https://flashflood.info:8282/355523767513122",
"https://flashflood.info:8282/355523767566690",
"https://flashflood.info:8282/355523767566690",
"https://flashflood.info:8282/355523767566690",
"https://flashflood.info:8282/352753091994234",
"https://flashflood.info:8282/352753092208477",
"https://flashflood.info:8282/356726104568571",
"https://flashflood.info:8282/356726104209879",
"https://flashflood.info:8282/355523767524228",
"https://flashflood.info:8282/355523767524228",
"https://flashflood.info:8282/352753092238631",
"https://flashflood.info:8282/352753090915511",
"https://flashflood.info:8282/352753090702927",
"https://flashflood.info:8282/352596142409045",
"https://flashflood.info:8282/352596145506615",
"https://flashflood.info:8282/352596146925475",
"https://flashflood.info:8282/352596146925475",
"https://flashflood.info:8282/352753092228988",
"https://flashflood.info:8282/352753092228988",
"https://flashflood.info:8282/352753092207768",
"https://flashflood.info:8282/352753092306842",
"https://flashflood.info:8282/352596144106516"
]

# FTP credentials and server information
FTP_HOST = "ftp.procedia.org"
FTP_USERNAME = "cfrcams@cfrlamar.com"
FTP_PASSWORD = "g#Pvu)&{;Buz"

# Output file name
output_file_name = datetime.now().strftime("%Y-%m-%d") + ".txt"

# List to accumulate output
all_outputs = []

# Function to generate output text
def generate_output_text(imei, code, date_str, circle_color):
    return f"IMEI: {imei}, Code: {code}, Last date: {date_str}, Color: {circle_color}"

# Iterate over BASE_URLs
for BASE_URL in BASE_URLS:
    JSON_URL = f"{BASE_URL}/all"

    try:
        # Fetch the JSON data
        with requests.get(JSON_URL, verify=False) as response:
            response.raise_for_status()
            data = response.json()

            # Extract the last file name
            last_file_name = data['files'][0][-1]
            # Convert list element to string
            last_file_name = str(last_file_name)
            # Replace '[' and ']' characters
            last_file_name = last_file_name.replace('[', '').replace(']', '')
            last_file_name = last_file_name.replace("'", "")
            last_file_name = last_file_name.split(',')[-1]

            # Get necessary information from the file name
            imei, code, date_str = last_file_name.split('_')[:3]

            # Calculate date difference
            image_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            date_difference = (datetime.now().date() - image_date).days

            # Choose circle color based on date difference
            circle_color = 'red' if date_difference > 1 else 'green'

            # Generate output text
            output_text = generate_output_text(imei, code, date_str, circle_color)

            # Append output to the list
            all_outputs.append(output_text)

    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Join all outputs into a single string
output_content = '\n'.join(all_outputs)

# Upload output to FTP server
with ftplib.FTP(FTP_HOST) as ftp:
    ftp.login(FTP_USERNAME, FTP_PASSWORD)
    with open(output_file_name, "w") as file:
        file.write(output_content)
    with open(output_file_name, "rb") as file:
        ftp.storbinary(f"STOR {output_file_name}", file)

print("Output file uploaded to FTP server successfully.")
