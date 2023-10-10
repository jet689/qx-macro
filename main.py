import time
import tkinter as tk
import json
from pynput import keyboard
from pynput.keyboard import Key,Controller
controller=Controller()
# print(keyboard.__file__)

pg = 0
val = True

f = open("data.json", "r")
data = json.loads(f.read())
f.close()

str_=""
keys=[]

for i in range(0,34):
    keys.append("")

class Option:
    def __init__(self, txt):
        self.uframe = tk.Frame(root)
        self.uframe.columnconfigure(0)
        self.uframe.columnconfigure(1)
        self.uframe.columnconfigure(2)
        self.purpose = tk.Text(self.uframe, font=("Arial", 15), height=3, width=60)
        self.purpose.insert("1.0", txt[1])
        self.purpose.grid(row=0, column=2, sticky=tk.W + tk.E)
        self.helper = tk.Label(self.uframe, font=("Arial", 15), text="==>")
        self.helper.grid(row=0, column=1, sticky=tk.W + tk.E)
        self.name = tk.Entry(self.uframe, font=("Arial", 15))
        self.name.insert(0, txt[0])
        self.name.grid(row=0, column=0, sticky=tk.W + tk.E)
        self.uframe.pack(fill="x", padx=10)

    def get_val(self):
        try:
            return self.purpose.get("1.0", tk.END), self.name.get()
        except:
            pass

    def destroy(self):
        self.purpose.destroy()
        self.uframe.destroy()
        self.helper.destroy()
        self.name.destroy()


def on_close():
    global val
    val = False
    root.destroy()


def fwd():
    global pg
    if pg < len(data[1]):
        pg += 1
        pgn.configure(state="normal")
        pgn.delete(0,tk.END)
        pgn.insert(0,f"{pg}")
        pgn.configure(state="disabled")
        global num1
        num1.destroy()
        try:
            num1 = Option(data[1][pg])
        except:
            num1 = Option(["", ""])
    # print(pg)


def bwd():
    global pg
    if pg != 0 or pg > 0:
        pg -= 1
        pgn.configure(state="normal")
        pgn.delete(0,tk.END)
        pgn.insert(0,f"{pg}")
        pgn.configure(state="disabled")
        global num1
        num1.destroy()
        num1 = Option(data[1][pg])

    # print(pg)


def save():
    f = open("data.json", "w")
    f.write(json.dumps(data))
    f.close()

def name(key_):
    key=str(key_)
    print(key,type(key))
    try:
        return key.char
    except AttributeError:
        return key
    
def keystore(e):
    global str_
    key=name(e).removeprefix("Key.").removeprefix("'").removesuffix("'")
    if key!="backspace":
        str1=""
        for i in range(0,33):
            keys[33-i]=keys[32-i]
            str1=str1+keys[33-i]
            print(33-i)

        if key!="space":
            keys[0]=key
        else:
            keys[0]=" "
        str1=str1+f"{keys[0]}"
        print(keys,str1)
        str_=str1
    else:
        str1=""
        for i in range(0,33):
            keys[i]=keys[i+1]
            str1=str1+keys[33-i]
            print(i)

        if key!="space":
            keys[33]=""
        else:
            keys[0]=" "
        str1=str1+f"{keys[0]}"
        print(str1)
        str_=str(str1)








listen=keyboard.Listener(on_press=keystore)
listen.start()





def updatedict():
    tc.destroy()
    str_=""
    for i in range(0,len(data[1])):
        str_=str_+f"pg {i}  {data[1][i][0]}. "
    
    tc= tk.Text(root, font=("Arial", 15), height=3, width=60)
    tc.pack(pady=80)
    tc.insert("1.0", str)
    tc.config(state="disabled")

def loop():
    global str_
    global num1
    global pg
    # print(num1.get_val())
    if not num1.get_val():
        exit()
    if pg!=int(pgn.get()):
        pg=pgn.get()
        num1.destroy()
        num1 = Option(data[1][pg])

    p, n = num1.get_val()
    # print("done with get val")
    p=p.removesuffix("\n")
    try:
        data[1][pg][0] = n
        data[1][pg][1] = p
    except:
        try:
            data[1].append([])
            data[1][pg].append(n)
            data[1][pg].append(p)
        except:
            exit()
    # print("leaving loop")
    if not val:
        root.destroy()   
        return
    for i in data[1]:
        if str_!=str_.removesuffix("qx."+f"{i[0]}"):
            print(i)
            print(i[1])
            for j in "qx."+f"{i[0]}":
                time.sleep(0.05)
                controller.tap(Key.backspace)
            controller.type(i[1].removesuffix("\n"))
            str_=str_+"^"
            break
    root.after(200, loop)


def getdict():
    str_=""
    for i in range(0,len(data[1])):
        str_=str_+f"pg {i}  {data[1][i][0]}. "
    return str




root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", on_close)
root.geometry("1000x500")
root.title("qx macro")

pgn= tk.Entry(root, font=("Arial", 15), width=10)
pgn.place(y=30,x=200)
pgn.insert(0,f"{pg}")
pgn.configure(state="disabled")
label = tk.Label(root, text="qx macro", font=("Arial", 25))
label.pack(pady=10)
num1 = Option(data[1][pg])

pg_forward = tk.Button(root, text=">", command=fwd)
pg_forward.place(x=900, y=30)

pg_bwd = tk.Button(root, text="<", command=bwd)
pg_bwd.place(x=100, y=30)

sv=tk.Button(root,text="save",command=save)
sv.place(x=800, y=30)
tc= tk.Text(root, font=("Arial", 15), height=3, width=60)
tc.place(y=200,x=50)
tc.insert("1.0", getdict())
tc.config(state="disabled")
root.after(0, loop)  # Call loop after 0 milliseconds
root.mainloop()
