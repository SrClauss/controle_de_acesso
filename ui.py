import json
from tkinter import BooleanVar, Button, Text, Tk, Frame, Checkbutton, Label
import requests


prodution = False
url = "https://x9s3hsdp44.us-east-1.awsapprunner.com/" if prodution else "http://192.168.1.6:8080/"

def send_click(e):

    body = {"script_id": text_id_script.get("1.0", "end-1c"), "activate": check_var.get(), 'errors': []}
    req = requests.post(f"{url}save_script", json=body)
    print(body)

root = Tk()
frame = Frame(root)
frame.pack()
Label(frame, text="Script ID").pack(anchor="w")

text_id_script = Text(frame, width=30, height=1)
text_id_script.pack(padx=5, pady=5)

check_var = BooleanVar()
checkbox_activate = Checkbutton(frame, text="Activate", variable=check_var)
checkbox_activate.pack(padx=5, pady=5, anchor="w")
checkbox_activate.select()

button_send = Button(frame, text="Send",background="green", foreground="white", width=33, height=3)
button_send.pack(padx=5, pady=5, anchor="w")
button_send.bind("<Button-1>", send_click)



root.mainloop()