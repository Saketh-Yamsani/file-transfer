from tkinter import *
import socket
import threading
from tkinter import filedialog, messagebox
import os

root = Tk()
root.title("Share Me")
root.geometry("450x560+500+200")
root.configure(bg="#f4fdfe")
root.resizable(False, False)

filename = None  # Initialize filename variable globally

def Send():
    window = Toplevel(root)
    window.title("Send")
    window.geometry('450x560+500+200')
    window.configure(bg="#f4fdfe")
    window.resizable(False, False)

    def select_file():
        global filename
        filename = filedialog.askopenfilename(
            initialdir=os.getcwd(), title='Select File',
            filetype=(('Text Files', '*.txt'), ("All Files", "*.*"))
        )
        if filename:
            send_button.config(state=NORMAL)
            messagebox.showinfo("File Selected", f"File selected: {filename}")

    def sender():
        if not filename:
            messagebox.showwarning("Warning", "Please select a file first.")
            return

        def send_file():
            try:
                s = socket.socket()
                host = socket.gethostname()
                port = 8080
                s.bind((host, port))
                s.listen(1)
                print(host)
                print("Waiting for incoming connections...")

                conn, addr = s.accept()
                with open(filename, 'rb') as file:
                    file_data = file.read(1024)
                    conn.send(file_data)
                conn.close()

                success_label.config(text="File has been sent successfully!", fg="green")
            except Exception as e:
                print(f"Error: {e}")
                success_label.config(text="Failed to send the file.", fg="red")

        threading.Thread(target=send_file).start()

    # icon
    image_icon1 = PhotoImage(file="Image/send.png")
    window.iconphoto(False, image_icon1)

    Sbackground = PhotoImage(file="Image/sender.png")
    Label(window, image=Sbackground).place(x=-2, y=0)

    Mbackground = PhotoImage(file="Image/id.png")
    Label(window, image=Mbackground, bg="#f4fdfe").place(x=100, y=260)

    host = socket.gethostname()
    Label(window, text=f'ID: {host}', bg='white', fg='black').place(x=140, y=290)

    Button(window, text="+ Select File", width=10, height=1, font='arial 14 bold', bg="#fff", fg="#000", command=select_file).place(x=160, y=150)
    
    send_button = Button(window, text="SEND", width=8, height=1, font='arial 14 bold', fg="#fff", bg="#000", command=sender, state=DISABLED)
    send_button.place(x=300, y=150)
    
    success_label = Label(window, text="", bg="#f4fdfe", font=('arial', 12))
    success_label.place(x=150, y=400)

    window.mainloop()

def Receive():
    main = Toplevel(root)
    main.title("Receive")
    main.geometry('450x560+500+200')
    main.configure(bg="#f4fdfe")
    main.resizable(False, False)

    def receiver():
        def receive_file():
            try:
                ID = SenderID.get()
                filename1 = incoming_file.get()

                s = socket.socket()
                port = 8080
                s.connect((ID, port))
                with open(filename1, 'wb') as file:
                    file_data = s.recv(1024)
                    file.write(file_data)
                s.close()

                success_label.config(text="File has been received successfully!", fg="green")
            except Exception as e:
                print(f"Error: {e}")
                success_label.config(text="Failed to receive the file.", fg="red")

        threading.Thread(target=receive_file).start()

    # icon
    image_icon1 = PhotoImage(file="Image/receive.png")
    main.iconphoto(False, image_icon1)

    Hbackground = PhotoImage(file="Image/receiver.png")
    Label(main, image=Hbackground).place(x=-2, y=0)

    logo = PhotoImage(file='Image/profile.png')
    Label(main, image=logo, bg="#f4fdfe").place(x=100, y=250)

    Label(main, text="Receive", font=('arial', 20), bg="#f4fdfe").place(x=100, y=280)

    Label(main, text='Input Sender ID', font=('arial', 10, 'bold'), bg="#f4fdfe").place(x=20, y=340)
    SenderID = Entry(main, width=25, fg="black", border=2, bg='white', font=('arial', 15))
    SenderID.place(x=20, y=370)
    SenderID.focus()

    Label(main, text='Filename for the incoming file:', font=('arial', 10, 'bold'), bg="#f4fdfe").place(x=20, y=420)
    incoming_file = Entry(main, width=25, fg="black", border=2, bg='white', font=('arial', 15))
    incoming_file.place(x=20, y=450)

    imageicon = PhotoImage(file="Image/arrow.png")
    rr = Button(main, text="Receive", compound=LEFT, image=imageicon, width=130, bg="#39c790", font="arial 14 bold", command=receiver)
    rr.place(x=20, y=500)

    success_label = Label(main, text="", bg="#f4fdfe", font=('arial', 12))
    success_label.place(x=150, y=400)

    main.mainloop()

# Main window setup
image_icon = PhotoImage(file="Image/icon.png")
root.iconphoto(False, image_icon)

Label(root, text="File Transfer", font=('Acumin Variable Concept', 20, 'bold'), bg="#f4fdfe").place(x=0, y=30)
Frame(root, width=400, height=2, bg="#f3f5f6").place(x=25, y=80)

send_image = PhotoImage(file="Image/send.png")
send = Button(root, image=send_image, bg="#f4fdfe", bd=0, command=Send)
send.place(x=50, y=100)

receive_image = PhotoImage(file="Image/receive.png")
receive = Button(root, image=receive_image, bg="#f4fdfe", bd=0, command=Receive)
receive.place(x=300, y=100)

Label(root, text="Send", font=('Acumin Variable Concept', 17, 'bold'), bg="#f4fdfe").place(x=65, y=200)
Label(root, text="Receive", font=('Acumin Variable Concept', 17, 'bold'), bg="#f4fdfe").place(x=300, y=200)

background = PhotoImage(file="Image/background.png")
Label(root, image=background).place(x=-2, y=323)

root.mainloop()
