import schedule
import time


# 定义要执行的任务函数
def my_job():
    print("Cron job is running!")


# 创建一个定期执行的任务，每小时执行一次
schedule.every().minute.do(my_job)

# 主循环，持续执行计划任务
while True:
    schedule.run_pending()
    time.sleep(1)  # 可以调整休眠时间以节省CPU资源
