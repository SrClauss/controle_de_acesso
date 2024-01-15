from tkinter import BooleanVar, Button, Text, Tk, Frame, Checkbutton, Label
import requests

def send_click(e):

    body = {"script": text_id_script.get("1.0", "end-1c"), "activate": check_var.get()}
    req = requests.post("http://127.0.0.1:8080/save_script", json=body)
    print(req.text)
    

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