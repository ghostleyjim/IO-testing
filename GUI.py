from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
import netifaces
import csv

# tag retrieval plc control scheme
import tag_retrieval


# main display:
# TODO read tags button
# TODO start IO
# TODO Project load


class selectionMenu():
    # show the GUI for selecting the PLC

    def __init__(self):
        self.ipselection = StringVar()
        self.selectmenu = ttk.Frame(root, padding="3 3 12 12")
        self.selectmenu.grid(column=0, row=0, sticky='N, W, E, S')
        self.ip_select = ttk.Combobox(self.selectmenu, textvariable=self.ipselection)
        self.ok_button = ttk.Button(self.selectmenu, text="OK", command=self.plcselected)
        self.selectdisplay()

    def plcselected(self):
        tag_retrieval.get_tags(self.ipselection.get())

    def selectdisplay(self):
        self.ipinfo()
        self.requestplcinfo()
        self.statusindication(False)
        return_button = ttk.Button(self.selectmenu, text="back", command=self.previous_menu)
        return_button.grid(column=2, row=0)

    def requestplcinfo(self):
        plc_info_button = ttk.Button(self.selectmenu, text="Check PLC", command=self.checkplc)
        plc_info_button.grid(column=0, row=1, sticky='W')

    def checkplc(self):
        check_label = ttk.Label(self.selectmenu, text="checking...", foreground='red')
        check_label.grid(column=1, row=1, sticky=W)
        self.discoverplc(check_label)

    def discoverplc(self, check_label):
        available = tag_retrieval.discoverPLC()

        if not available:
            check_label.config(text="no device found!")
        else:
            with open('plcinfo.txt', 'r') as f:
                plcinfo = f.read()
                plcdict = eval(plcinfo)
                ip_available = []
                for i in range(len(plcdict)):
                    ip_available.append(plcdict[i]['ip_address'])
                check_label.config(text="PLC file loaded")
                self.ip_select.grid(row=2, column=1)
                self.ip_select['values'] = ip_available
                self.ip_select.state(["readonly"])
                self.ok_button.grid(row=3, column=2)

    def findnetif(self):
        nics = netifaces.interfaces()
        niclist = []

        for i in range(len(nics)):
            nicinfo = netifaces.ifaddresses(nics[i])
            iplist = nicinfo[netifaces.AF_INET]
            ip = iplist[0]
            ipaddress = ip['addr']
            mac = nicinfo[netifaces.AF_LINK]
            mac = mac[0]
            macaddress = mac['addr']
            nic_mac_ip = "nic " + str(i) + " " + macaddress + " ," + ipaddress
            niclist.append(nic_mac_ip)

        return niclist

    def ipinfo(self):
        nic = self.findnetif()
        ipframe = ttk.Frame(self.selectmenu)
        ipframe.grid(column=0, row=0, sticky='N, W, E, S')

        for i in range(len(nic)):
            ttk.Label(ipframe, text=nic[i]).grid(column=1, row=i + 1, sticky=W)

    def statusindication(self, status):
        statusframe = ttk.Frame(self.selectmenu)
        statusframe.grid(sticky=W, column=0, row=3, columnspan=3)
        statustext = ttk.Label(statusframe, text="not connected")
        statustext.grid(column=0, row=2)
        statuscanvas = Canvas(statusframe, width=25, height=25)
        statuscanvas.grid(column=0, row=0)
        connectionindicator = statuscanvas.create_oval(10, 10, 25, 25)
        statuscanvas.itemconfig(connectionindicator, fill="red")
        if status == True:
            statustext.config(text="Connected")
            statuscanvas.itemconfig(connectionindicator, fill="green")

    def previous_menu(self):
        self.selectmenu.destroy()
        mainMenu()



class loadMenu:
    # load previous project to continue IO
    # TODO: load file
    def __init__(self):
        self.loadmenu = ttk.Frame(root, padding="3 3 12 12")
        self.loadmenu.grid(column=0, row=0, sticky='N, W, E, S')
        load_button = ttk.Button(self.loadmenu, text="load project...", command=self.loaddialogue)
        load_button.grid(column=0, row=0)
        return_button = ttk.Button(self.loadmenu, text="back", command=self.previous_menu)
        return_button.grid(column=0, row=1)

        self.projectfile = ''


    def previous_menu(self):
        print(self.projectfile)
        self.loadmenu.destroy()
        mainMenu()

    def loaddialogue(self):
        filetypes = (
            ('houdijk project' , '*.hdk'),
            ('All files', '*.*')
        )

        self.projectfile = fd.askopenfilename(
            title='open previous project',
            initialdir='/',
            filetypes=filetypes
        )

        ttk.Label(self.loadmenu, text=self.projectfile).grid(column=1, row=0)





class mainMenu:
    # main menu for selection of the different menu's
    def __init__(self):
        self.mainFrame = ttk.Frame(root, padding="3 3 12 12")
        self.mainFrame.grid(column=0, row=0, sticky='N, W, E, S')
        self.create_buttons()

    def select_PLC(self):
        self.mainFrame.destroy()
        selectionMenu()

    def load_project(self):
        self.mainFrame.destroy()
        loadMenu()

    def load_tags(self):
        self.mainFrame.destroy()
        tag_retrieval.get_tags()

    def create_buttons(self):
        button_PLC_select = ttk.Button(self.mainFrame, text="PLC config", command=self.select_PLC)
        button_PLC_select.grid(column=0, row=0)
        button_load_previous_project = ttk.Button(self.mainFrame, text="load project", command=self.load_project)
        button_load_previous_project.grid(row=1)


root = Tk()


def start_gui():

    mainMenu()
    root.mainloop()
