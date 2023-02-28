import queue
import threading
from global_msg import balance, queue_msg

# 初始余额为0
# 创建队列对象
q = queue.Queue()

# 存款线程
def deposit():
    global balance
    amount = 100 # 假设每次存100元
    balance += amount
    queue_msg.put(amount)
    print(f"存入 {amount} 后，余额为 {balance}")

# 取款线程
def withdraw():
    global balance
    amount = queue_msg.get()
    balance -= amount
    print(f"取出 {amount} 后，余额为 {balance}")

# 创建线程对象
deposit_thread = threading.Thread(target=deposit)
withdraw_thread = threading.Thread(target=withdraw)

# 启动线程
deposit_thread.start()
withdraw_thread.start()

# 等待线程执行完毕
deposit_thread.join()
withdraw_thread.join()
