import Tkinter as Tk                 # imports
import tkMessageBox
import ttk
import sqlite3


class Application(ttk.Frame, Tk.Frame, Tk.PhotoImage):

    double_click_flag = False
    

    def __init__(self, master):
        ttk.Frame.__init__(self)
        Tk.Frame.__init__(self)
        Tk.PhotoImage.__init__(self)
        self.master = master
        
        master.geometry("800x600")                           # Create instance      
        master.title("Python GUI")                 # Add a title 
        
        #=================================================================================================
        # Establish Database Connection
        self.conn = sqlite3.connect("W_management.db") # or use :memory: to put it in RAM
        self.cursor = self.conn.cursor()
        # Create these tables if they don't already exist
        try:
            self.cursor.execute("""CREATE TABLE people(firstname text, lastname text, address text, relationship text, status text)""")
            self.message = tkMessageBox.showinfo("Title", "Congratulations, who is getting married?")
            #self.get_names = Tk.Entry(master, text"Enter His Name")
        except:
            pass
            
        #=================================================================================================
        # Define our Application
        #=================================================================================================
        
        self.toolbar = Tk.Frame(master, bd=1, relief=Tk.RAISED)
        self.toolbar.pack(anchor="n", fill=Tk.X)
        #self.add_person_image = Tk.PhotoImage(file="add_person.png")
        self.add_person_image = Tk.PhotoImage(file='add_person.gif')
        self.button = Tk.Button(self.toolbar, image=self.add_person_image, command=self.add_person)
        self.button.pack(side="left", padx=2, pady=2)
        
        self.separator1 = ttk.Separator(self.toolbar, orient=Tk.VERTICAL)
        self.separator1.pack(side="left", padx=2, fill=Tk.BOTH)
        
        #=================================================================================================
        
        self.tabControl = ttk.Notebook(master)          # Create Tab Control
        self.tabControl.pack(expand=1, fill="both")  # Pack to make visible
        self.style = ttk.Style()
        self.style.configure(".", font=('Helvetica', 8), foreground="black")
        self.style.configure("Treeview", foreground='black')
        

        self.tab1 = ttk.Frame(self.tabControl)
        #tab1.grid(column=1,row=1,sticky='news')            # Create a tab 
        self.tabControl.add(self.tab1, text='To do')
        self.tab1.dataCols = ("First Name", "Last Name", "Status", "Relationship")
        self.create_columns(self.tab1.dataCols, self.tab1)      # Add the tab
        
        #=================================================================================================
        # Create Tab Control
        
        self.tab2 = ttk.Frame(self.tabControl)            # Create a tab 
        self.tabControl.add(self.tab2, text='Invited')      # Add the tab
        self.label2 = Tk.Label(self.tab2, text="Denver")
        self.label2.grid(row=1, column=0)
        
        #=================================================================================================
        #Creating Methods
        #=================================================================================================
    
    def create_columns(self, dataCols, tab):
        # Adding the Columns for organization
        self.columns_tab1 = ttk.Frame(tab)
        self.columns_tab1.pack(side=Tk.TOP, fill=Tk.BOTH, expand=Tk.Y)
        
        # create the tree and scrollbars
        self.dataCols = dataCols       
        self.tree = ttk.Treeview(columns=self.dataCols, show= 'headings')
        
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
        self.load_people_data()
        
    def load_people_data(self):
        self.data = []
        # add data to the tree 
        sql = "SELECT firstname, lastname, status, relationship FROM people"
        self.res = self.cursor.execute(sql)
        for self.row in self.res:
            self.firstname = self.row[0]
            self.lastname = self.row[1]
            # self.address = self.row[2]
            self.relationship = self.row[2]
            self.status = self.row[3]
            self.data.append([self.firstname, self.lastname, self.status, self.relationship])
        
        
        for item in self.data: 
            self.tree.insert('', 'end', values=item)

    def add_person_window(self):
        self.t = Tk.Toplevel(self)
        self.t.wm_title("Window")
        self.t.geometry("400x400")
        
        self.toolbar1 = Tk.Frame(self.t, bd=1, relief=Tk.RAISED)
        
        self.toolbar1.pack(side="top", fill=Tk.X)
        self.n_label = Tk.Label(self.t, text="First:")
        self.n_label.place(x=0, y=50)
        self.n_ent = Tk.Entry(self.t, width=30)
        self.n_ent.place(x=50, y=50)
        
        self.ln_label = Tk.Label(self.t, text="Last:")
        self.ln_label.place(x=0, y=75)
        self.ln_ent = Tk.Entry(self.t, width=30)
        self.ln_ent.place(x=50, y=75)

        self.address_label = Tk.Label(self.t, text="Address:")
        self.address_label.place(x=0, y=100)
        self.address_text = Tk.Text(self.t, height=3, width=30)
        self.address_text.place(x=50, y=100)

        self.var1 = Tk.StringVar(self.t)
        self.relationship_label = Tk.Label(self.t, text="Relation:")
        self.relationship_label.place(x=0, y=155)
        self.relationship_listbox = Tk.OptionMenu(self.t, self.var1, " ", "Coming", "Not Coming")
        self.var1.set("Invited")
        self.relationship_listbox.place(x=50, y=155)
        
        self.var2 = Tk.StringVar(self.t)
        self.status_label = Tk.Label(self.t, text="Status:")
        self.status_label.place(x=0, y=185)
        self.status_listbox = Tk.OptionMenu(self.t, self.var2, "Invited", "Might Invite", "Coming", "Not Coming")
        self.var2.set("Invited")
        self.status_listbox.place(x=50, y=185)
        
        self.nbutton = Tk.Button(self.toolbar1, text="Save", height=2, width=5, command=self.save_person_db)
        self.nbutton.pack(side="left", padx=2, pady=2)

    def double_click(self, event):
        '''  set the double click status flag
        '''
        global double_click_flag
        double_click_flag = True
        print "You did it"
        
    
    def add_person(self):
        self.add_person_window()

    def save_person_db(self):
        self.var1 = self.n_ent.get() # Get firstname
        self.var2 = self.ln_ent.get() # Get Lastname
        self.var3 = self.address_text.get() # Get address
        self.var4 = self.nent.get() # Get relationship
        self.var5 = self.nent.get() # Get Status
        
        sql = "INSERT INTO people (firstname, lastname, address, relationship, status) VALUES (?,?,?,?,?)"
        self.res = cursor.execute(sql, (self.input,))
        self.conn.commit()
        
        sql = "SELECT firstname, lastname, status, relationship FROM people WHERE firstname=?"
        self.res = self.cursor.execute(sql, (self.input,))
        for self.row in self.res:
            self.firstname = self.row[0]
            self.lastname = self.row[1]
            self.status = self.row[2]
            self.relationship = self.row[3]
            self.tree.insert('', 'end', values=[self.firstname, self.lastname, self.status, self.relationship])
        
    def quit(self):
        self.master.destroy()
        self.cursor.close()
        del self.cursor
        self.conn.close()
        
def main():     
        
    win = Tk.Tk()
    app = Application(win)
    win.protocol("WM_DELETE_WINDOW", app.quit)
    win.mainloop()                     
    
   
main()
            
            
            



    

        
       
        
        
        



    
