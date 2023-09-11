import schedule
import mysql.connector
import time
import requests
import asyncio
import json

PASSED_BLOCK = 10


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
        print("trying to get request from get_request()...")
        try:
            response = requests.get(block_url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            # 处理请求异常，例如连接问题
            print("Request failed:", e)
            continue
    if response.status_code == 200:
        return response
    else:
        # 处理其他响应状态码
        print("Request failed with status code:", response.status_code)


async def get_tx_info_by_tx_id(txid: str, block_id: int) -> [tx]:
    my_list: [tx] = []
    # get transaction info
    url = f"https://tonapi.io/v2/blockchain/transactions/{txid}"
    print(f"the url: {url}")
    print("--------------------------------")
    response = await get_request(url)
    # time.sleep(5)
    data = response.json()

    # TODO: too many cases that Sender_address = Receiver_address
    in_msgs = data.get("in_msg", [])
    if in_msgs:
        trans_id = data["hash"]
        sender_address = data["account"]["address"]
        receiver_address = data["in_msg"]["destination"]["address"]
        amount = int(data["in_msg"]["value"])
        confirm_time = data["utime"]
        # print("amount: %s" % amount)
        print("sender_address: %s" % sender_address)
        print("receiver_address: %s" % receiver_address)

        if amount > 0 and sender_address != receiver_address:
            in_msg_data: tx = {
                "tx_id": trans_id,
                "block_id": block_id,
                "sender_address": sender_address,
                "receiver_address": receiver_address,
                "type": "",
                "amount": amount,
                "confirm_time": confirm_time,
            }
            my_list.append(in_msg_data)
        else:
            print("can't nothing to add in my_list")

    else:
        print("doesn't get in_msg in get_tx_info()")

    # out_msgs = data.get("out_msgs", [])
    # if out_msgs:
    #     trans_id = data["hash"]
    #     sender_address = data["account"]["address"]
    #     receiver_address = data["out_msgs"][0]["destination"]["address"]
    #     amount = int(data["out_msgs"][0]["value"]) // 10**9
    #     asset = "TON"
    #     confirm_time = data["utime"]

    #     if amount > 0 and sender_address != receiver_address:
    #         out_msgs_data = {
    #             "Transaction_id": trans_id,
    #             "Sender_address": sender_address,
    #             "Receiver_address": receiver_address,
    #             "Amount": amount,
    #             "Confirm_time": confirm_time,
    #         }
    #         out_msgs_data = json.dumps(out_msgs_data, indent=2)
    #         my_list.append(out_msgs_data)
    # """
    # else:
    #     print("doesn't get out_msgs in get_tx_info()\n")
    # """
    return my_list


async def get_tx_by_block_id(block_ids: [int]) -> [tx]:
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
                print("tmp:")
                print(tmp)
                all_txs.extend(tmp)
        else:
            print(f"can't find transaction in block {id}")
            continue

    print(f"total get {len(all_txs)} in {block_ids}")
    return all_txs


async def update_database(conn):
    # TODO
    added_block_ids: [int] = [37876848, 37876849]
    removed_block_ids: [int] = [37876840, 37876841]

    # print("start to get block tx...")
    added_txs: [tx] = await get_tx_by_block_id(added_block_ids)
    # removed_txs: [tx] = await get_tx_by_block_id(removed_block_ids)

    print("start to filter the txs...")
    # TODO

    print("start to add new txs in DB...")

    print("start to remove old txs in DB...")


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
    time.sleep(1)  # 可以调整休眠时间以节省CPU资源
