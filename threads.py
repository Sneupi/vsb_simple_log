
from logger import Logger
from threading import Event
from serial import Serial
import time
from queue import Queue
from gui.maingui import MainGUI
from updaters import update_gui

def serial_thread(ser: Serial, log: Logger, run_event: Event, tx_queue: Queue, gui: MainGUI):
    """Waits for read and logs"""
    while run_event.is_set():
        # RX
        if ser.in_waiting > 0:
            data = ser.readline().decode().strip()
            print(data)
            log.log(('RX',data))
            update_gui(data, gui)
            
        # TX
        if not tx_queue.empty():
            data = str(tx_queue.get()).strip()
            ser.write(data.encode() + b'\n')
            print(data)
            log.log(('TX',data))
            
        # Neither, sleep
        if tx_queue.empty() and ser.in_waiting == 0:
            time.sleep(0.01)
            