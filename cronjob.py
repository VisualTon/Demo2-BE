import schedule
import mysql.connector
import time
import requests
import asyncio
import json

prev_latest_block = 32616077
remove_from = 0
BLOCK_NUM = 10


class tx:
    tx_id: str
    block_id: int
    sender_address: str
    receiver_address: str
    type: str
    amount: int
    confirm_time: int


# 创建MySQL连接
def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",  # 如果 MySQL 服务器在本地，使用 "localhost"；如果在不同的主机上，使用该主机的 IP 地址
            port=3390,  # 映射的本地端口
            user="root",  # MySQL 用户名
            password="0505jo",  # MySQL 密码
            database="visualtondb",  # 要连接的数据库名称
        )
        return conn
    except Exception as e:
        print(f"Error connecting to MySQL: {str(e)}")
        return None


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


async def get_tx_info_by_tx_id(txid: str, block_id: int) -> tx | None:
    # get transaction info
    url = f"https://tonapi.io/v2/blockchain/transactions/{txid}"
    response = await get_request(url)
    # time.sleep(5)
    data = response.json()

    if "in_msg" in data:
        in_msg = data["in_msg"]
        if "source" in in_msg and "destination" in in_msg and in_msg["value"] > 0:
            res: tx = {
                "tx_id": data["hash"],
                "block_id": block_id,
                "sender_address": in_msg["source"]["address"],
                "receiver_address": in_msg["destination"]["address"],
                "type": "",
                "amount": in_msg["value"],
                "confirm_time": data["utime"],
            }
            return res

    if "out_msgs" in data:
        out_msgs = data["out_msgs"][0]
        if "source" in out_msgs and "destination" in out_msgs and out_msgs["value"] > 0:
            res: tx = {
                "tx_id": data["hash"],
                "block_id": block_id,
                "sender_address": out_msgs["source"]["address"],
                "receiver_address": out_msgs["destination"]["address"],
                "type": "",
                "amount": out_msgs["value"],
                "confirm_time": data["utime"],
            }
            return res

    print(f"can't analyze tx {txid} !")
    print(data["in_msg"])
    print(data["out_msgs"])
    return None


async def get_txs_by_block_ids(block_ids: [int]) -> [tx]:
    all_txs: [tx] = []

    for id in block_ids:
        print(f"start to get block {id} tx...")
        block_url = f"https://tonapi.io/v2/blockchain/blocks/(0,8000000000000000,{id})/transactions"
        response = await get_request(block_url)
        block_data = response.json()

        if "transactions" in block_data:
            for transaction in block_data["transactions"]:
                hash_value: str = transaction["hash"]
                tmp = await get_tx_info_by_tx_id(hash_value, id)
                if tmp is not None:
                    all_txs.extend(tmp)
        else:
            print(f"can't find transaction in block {id}")
            continue

    print(f"total get {len(all_txs)} in {block_ids}")
    return all_txs


async def get_latest_block_id(conn) -> int:
    res = await get_request(f"https://tonapi.io/v2/blockchain/masterchain-head")
    return int(res.json()["seqno"])


async def update_database(conn):
    latest_block_id: int = await get_latest_block_id(conn)
    print(f"latest_block_id is: {latest_block_id}")

    global prev_latest_block
    global remove_from

    added_block_ids: [int] = list(range(prev_latest_block, latest_block_id))
    removed_block_ids: [int] = []
    if remove_from != 0:
        removed_block_ids = list(
            range(
                remove_from,
                latest_block_id - BLOCK_NUM,
            )
        )
    else:
        removed_block_ids = list(
            range(
                prev_latest_block,
                latest_block_id - BLOCK_NUM,
            )
        )

    # print("start to get block tx...")
    added_txs: [tx] = await get_txs_by_block_ids(added_block_ids)
    removed_txs: [tx] = await get_txs_by_block_ids(removed_block_ids)

    print("start to filter the txs...")
    # TODO

    print("start to add new txs in DB...")
    # TODO

    print("start to remove old txs in DB...")
    # TODO

    remove_from = latest_block_id - BLOCK_NUM
    prev_latest_block = latest_block_id


def my_job():
    conn = create_connection()
    if conn:
        print("connect success")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(update_database(conn))
        conn.close()


# schedule.every().minute.do(my_job)
schedule.every(10).seconds.do(my_job)

while True:
    schedule.run_pending()
    time.sleep(1)
