import queue
import time

def send_data(data_queue):
    data_queue.put('1Hello')

if __name__ == "__main__":
    external_data_queue = queue.Queue()
    send_data(external_data_queue)
