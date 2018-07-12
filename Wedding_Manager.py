import Tkinter as Tk                    # imports
import ttk
import sqlite3

# Establish Database Connection
conn = sqlite3.connect("W_management.db") # or use :memory: to put it in RAM
cursor = conn.cursor()
# Create these tables if they don't already exist
try:
    cursor.execute("""CREATE TABLE people(firstname text, lastname text, street text, relationship text, status text)""")
except:
    pass
# Define our Application
class Application(ttk.Frame, Tk.Frame, Tk.PhotoImage):

    double_click_flag = False
    

    def __init__(self, master):
        ttk.Frame.__init__(self)
        Tk.Frame.__init__(self)
        Tk.PhotoImage.__init__(self)
        self.master = master
        

    
        master.geometry("800x600")                           # Create instance      
        master.title("Python GUI")                 # Add a title 
        
        self.toolbar = Tk.Frame(master, bd=1, relief=Tk.RAISED)
        self.toolbar.pack(anchor="n", fill=Tk.X)
        #self.add_person_image = Tk.PhotoImage(file="add_person.png")
        self.button = Tk.Button(self.toolbar, command=self.add_person)
        self.button.pack(side="left")
        
        self.separator1 = ttk.Separator(self.toolbar)
        self.separator1.pack(side="left")
        
        self.tabControl = ttk.Notebook(master)          # Create Tab Control
        self.tabControl.pack(expand=1, fill="both")  # Pack to make visible
        self.my_style = ttk.Style()
        self.my_style.configure('My.TFrame', background='#fff')

        self.tab1 = ttk.Frame(self.tabControl,  style='My.TFrame')
        #tab1.grid(column=1,row=1,sticky='news')            # Create a tab 
        self.tabControl.add(self.tab1, text='To do')      # Add the tab
        
        
        # Create Tab Control
        self.tab2 = ttk.Frame(self.tabControl)            # Create a tab 
        self.tabControl.add(self.tab2, text='Invited')      # Add the tab
        self.label2 = Tk.Label(self.tab2, text="Denver")
        self.label2.grid(row=1, column=0)
        # Adding the Columns for organization
        self.columns_tab1 = ttk.Frame(self.tab1)
        self.columns_tab1.pack(side=Tk.TOP, fill=Tk.BOTH, expand=Tk.Y)
        
        # create the tree and scrollbars
        self.dataCols = ('Name', 'Status', 'Phone')        
        self.tree = ttk.Treeview(columns=self.dataCols, 
                                 show = 'headings')
        
        ysb = ttk.Scrollbar(orient=Tk.VERTICAL, command= self.tree.yview)
        xsb = ttk.Scrollbar(orient=Tk.HORIZONTAL, command= self.tree.xview)
        self.tree['yscroll'] = ysb.set
        self.tree['xscroll'] = xsb.set
        
        # add tree and scrollbars to frame
        self.tree.grid(in_=self.columns_tab1, row=0, column=0, sticky=Tk.NSEW)
        ysb.grid(in_=self.columns_tab1, row=0, column=1, sticky=Tk.NS)
        xsb.grid(in_=self.columns_tab1, row=1, column=0, sticky=Tk.EW)
        
        # set frame resize priorities
        self.columns_tab1.rowconfigure(0, weight=1)
        self.columns_tab1.columnconfigure(0, weight=1)

        for n in self.dataCols:
            self.tree.heading(n, text=n.title())
        self.load_data()
    def load_data(self):
        self.data = [self.person_label = Tk.Label(self.tab1, text=self.input)]
        # add data to the tree 
        for item in self.data: 
            self.tree.insert('', 'end', values=item)

    def person_window(self):
        self.t = Tk.Toplevel(self)
        self.t.wm_title("Window")
        self.t.geometry("400x400")
        self.nlabel = Tk.Label(self.t, text="Name")
        self.nlabel.grid(row=0, column=0)
        self.nent = Tk.Entry(self.t, width=30)
        self.nent.grid(row=0, column=2)
        self.nbutton = Tk.Button(self.t, text="Save", command=self.save_person_db)
        self.nbutton.grid(row=1, column=2)

    def double_click(self, event):
        '''  set the double click status flag
        '''
        global double_click_flag
        double_click_flag = True
        print "You did it"
        
    
    def add_person(self):
        self.person_window()

    def save_person_db(self):
        self.input = self.nent.get()
        
        sql = "INSERT INTO people (firstname) VALUES (?)"
        self.res = cursor.execute(sql, (self.input,))
        conn.commit()
        # self.person_label = Tk.Label(self.tab1, text=self.input)
        # self.data.append(self.person_label)
        # self.load_data()

def main():     
        
    win = Tk.Tk()
    app = Application(win)
    
    win.mainloop()                     
    
   
main()

cursor.close()
del cursor
conn.close()
        
        
       
        
        
        



    
