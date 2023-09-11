import asyncio
import requests


async def get_request(block_url):
    response = None
    while response is None or response.status_code != 200:
        # print("trying to get request from get_request()...")
        try:
            response = requests.get(block_url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("Request failed:", e)
            continue
    if response.status_code == 200:
        return response
    else:
        print("Request failed with status code:", response.status_code)


async def main():
    res = await get_request(f"https://tonapi.io/v2/blockchain/masterchain-head")
    print(int(res.json()["seqno"]))


if __name__ == "__main__":
    asyncio.run(main())
