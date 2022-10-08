from tkinter import *
import collections
import pickle
from functools import partial
from tkinter import messagebox


class ContactList:

    def __init__(self, master, contacts):
        self.master = master
        self.contact_dict = contacts

        self.contacts_frame = Frame(self.master)
        frame = Frame(self.master)
        frame.master.title("Contact List")

        self.update_data()

        Button(frame, text='Add New Contact', width=200, command=self.add_contact_window).pack(anchor='center')
        Label(frame, text=' ').pack(anchor='n')

        frame.pack(anchor='center', fill='both')
        self.contacts_frame.pack(anchor='nw')

    def update_data(self):
        for widget in self.contacts_frame.winfo_children():
            widget.destroy()

        for key in self.contact_dict:
            Button(self.contacts_frame, text=key, width=200, command=partial(self.contact_info, key)).pack(anchor='center')

    def add_contact_window(self):
        AddWindow(self.master, self , self.contact_dict)

    def contact_info(self, key):
        ContactInfo(self.master, self.contact_dict, key)


class ContactInfo:

    def __init__(self, master, contacts, key):
        self.master = master
        self.contact = contacts[key]
        self.contacts_window = Toplevel()
        self.contacts_window.title("Contact Details")
        self.contacts_window.geometry('400x200')

        Label(self.contacts_window, text='Name: ', width=15, anchor='e').grid(row=0, column=0)
        self.nameEntry = Entry(self.contacts_window, width=35)
        self.nameEntry.insert(0, str(self.contact['name']))
        self.nameEntry.grid(row=0, column=1)

        Label(self.contacts_window, text='phone: ', width=15,  anchor='e').grid(row=1, column=0)
        self.phoneEntry = Entry(self.contacts_window, width=35)
        self.phoneEntry.insert(0, str(self.contact['phone']))
        self.phoneEntry.grid(row=1, column=1)
      
        Label(self.contacts_window, text='email: ', width=15, anchor='e').grid(row=2, column=0)
        self.emailEntry = Entry(self.contacts_window, width=35)
        self.emailEntry.insert(0, str(self.contact['email']))
        self.emailEntry.grid(row=2, column=1)

        Label(self.contacts_window, text='address: ', width=15, anchor='e').grid(row=3, column=0)
        self.addressEntry = Entry(self.contacts_window, width=35)
        self.addressEntry.insert(0, str(self.contact['address']))
        self.addressEntry.grid(row=3, column=1)

        Label(self.contacts_window, text='     ', width=15).grid(row=4)
        Button(self.contacts_window, text='Cancel', width=10, command=self.contacts_window.destroy).place(x=120, y=100)
        Button(self.contacts_window, text='Save', width=10, command=lambda: self.update_contact(contacts)).place(x=245, y=100)


    def update_contact(self, contacts):
        name = str(self.nameEntry.get())
        phone = str(self.phoneEntry.get())
        email = str(self.emailEntry.get())
        address = str(self.addressEntry.get())
        

        save = {'name': name, 'phone': phone, 'email': email, 'address': address}
        key = save['name']
        contacts[key] = save
        contact = {}
        for item in sorted(list(contacts)):
            contact[item] = contacts[item]
        pickle.dump(contact, open('contacts.txt', 'wb'))
        messagebox.showinfo('Status', 'Contact update successfully')
        self.contacts_window.destroy()
    
    
class AddWindow:

    def __init__(self, master, main_window, contacts):
        self.master = master
        self.contacts = contacts
        self.main_window = main_window

        self.add_window = Toplevel()
        self.add_window.geometry('400x200')
        self.add_window.title("Add Contact")
        Label(self.add_window, text='Name: ', width=15, anchor='e').grid(row=1, column=1)
        Label(self.add_window, text='Phone: ', width=15, anchor='e').grid(row=2, column=1)
        Label(self.add_window, text='Email: ', width=15, anchor='e').grid(row=3, column=1)
        Label(self.add_window, text='Address: ', width=15, anchor='e').grid(row=4, column=1)
        
        self.name = StringVar()
        self.email = StringVar()
        self.address = StringVar()
        self.phone = StringVar()

        Entry(self.add_window, textvariable=self.name, width=35).grid(row=1, column=2)
        Entry(self.add_window, textvariable=self.phone, width=35).grid(row=2, column=2)
        Entry(self.add_window, textvariable=self.email, width=35).grid(row=3, column=2)
        Entry(self.add_window, textvariable=self.address, width=35).grid(row=4, column=2)

        Button(self.add_window, text='Cancel', width=10, command=self.add_window.destroy).place(x=120, y=100)
        Button(self.add_window, text="Save", width=10, command=lambda: self.save(self.contacts)).place(x=245, y=100)

    def save(self, contacts):
        name = str(self.name.get())
        phone = str(self.phone.get())
        email = str(self.email.get())
        address = str(self.address.get())
        

        save = {'name': name, 'phone': phone, 'email': email, 'address': address}
        key = save['name']
        contacts[key] = save
        contact = {}
        for item in sorted(list(contacts)):
            contact[item] = contacts[item]
        pickle.dump(contact, open('contacts.txt', 'wb'))
        messagebox.showinfo('Status', 'Contact save successfully')
        self.add_window.destroy()
        self.main_window.update_data()


def main():
    try:
        input_file = open("contacts.txt", "rb")
        data = pickle.load(input_file)
    except (FileNotFoundError, IOError):
        data = collections.OrderedDict()

    root = Tk()
    root.geometry('400x200')
    ContactList(root, data)
    root.mainloop()

main()