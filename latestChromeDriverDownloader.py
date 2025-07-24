import requests
import re

if __name__ == "__main__":
    response = requests.get(
        "https://googlechromelabs.github.io/chrome-for-testing/"
    ).text
    print(f"response:{response}")
    # stable > div > table > tbody > tr:nth-child(10) > td:nth-child(3) > code
    # //*[@id="stable"]/div/table/tbody/tr[10]/td[1]/code
    pattern = r"<code>(https://[^>]*chromedriver-win64.zip)"

    match = re.search(pattern, response)
    print("")
    if match:
        print(f"match:{match}")
        print(match.group(0))
        print(match.group(1))
    local_filename = match.group(1)
    with requests.get(local_filename, stream=True) as response:
        response.raise_for_status()  # Check for request errors
        with open("chromedriver-win64.zip", "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive chunks
                    f.write(chunk)

    print(f"Downloaded file saved as {local_filename}")
