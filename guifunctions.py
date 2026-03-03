from tkinter import *
from tkinter import ttk
from sqlfunctions import *


root = Tk()

class Application():
    def __init__(self):
        createTable()
        self.front()
        self.frame()
        self.widgets()
        self.treeview()

        root.mainloop()




    def front(self):
        root.title("Password Management")
        root.geometry("700x500")
        root.minsize(width=500, height=300)
        root.maxsize(width=1080, height=600)
        alert = Label(root, text="🏆 To use the auto password generator, leave the password field blank.")
        alert.place(relx=0.1, rely=0.001)
        Label(root, text="⚠️ Auto Password have 11 characters").place(relx=0.1, rely=0.05)

    def frame(self):
        ## Frame Above
        self.frameone = Frame(root, border=4, bg="#042a92") 
        self.frameone.place(relx=0.01, rely=0.1, relwidth=0.98, relheight=1)

        ## Frame Below
        self.frametwo = Frame(root, border=4, bg="#7784ad")
        self.frametwo.place(relx=0.01, rely=0.5, relwidth=0.98, relheight=1)

    def widgets(self):

        ## Buttons
        self.create_table_btn = Button(self.frameone, text="Add account", bd=3, command=lambda: [createAccount(self.platform_entry.get(), self.user_entry.get(), self.password_entry.get()), self.realtime()])
        self.create_table_btn.place(relx=0.6, rely=0.01)

        self.update_table_btn = Button(self.frameone, text="Change pass", bd=3, command=lambda: [changePassword(platform=self.platform_entry.get(), password=self.password_entry.get(), user=self.user_entry.get()), self.realtime()])
        self.update_table_btn.place(relx=0.78, rely=0.01)

        self.encrypt_btn = Button(self.frameone, text="Encrypt data", bd=3, command=lambda: [encryptSrc(), self.realtime()])
        self.encrypt_btn.place(relx=0.6, rely=0.1)

        self.decrypt_btn = Button(self.frameone, text="Decrypt data", bd=3, command=lambda: [decryptSrc(), self.realtime()])
        self.decrypt_btn.place(relx=0.78, rely=0.1)

        self.delete_row_btn = Button(self.frameone, text="Delete", bd=3, command=lambda: [deleteAccount(platform=self.platform_entry.get(), password=self.password_entry.get(), user=self.user_entry.get()), self.realtime()])
        self.delete_row_btn.place(relx=0.72, rely=0.19)

        ## Labels
        self.platform = Label(self.frameone, text="Platform", bg="#042a92", fg="#ffffff", font=('verdana',11))
        self.platform.place(relx=0.01, rely=0.005)

        self.user = Label(self.frameone, text="User", bg="#042a92", fg="#ffffff", font=('verdana',11))
        self.user.place(relx=0.01, rely=0.08)

        self.password = Label(self.frameone, text="Password", bg="#042a92", fg="#ffffff", font=('verdana',11))
        self.password.place(relx=0.01, rely=0.15)

        ## Input
        self.platform_entry = Entry(self.frameone)
        self.platform_entry.place(relx=0.13, rely=0.005)

        self.user_entry = Entry(self.frameone)
        self.user_entry.place(relx=0.13, rely=0.08)

        self.password_entry = Entry(self.frameone)
        self.password_entry.place(relx=0.13, rely=0.15)


    def treeview(self):
        global tree 
        tree = ttk.Treeview(self.frametwo, height=3, columns=("col1", "col2", "col3"), show="headings")

        tree.heading("col1", text="Platform")
        tree.heading("col2", text="Username")
        tree.heading("col3", text="Password")

        tree.column("col1", width=200)
        tree.column("col2", width=200)
        tree.column("col3", width=200)

        tree.place(relx=0.01, rely=0.01, relwidth=0.96, relheight=0.85)

        self.scroll = Scrollbar(self.frametwo, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=self.scroll.set)
        self.scroll.place(relx=0.96, rely=0.01, relwidth=0.03, relheight=0.85 )

        for line in readTable():
                tree.insert("", END, values=line)
        tree.bind("<<TreeviewSelect>>", self.select)

    
    def select(self, event=None):
        selected_item = tree.selection()
        if selected_item:
            values = tree.item(selected_item[0], "values" )

            self.platform_entry.delete(0, END)
            self.user_entry.delete(0, END)
            self.password_entry.delete(0, END)


            self.platform_entry.insert(0, values[0])
            self.user_entry.insert(0, values[1])
            self.password_entry.insert(0, values[2])


    def realtime(self):
        for item in tree.get_children():
            tree.delete(item)

        for line in readTable():
            tree.insert("", END, values=line)
