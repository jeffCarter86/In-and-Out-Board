# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: inandout3.pyw
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import tkinter as tk
from tkinter import ttk
import json
import time

# STATUS_COLORS = {
#     "In the Hickory office": "light green",
#     "At Taylorsville Office": "light green",
#     "At the PC": "light green",
#     "At Clients": "light green",
#     "Lunch": "orange",
#     "Working Remotely": "orange",
#     "Meeting": "orange",
#     "Out of office": "red",
#     "Vacation": "red",
#     "Sick": "red",
#     # Add more statuses and colors as needed
# }

class InOutBoardApp:

    def __init__(self, root):
        self.root = root
        self.root.title('In and Out Board')
        self.users = {}
        with open('user_list.json', 'r') as file:
            self.user_list = json.load(file)
        self.label_name = tk.Label(root, text='Select your name:')
        self.label_name.pack()
        

        self.name_var = tk.StringVar()
        self.name_var.set(self.user_list[0] if self.user_list else "No Users")
        self.name_option_menu = tk.OptionMenu(root, self.name_var, *self.user_list)
        self.name_option_menu.pack()
        self.label_status = tk.Label(root, text='Select status:')
        self.label_status.pack()
        self.status_options = ['In the Hickory office', 'At Taylorsville Office', 'At the PC', 'At Clients', 'Lunch', 'Out of office', 'Working Remotely', 'Meeting', 'Vacation', 'Sick']
        self.status_var = tk.StringVar()
        self.status_var.set(self.status_options[0])
        self.status_option_menu = tk.OptionMenu(root, self.status_var, *self.status_options)
        self.status_option_menu.pack()
        self.label_comments = tk.Label(root, text='Add comments:')
        self.label_comments.pack()
        self.comments_entry = tk.Entry(root)
        self.comments_entry.pack()
        self.label_contact = tk.Label(root, text='Add contact number:')
        self.label_contact.pack()
        self.contact_entry = tk.Entry(root)
        self.contact_entry.pack()
        self.update_button = tk.Button(root, text='Update Status', command=self.update_status)
        self.update_button.pack()
        self.delete_button = tk.Button(root, text='Delete User', command=self.delete_user)
        self.delete_button.pack()
        self.user_tree = ttk.Treeview(root, columns=('Name', 'Status', 'Comments', 'Contact', 'Timestamp'))
        self.user_tree.heading('#0')
        self.user_tree.column('#0', width=0)
        self.user_tree.heading('#1', text='Name')
        self.user_tree.heading('#2', text='Status')
        self.user_tree.heading('#3', text='Comments')
        self.user_tree.heading('#4', text='Contact')
        self.user_tree.heading('#5', text='Timestamp')
        self.user_tree.pack()
        self.load_button = tk.Button(root, text='Refresh list', command=self.load_status)
        self.load_button.pack()
        self.refresh_timer()
        self.columns = ('Name', 'Status', 'Comments', 'Contact', 'Timestamp')
        self.sort_column = None
        for idx, col in enumerate(self.columns):
            self.user_tree.heading(idx, text=col, command=lambda c=col: self.sort_treeview(c, False))

    def sort_treeview(self, col, reverse):
        col_index = self.columns.index(col)
        data = [(self.user_tree.set(child, col_index), child) for child in self.user_tree.get_children('')]
        try:
            data.sort(key=lambda x: int(x[0]), reverse=reverse)
        except ValueError:
            data.sort(reverse=reverse)
        for index, item in enumerate(data):
            self.user_tree.move(item[1], '', index)
        self.user_tree.heading(col_index, command=lambda: self.sort_treeview(col, not reverse))

    def update_status(self):
        name = self.name_var.get()
        status = self.status_var.get()
        comments = self.comments_entry.get()
        contact = self.contact_entry.get()
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        if name:
            self.users[name] = {'status': status, 'comments': comments, 'contact': contact, 'timestamp': timestamp}
            self.comments_entry.delete(0, tk.END)
            self.contact_entry.delete(0, tk.END)
            self.update_user_tree()
            self.save_status()

    def delete_user(self):
        selected_items = self.user_tree.selection()
        if selected_items:
            selected_name = self.user_tree.item(selected_items[0])['values'][0]
            if selected_name in self.users:
                del self.users[selected_name]
                self.update_user_tree()
                self.save_status()

    def update_user_tree(self):
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
            
         # Configure tag for each status with its respective color
        status_colors = {
            "In the Hickory office": "light green",
            "At Taylorsville Office": "light green",
            "At the PC": "light green",
            "At Clients": "light green",
            "Lunch": "orange",
            "Working Remotely": "orange",
            "Meeting": "orange",
            "Out of office": "red",
            "Vacation": "red",
            "Sick": "red",
            # Add more statuses and colors as needed
        }
            
            
        for name, info in sorted(self.users.items()):
            status = info['status']
            comments = info['comments']
            contact = info['contact']
            timestamp = info['timestamp']
            self.user_tree.insert('', 'end', values=(name, status, comments, contact, timestamp),
                                  tags=(status,))
            self.user_tree.tag_configure(status, background=status_colors.get(status, 'white'))


    def load_status(self):
        try:
            with open('status.json', 'r') as file:
                self.users = json.load(file)
                self.update_user_tree()
        except FileNotFoundError:
            return
        else:
            pass

    def save_status(self):
        with open('status.json', 'w') as file:
            json.dump(self.users, file)

    def refresh_timer(self):
        self.load_status()
        self.update_user_tree()
        self.root.after(5000, self.refresh_timer)
if __name__ == '__main__':
    root = tk.Tk()
    app = InOutBoardApp(root)
    root.mainloop()