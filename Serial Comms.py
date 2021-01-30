import tkinter as tk
from tkinter.constants import END
import tkinter.ttk as ttk
from serial import *
from threading import Timer
import serial.tools.list_ports

ser = ''
serBuffer = ''
backgroundColour = '#3C3C3C'

def serial_ports():                                             # Find available com ports
    ports = serial.tools.list_ports.comports()
    available_ports = []
    for p in ports:
        available_ports.append(p.device)                        # Append each found serial port to array available_ports

    return available_ports

def updateComPortlist():
    list = serial_ports()
    cb['values'] = list

def on_select(event=None):                                      # When com port is selected, connect to com port
    global ser
    serialPortSelect = cb.get()
    baudRate = 115200
    ser = Serial(serialPortSelect , baudRate, timeout=0, writeTimeout=0) #ensure non-blocking
    readSerial()

def buttonSendCommand():
    temp='T1'                                                   # Change temp to what value you want the button to send
    sendSerial(temp)

def sendSerial(sendValue):
    if (ser == ''):                                             # Checks to see if com port has been selected
        textOUTPUT.insert(END, 'Serial port not selected!\n')
        textOUTPUT.see(END)
    else:
        ser.write(sendValue.encode())                           # Send button value to coneected com port

def clearAll():
    textINPUT.delete(0,END)                                     # Clear text box

def func(event):                                                # When 'enter' pressed
    res1 = textINPUT.get()                                      # Get text from box
    ser.write(res1.encode())                                    # Write contents of box to serial port
    t = Timer(0.5, clearAll)                                    # Clears text after 0.5 seconds
    t.start()

mainWindow = tk.Tk()
mainWindow.title('Serial Comms')
mainWindow.configure(height='600', width='800')
frame_1 = tk.Frame(mainWindow, bg=backgroundColour)
frame_1.configure(height='600', width='800')
frame_1.place(anchor='nw', x='0', y='0')
lbl1 = tk.Label(mainWindow, text='Serial Port')
lbl1.configure(bg=backgroundColour, fg='White')
lbl1.place(anchor='nw', x='30', y='10')
cb = ttk.Combobox(frame_1, postcommand=updateComPortlist)
cb.place(anchor='nw', height='26', width='200', x='30', y='40')
buttonComm = tk.Button(frame_1)
buttonComm.configure(text='Send\nCommand')
buttonComm.place(anchor='nw', height='60', width='100', x='30', y='120')
buttonComm.configure(command=buttonSendCommand)
lbl2 = tk.Label(mainWindow, text='Serial Send:')
lbl2.configure(bg=backgroundColour, fg='White')
lbl2.place(anchor='nw', x='30', y='220')
textINPUT = tk.Entry(frame_1)
textINPUT.place(anchor='nw', height='30', width='740', x='30', y='250')
textINPUT.focus_set()
lbl3 = tk.Label(mainWindow, text='Serial Receive:')
lbl3.configure(bg=backgroundColour, fg='White')
lbl3.place(anchor='nw', x='30', y='300')
textOUTPUT = tk.Text(frame_1)
textOUTPUT.configure(height='18', width='105')
textOUTPUT.place(anchor='nw', x='30', y='330')

def readSerial():
    global ser
    global serBuffer
    if (ser == ''):
        return
    else:
        while True:
            c = ser.read()

            if len(c) == 0:
                break

            if (c == b'\xb0'):                                  # Change / remove characters that cause error
                c = '°'
            elif (c == b'\xb2'):
                c = '²'
            elif (c == b'\xba') or (c == b'\xc2'):
                c = ''
            else:
                c = c.decode('ascii') 

            if c == '\r':                                       # check if character is a delimeter
                c = ''                                          # don't want returns. chuck it
                
            if c == '\n':
                serBuffer += '\n'                               # add the newline to the buffer
                textOUTPUT.insert(END, serBuffer)               #add the line to the TOP of the log
                textOUTPUT.see(END)
                serBuffer = ''                                  # empty the buffer
            else:
                serBuffer += c                                  # add to the buffer
        
        mainWindow.after(10, readSerial)                        # check serial again soon

mainWindow.bind('<Return>', func)
cb.bind('<<ComboboxSelected>>', on_select)

mainWindow.mainloop()