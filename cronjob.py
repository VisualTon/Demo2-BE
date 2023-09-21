import schedule
import asyncio
from utils.utils_api import (
    tx,
    get_txs_by_block_ids,
    get_latest_block_id,
    create_connection,
    filter_tx,
)
from utils.utils_DB import (
    add_data,
    delete_data,
    get_table_data,
    delete_duplicate_data,
    get_tx_table_rowdata_amount,
    get_min_max_amount_data,
)

prev_latest_block = 38595043
remove_from = 0
BLOCK_NUM = 5000
MAX_BLOCK_DISTANCE = 15

# base on basechain, not masterchain
# MasterChain: -1; BaseChain: 0
# (0,8000000000000000, 38350352)


async def update_database(conn):
    latest_block_id: int = await get_latest_block_id()
    print(f"latest_block_id is: {latest_block_id}")

    global prev_latest_block
    global remove_from

    if latest_block_id - prev_latest_block > MAX_BLOCK_DISTANCE:
        print("latest_block_id exceeds MAX_BLOCK_DISTANCE from prev_latest_block!!!")
        # TODO

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

    # print("start to filter the txs...")
    added_txs = filter_tx(added_txs)

    # print("start to add new txs in DB...")
    if len(added_txs) != 0:
        add_data(conn, added_txs)

    print("start to remove old txs in DB...")
    if len(removed_block_ids) != 0:
        print(f"remove block {removed_block_ids}")
        delete_data(conn, removed_block_ids)

    print("fetch out all exist DB data...")
    all_txs: [tx] = get_table_data(conn)
    # print(f"there are {len(all_txs)} txs in table.")

    tx_amount: int = get_tx_table_rowdata_amount(conn)
    print(f"tx amount: {tx_amount}")

    # min_max_tx: [tx] = get_min_max_amount_data(conn)
    # print("min tx and max tx:")
    # print(min_max_tx)

    remove_from = latest_block_id - BLOCK_NUM
    prev_latest_block = latest_block_id


def my_job():
    conn = create_connection()
    if conn:
        print("connect success")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(update_database(conn))
        conn.close()


schedule.every(5).seconds.do(my_job)

while True:
    schedule.run_pending()
    # time.sleep(1)
