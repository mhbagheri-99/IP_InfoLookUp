from tkinter import *
from tkinter import messagebox
import re
import json
from urllib.request import urlopen


masks = ['255','254','252','248','240','224','192','128','0']

#defs

def clicked():

    if not validIPAddress(txt.get()):
        messagebox.showerror("ERROR","Invalid IP!!!")
        reset()
    else:
        IP = txt.get().split(".")
        IP_bin = [bin(int(i)).replace('0b','') for i in IP]
        ip.configure(text=txt.get())
        ip_bin.configure(text=IP_bin)
    
        if 1 <= int(IP[0]) < 127:
            cl.configure(text="Class A")
            if int(IP[0]) == 10:
                pv.configure(text="Private")
            else:
                pv.configure(text="Public")
        
        if int(IP[0]) == 127:
            cl.configure(text="Class A [root back test]")
            pv.configure(text="Public")
        
        if 128 <= int(IP[0]) <= 191:
            cl.configure(text="Class B")
            if int(IP[0]) == 172 and 16 <= int(IP[1]) <= 31:
                pv.configure(text="Private")
            else:
                pv.configure(text="Public")
        
        if 192 <= int(IP[0]) <= 223:
            cl.configure(text="Class C")
            if int(IP[0]) == 192 and int(IP[1]) == 168:
                pv.configure(text="Private")
            else:
                pv.configure(text="Public")
        
        if 224 <= int(IP[0]) <= 239:
            cl.configure(text="Class D")
            pv.configure(text="Public")
        
        if 240 <= int(IP[0]) <= 255:
            cl.configure(text="Class E")
            pv.configure(text="Public")
        
        ipinfo(txt.get())


def validIPAddress(IP):
      
        def isIPv4(s):
            try: return str(int(s)) == s and 0 <= int(s) <= 255
            except: return False
        if IP.count(".") == 3 and all(isIPv4(i) for i in IP.split(".")):
            return True
        else:
            return False

def ipinfo (ip):
    url = 'http://ipinfo.io/' + ip + '/json'
    response = urlopen(url)
    data = json.load(response)

    country.configure(text=data['country'])
    city.configure(text=data['city'])
    region.configure(text=data['region'])

def netClicked():
    if not validNetMaskAddress(txt1.get()):
        messagebox.showerror("ERROR","Netmask not supported!!!")
    else:
        NET = txt1.get().split(".")
        NET_bin = [bin(int(i)).replace('0b','') for i in NET]
        net.configure(text=txt1.get())
        net_bin.configure(text=NET_bin)
        mb.configure(text=str(net_bin.cget("text").count("1")))
        net_addr.configure(text=andTwoNums(ip.cget("text"),net.cget("text")))
        br.configure(text=broadcastAddress(ip.cget("text"),32 - int(mb.cget("text"))))

def validNetMaskAddress(netmask):
    net_list = netmask.split(".")
    if cl.cget("text") == "Class A":
        if netmask.count(".") == 3 and net_list[0] == '255' and net_list[1] in masks and net_list[2] == net_list[3] == '0':
            return True
        else:
            return False
    elif  cl.cget("text") == "Class B":
        if netmask.count(".") == 3 and net_list[0] == net_list[1] == '255' and net_list[2] in masks and net_list[3] == '0':
            return True
        else:
            return False
    elif cl.cget("text") == "Class C":
        if netmask.count(".") == 3 and net_list[0] == net_list[1] == net_list[2] == '255' and net_list[3] in masks:
            return True
        else:
            return False
    else:
        return False

def andTwoNums(num1,num2):
    list1 = num1.split(".")
    list2 = num2.split(".")
    text = str(int(list1[0]) & int(list2[0]))
    for i in range(1,len(list1)):
        text += "." + str(int(list1[i]) & int(list2[i]))
    return text

def broadcastAddress(num1,num2):
    list1 = num1.split(".")
    list2 = []
    i = num2
    text = ""
    while i > 0:
        if i > 8:
            list2.append(255)
            i -= 8
        else:
            list2.append(2**i - 1)
            i = 0
    while len(list2) != 4:
        list2.append(0)
    for i in range(4):
        text += str(int(list1[i]) | list2[3-i]) + "."
    text = text[:-1]
    return text

def reset():
    ip.configure(text="")
    ip_bin.configure(text="")
    cl.configure(text="")
    pv.configure(text="")
    country.configure(text="")
    city.configure(text="")
    region.configure(text="")
    net.configure(text="")
    net_bin.configure(text="")
    mb.configure(text="")
    net_addr.configure(text="")
    br.configure(text="")

#GUI
window = Tk()

window.title("IP Checker")
window.geometry('300x700')

lbl1 = Label(window, text="IP address:")
lbl1.pack()

ip = Label(window, text="")
ip.pack()

ip_bin = Label(window, text="")
ip_bin.pack()

lbl2 = Label(window, text="Class:")
lbl2.pack()

cl = Label(window, text="")
cl.pack()

lbl3 = Label(window, text="Privacy:")
lbl3.pack()

pv = Label(window, text="")
pv.pack()

lbl4 = Label(window, text="Country:")
lbl4.pack()

country = Label(window, text="")
country.pack()

lbl5 = Label(window, text="City:")
lbl5.pack()

city = Label(window, text="")
city.pack()

lbl6 = Label(window, text="Region:")
lbl6.pack()

region = Label(window, text="")
region.pack()

lbl7 = Label(window, text="")
lbl7.pack()

lbl8 = Label(window, text="Enter the IP address:")
lbl8.pack()

txt = Entry(window,width=20)
txt.pack()
txt.focus()



sub = Button(window, text="Submit", command=clicked)
sub.pack()

lbl9 = Label(window, text="********************************************")
lbl9.pack()

lbl10 = Label(window, text="Netmask:")
lbl10.pack()

net = Label(window, text="")
net.pack()

net_bin = Label(window, text="")
net_bin.pack()

lbl11 = Label(window, text="Mask bits:")
lbl11.pack()

mb = Label(window, text="")
mb.pack()

lbl12 = Label(window, text="Network address:")
lbl12.pack()

net_addr = Label(window, text="")
net_addr.pack()

lbl13 = Label(window, text="Broadcast address:")
lbl13.pack()

br = Label(window, text="")
br.pack()

lbl14 = Label(window, text="Enter the subnet mask:")
lbl14.pack()

txt1 = Entry(window,width=20)
txt1.pack()

netSub = Button(window, text="Submit", command=netClicked)
netSub.pack()

rst = Button(window, text="Reset", command=reset)
rst.pack()

window.mainloop()