import requests

paylaod = {"query": "{wcBlocks: blocks(workchain: 0, page_size: 1) { seqno }}"}
r = requests.post("https://dton.io/graphql/", data=paylaod).json()
print(int(r["data"]["wcBlocks"][0]["seqno"]))
