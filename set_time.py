import subprocess
import requests
from dotenv import load_dotenv
load_dotenv()
import os
try:
	url = "https://timeapi.io/api/time/current/zone?timeZone=America/New_York"
	sudo_password = str(os.getenv("MIGHTY_TOKEN")) # You aint getting my sudo password
	response = requests.get(url, timeout=10)
	response.raise_for_status()

	data = response.json()
	new_time = data["dateTime"].split(".")[0]

	print("Internet time:", new_time)

	subprocess.run(
	    ["sudo", "-S", "date", "-s", new_time],
	    input=sudo_password + "\n",
	    text=True,
	    check=True,
	    stdout=subprocess.PIPE
	)
except exception as e:
	print('CRITICAL ERROR: UNABLE TO GET TIME')
	print(e)
