import tkinter as tk
from tkinter.constants import TRUE
import serial
from serial.serialutil import PortNotOpenError
from serial.tools.list_ports import comports
import os
import sys
from tkinter.ttk import *

# Define constants used throughout the program
PORT = 'COM5'
BAUD_RATE = 9600
TIMEOUT = 0

# Initialize the serial communication and GUI
Device = serial.Serial(baudrate=BAUD_RATE, timeout=TIMEOUT)
window = tk.Tk()
window.title('Serial Communication')

def initDevice(com = PORT):
        '''This function opens the connection between Device and the PC
                Input: <string> COM port (optional. uses the globally defined port if not given)
                Output: <boolean> the success of the operation'''
        
        print("Connection to:", com)
        Device.port = com

        try:    #Try and except function is similar to if condition, the differece is it does the action then waits for the reply whether it's true or false.
                Device.open()
                print("Connection with Device successfully opened")
                return True
        except (FileNotFoundError, OSError):
                print("ERROR: Can't connect to this port!")
                return False

def reading():
        '''Tries to read the value sent by Device and returns it
                Input: None
                Output: <int|str> the integer sent by the Device, or ‘N/A’ if it couldn’t be read
        '''
        try:
                read = Device.read(3)           # read 3 bytes (1 digit + 2 line terminators)
                string = read.decode().strip()  # decode the binary string to unicode and strip all whitespace
                return int(string)
        except:
                return 'N\A'


running = True
def read_notepad():

        try:
                filesize = os.path.getsize("serial_no.txt")
                while filesize == 0:
                        filesize = os.path.getsize("serial_no.txt")
                        return 'Waiting for data'
                if running:
                        CMD = open("serial_no.txt","r+")
                        line = CMD.readline();
                        CMD = open("serial_no.txt","w")
                        return Device.write((line + '\r\n').encode())
        
        except (PortNotOpenError):
                return 'Connect port'
        window.after(1500, read_notepad)

def start():
        global running
        running = True

def stop():
        global running
        running = False


sel = tk.StringVar()
sel.set('Refresh to see available ports')
sel.trace('w', lambda *args: initDevice(sel.get()))

options = tk.OptionMenu(window, sel, [])

def listPorts():
        ''' Refreshes the available COM ports and updates the Options Menu
        '''
        ports = [port.device for port in comports()]    # get the available ports
        #ports = [1,2,3]     # for testing. comment later
        print("Ports found:", ports)
        menu = options['menu']
        menu.delete(0, 'end')   # Clear the previous items
        if len(ports) == 0:
                sel.set('No ports found. refresh again')
        else:
                for port in ports:
                        menu.add_command(label=port, command=lambda p=port: sel.set(p))
                sel.set('Choose a port:')


refreshPorts = tk.Button(window, text='Refresh COM ports', command=listPorts) 
start_button = tk.Button(window, text = 'Start Reading', command = start)
stop_button = tk.Button(window, text = 'Stop Reading', command = stop)
label = tk.Label(window)

def update_label():
        label.configure(text=f"Current reading: {read_notepad()}")   # Update the text with the latest reading
        label.after(1000, update_label)          # Queue the function to run again after 100 milliseconds

update_label()                  # Call for the first time to initialize the recursive updating

# pack the UI elements to the window
refreshPorts.pack(side='top')
options.pack()
label.pack()
start_button.pack()
stop_button.pack()

window.config()
window.mainloop()