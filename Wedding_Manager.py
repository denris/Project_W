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
        master.title("Wedding Central")                 # Add a title 
        
        #=================================================================================================
        # Establish Database Connection
        self.conn = sqlite3.connect("W_management.db") # or use :memory: to put it in RAM
        self.cursor = self.conn.cursor()
        self.jobs = ["Photographer", "Server", "Sermon"]
        
        # Create these tables if they don't already exist
        try:
            self.cursor.execute("""CREATE TABLE couple(hisname text, hername text)""")
            self.cursor.execute("""CREATE TABLE relations(hisdadside text, herdadside text, hismomside text, hermomside text)""")
            self.cursor.execute("""CREATE TABLE people(ID integer PRIMARY KEY AUTOINCREMENT, firstname text, lastname text, address text, relationship text, family text,\
                                numberofpeople int, status text, job text, tablenumber int, notes text)""")
            self.message = tkMessageBox.showinfo("Title", "Congratulations, who is getting married?")

            self.message_window = Tk.Toplevel(self)
            self.message_window.wm_title("Enter Names & Families")
            self.message_window.geometry("325x185")
            
            ### Label for couples Names
            self.top_label = Tk.Label(self.message_window, font=("Helvetica", 10, "bold italic"), text="Couple's Names")
            self.top_label.place(x=0, y=3)
            self.sep_top = ttk.Separator(self.message_window, orient=Tk.HORIZONTAL)
            self.sep_top.place(x=9, y=23, width=305)
            self.sep_left = ttk.Separator(self.message_window, orient=Tk.VERTICAL)
            self.sep_left.place(x=9, y=23, height=33)
            self.sep_right = ttk.Separator(self.message_window, orient=Tk.VERTICAL)
            self.sep_right.place(x=315, y=23, height=33)
            self.sep_bot = ttk.Separator(self.message_window, orient=Tk.HORIZONTAL)
            self.sep_bot.place(x=9, y=55, width=305)
            
            self.his_label = Tk.Label(self.message_window, text="His Name:")
            self.his_label.place(x=10, y=30)
            self.his_ent = Tk.Entry(self.message_window, width=15)
            self.his_ent.place(x=70, y=30)
            
            self.her_label = Tk.Label(self.message_window, text="Her Name:")
            self.her_label.place(x=152, y=30)
            self.her_ent = Tk.Entry(self.message_window, width=15)
            self.her_ent.place(x=218, y=30)
            
            #=======================Label for Family Names==============================================================
            self.bot_label = Tk.Label(self.message_window, font=("Helvetica", 10, "bold italic"), text="Family Names")
            self.bot_label.place(x=0, y=60)
            self.bot_sep_top = ttk.Separator(self.message_window, orient=Tk.HORIZONTAL)
            self.bot_sep_top.place(x=9, y=80, width=305)
            self.bot_sep_left = ttk.Separator(self.message_window, orient=Tk.VERTICAL)
            self.bot_sep_left.place(x=9, y=80, height=61)
            self.bot_sep_right = ttk.Separator(self.message_window, orient=Tk.VERTICAL)
            self.bot_sep_right.place(x=315, y=80, height=61)
            self.bot_sep_bot = ttk.Separator(self.message_window, orient=Tk.HORIZONTAL)
            self.bot_sep_bot.place(x=9, y=140, width=305)
            
            self.his_dadside = Tk.Label(self.message_window, text="His Dad's:")
            self.his_dadside.place(x=10, y=87)
            self.his_dadside_ent = Tk.Entry(self.message_window, width=15)
            self.his_dadside_ent.place(x=73, y=87)
            
            self.her_dadside = Tk.Label(self.message_window, text="Her Dad's:")
            self.her_dadside.place(x=152, y=87)
            self.her_dadside_ent = Tk.Entry(self.message_window, width=15)
            self.her_dadside_ent.place(x=218, y=87)
            
            self.his_momside = Tk.Label(self.message_window, text="His Mom's:")
            self.his_momside.place(x=10, y=117)
            self.his_momside_ent = Tk.Entry(self.message_window, width=15)
            self.his_momside_ent.place(x=73, y=117)

            self.her_momside = Tk.Label(self.message_window, text="Her Mom's:")
            self.her_momside.place(x=152, y=117)
            self.her_momside_ent = Tk.Entry(self.message_window, width=15)
            self.her_momside_ent.place(x=218, y=117)
            
            self.cupfamily_b = Tk.Button(self.message_window, text="Submit", command=self.save_cupfam_db)
            self.cupfamily_b.place(x=265,y=150)
            
        except:
            pass
            
        #==========================Define our Application================================================
        
        self.toolbar = Tk.Frame(master, bd=1, relief=Tk.RAISED)
        self.toolbar.pack(anchor="n", fill=Tk.X)
        
        self.add_person_image = Tk.PhotoImage(file='add_person.gif')
        self.button = Tk.Button(self.toolbar, image=self.add_person_image, command=self.add_person, relief="flat")
        self.button.pack(side="left", padx=2, pady=2)
        
        self.button.bind("<Enter>", lambda event: self.button.configure(bg="darkgreen"))
        self.button.bind("<Leave>", lambda event: self.button.configure(bg="white"))
        
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
        self.tabControl.add(self.tab1, text='All')
        self.tab1.dataCols = ("First Name", "Last Name", "Relationship", "Status")
        self.create_columns(self.tab1.dataCols, self.tab1)      # Add the tab
        
        #===========================Creating Tab Control======================================================================
        
        self.tab2 = ttk.Frame(self.tabControl)            # Create a tab 
        self.tabControl.add(self.tab2, text='Invited')      # Add the tab
        self.label2 = Tk.Label(self.tab2, text="Denver")
        self.label2.grid(row=1, column=0)
        
        #========================Creating Methods=========================================================================
    
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
        
        self.tree.bind("<Double-1>", self.OnDoubleClick)
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
            self.tree.insert('', 'end', text=item[0], values=item)

    def add_person_window(self):
        self.person_window = Tk.Toplevel(self)
        self.person_window.wm_title("Add Person")
        self.person_window.geometry("450x400")
        
        self.sql_fam = "SELECT * FROM relations"
        self.res_fam = self.cursor.execute(self.sql_fam)
        for self.row in self.res_fam:
            self.his_dad_fam = self.row[0]
            self.her_dad_fam = self.row[1]
            self.his_mom_fam = self.row[2]
            self.her_mom_fam = self.row[3]
            
        self.toolbar1 = Tk.Frame(self.person_window, bd=1, relief=Tk.RAISED)
        
        self.toolbar1.pack(side="top", fill=Tk.X)
        self.n_label = Tk.Label(self.person_window, text="First:")
        self.n_label.place(x=0, y=50)
        self.n_ent = Tk.Entry(self.person_window, width=30)
        self.n_ent.place(x=50, y=50)
        
        self.ln_label = Tk.Label(self.person_window, text="Last:")
        self.ln_label.place(x=0, y=75)
        self.ln_ent = Tk.Entry(self.person_window, width=30)
        self.ln_ent.place(x=50, y=75)

        self.address_label = Tk.Label(self.person_window, text="Address:")
        self.address_label.place(x=0, y=100)
        self.address_text = Tk.Text(self.person_window, height=3, width=30)
        self.address_text.place(x=50, y=100)

        self.relation = Tk.StringVar(self.person_window)
        self.relationship_label = Tk.Label(self.person_window, text="Relation:")
        self.relationship_label.place(x=0, y=155)
        self.relationship_listbox = Tk.OptionMenu(self.person_window, self.relation, "Friend", "Cousin", "Aunt", "Uncle", "Aunt & Uncle", "His " + "Friend")
        self.relation.set("Friend")
        self.relationship_listbox.place(x=50, y=155)

        self.family = Tk.StringVar(self.person_window)
        self.family_label = Tk.Label(self.person_window, text="Family:")
        self.family_label.place(x=150, y=155)
        self.family_listbox = Tk.OptionMenu(self.person_window, self.family, "None", self.his_dad_fam, self.her_dad_fam, self.his_mom_fam, self.her_mom_fam)
        self.family.set("None")
        self.family_listbox.place(x=195, y=155)

        self.n_coming = Tk.StringVar(self.person_window)
        self.n_coming_label = Tk.Label(self.person_window, text="Number Coming:")
        self.n_coming_label.place(x=150, y=185)
        self.n_coming_listbox = Tk.OptionMenu(self.person_window, self.n_coming, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        self.n_coming.set(1)
        self.n_coming_listbox.place(x=250, y=185)
        
        self.job = Tk.StringVar(self.person_window)
        self.jobs_label = Tk.Label(self.person_window, text="Job:")
        self.jobs_label.place(x=300, y=50)
        self.jobs_box = Tk.OptionMenu(self.person_window, self.job, self.jobs[0], self.jobs[1], self.jobs[2])
        self.job.set(self.jobs[0])
        self.jobs_box.place(x=325, y=50)

        self.table = Tk.StringVar(self.person_window)
        self.tablenum_label = Tk.Label(self.person_window, text="Table:")
        self.tablenum_label.place(x=300, y=80)
        self.tablenum_box = Tk.OptionMenu(self.person_window, self.table, 1, 2)
        self.table.set(100)
        self.tablenum_box.place(x=335, y=80)
        
        self.status = Tk.StringVar(self.person_window)
        self.status_label = Tk.Label(self.person_window, text="Status:")
        self.status_label.place(x=0, y=185)
        self.status_listbox = Tk.OptionMenu(self.person_window, self.status, "Invited", "Might Invite", "Coming", "Not Coming")
        self.status.set("Invited")
        self.status_listbox.place(x=50, y=185)

        self.people_nlabel = Tk.Label(self.person_window, text="Notes:")
        self.people_nlabel.place(x=0, y=215)
        self.people_ntext = Tk.Text(self.person_window, height=10)
        self.people_ntext.pack(side="bottom", fill=Tk.X)

        self.sbutton = Tk.Button(self.toolbar1, text="Save", height=2, width=5, command=self.save_person_db)
        self.sbutton.pack(side="left", padx=2, pady=2)

    
    def OnDoubleClick(self, event):
        self.selection = self.tree.item(self.tree.selection())['values'][0]
        self.selection1 = self.tree.item(self.tree.selection())['values'][1]
        sql = "SELECT ID FROM people WHERE firstname=(?) AND lastname=(?)"
        self.id = self.cursor.execute(sql, (self.selection, self.selection1))
        sql = "SELECT * FROM people WHERE ID=(?)"
        for self.row in self.id:
             rowid = self.row
        self.view = self.cursor.execute(sql, (rowid))
        
        for self.info in self.view:
            self.view_first = self.info[1]
            self.view_last = self.info[2]
            self.view_addr = self.info[3]
            self.view_relation = self.info[4]
            self.view_fam = self.info[5]
            self.view_numofpep = self.info[6]
            self.view_stat = self.info[7]
            self.view_job = self.info[8]
            self.view_table = self.info[9]
            self.view_notes = self.info[10]
            
            self.update_view_person_db(self.info[1], self.info[2], self.info[3], self.info[4], self.info[5], \
                                       self.info[6], self.info[7], self.info[8], self.info[9], self.info[10])
        
    
    def save_person_db(self):
        self.var_n = self.n_ent.get() # Get firstname
        self.var_ln = self.ln_ent.get() # Get Lastname
        self.var_address = self.address_text.get("1.0", Tk.END) # Get address
        self.var_relationship = self.relation.get() # Get relationship
        self.var_fam = self.family.get() # Get Family
        self.var_numofpep = self.n_coming.get() # Get number Coming
        self.var_status = self.status.get() # Get Status
        self.var_job = self.job.get() # Get Job
        self.var_tablenum = self.table.get()
        self.var_notes = self.people_ntext.get("1.0", Tk.END) # Get Notes
        
        sql = "INSERT INTO people (firstname, lastname, address, relationship, family, numberofpeople, status, job, tablenumber, notes) VALUES (?,?,?,?,?,?,?,?,?,?)"
        self.res = self.cursor.execute(sql, (self.var_n, self.var_ln, self.var_address, self.var_relationship, self.var_fam, self.var_numofpep, self.var_status, self.var_job, self.var_tablenum, self.var_notes))
        self.conn.commit()
        
        sql = "SELECT firstname, lastname, status, relationship FROM people WHERE firstname=?"
        self.res = self.cursor.execute(sql, (self.var_n,))
        for self.row in self.res:
            self.firstname = self.row[0]
            self.lastname = self.row[1]
            self.status = self.row[2]
            self.relationship = self.row[3]
            self.tree.insert('', 'end', text=self.firstname ,values=[self.firstname, self.lastname, self.status, self.relationship])
        
        self.destroy_window(self.person_window)

    def save_cupfam_db(self):
        self.his_name = self.his_ent.get()
        self.her_name = self.her_ent.get()
        self.his_dadside_fam = self.his_dadside_ent.get()
        self.her_dadside_fam = self.her_dadside_ent.get()
        self.his_momside_fam = self.his_momside_ent.get()
        self.her_momside_fam = self.her_momside_ent.get()
        
        sql = "INSERT INTO couple(hisname, hername) VALUES (?,?)"
        self.ins_cup = self.cursor.execute(sql, (self.his_name, self.her_name,))

        sql2 = "INSERT INTO relations(hisdadside, herdadside, hismomside, hermomside) VALUES (?,?,?,?)"
        self.ins_fam2 = self.cursor.execute(sql2, (self.his_dadside_fam, self.her_dadside_fam, self.his_momside_fam, self.her_momside_fam))
        self.conn.commit()
        self.destroy_window(self.message_window)

    def update_view_person_db(self, firstname, lastname, address, relationship, family, numofpep, status, job, table, notes):
        self.view_person = Tk.Toplevel(self, takefocus=True)
        self.view_person.wm_title("View/Update")
        self.view_person.geometry("450x400")
        
        
        self.sql_fam = "SELECT * FROM relations"
        self.res_fam = self.cursor.execute(self.sql_fam)
        for self.row in self.res_fam:
            self.his_dad_fam = self.row[0]
            self.her_dad_fam = self.row[1]
            self.his_mom_fam = self.row[2]
            self.her_mom_fam = self.row[3]
            
        self.toolbar1 = Tk.Frame(self.view_person, bd=1, relief=Tk.RAISED)
        
        self.toolbar1.pack(side="top", fill=Tk.X)
        self.n_label = Tk.Label(self.view_person, text="First:")
        self.n_label.place(x=0, y=50)
        self.n_ent = Tk.Entry(self.view_person, width=30)
        self.n_ent.place(x=50, y=50)
        
        self.ln_label = Tk.Label(self.view_person, text="Last:")
        self.ln_label.place(x=0, y=75)
        self.ln_ent = Tk.Entry(self.view_person, width=30)
        self.ln_ent.place(x=50, y=75)

        self.address_label = Tk.Label(self.view_person, text="Address:")
        self.address_label.place(x=0, y=100)
        self.address_text = Tk.Text(self.view_person, height=3, width=30)
        self.address_text.place(x=50, y=100)

        self.relation = Tk.StringVar(self.view_person)
        self.relationship_label = Tk.Label(self.view_person, text="Relation:")
        self.relationship_label.place(x=0, y=155)
        self.relationship_listbox = Tk.OptionMenu(self.view_person, self.relation, "Friend", "Cousin", "Aunt", "Uncle", "Aunt & Uncle", "His " + "Friend")
        self.relation.set("Friend")
        self.relationship_listbox.place(x=50, y=155)

        self.family = Tk.StringVar(self.view_person)
        self.family_label = Tk.Label(self.view_person, text="Family:")
        self.family_label.place(x=150, y=155)
        self.family_listbox = Tk.OptionMenu(self.view_person, self.family, "None", self.his_dad_fam, self.her_dad_fam, self.his_mom_fam, self.her_mom_fam)
        self.family.set("None")
        self.family_listbox.place(x=195, y=155)

        self.n_coming = Tk.StringVar(self.view_person)
        self.n_coming_label = Tk.Label(self.view_person, text="Number Coming:")
        self.n_coming_label.place(x=150, y=185)
        self.n_coming_listbox = Tk.OptionMenu(self.view_person, self.n_coming, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        self.n_coming.set(1)
        self.n_coming_listbox.place(x=250, y=185)

        self.job = Tk.StringVar(self.view_person)
        self.jobs_label = Tk.Label(self.view_person, text="Job:")
        self.jobs_label.place(x=300, y=50)
        self.jobs_box = Tk.OptionMenu(self.view_person, self.job, self.jobs[0], self.jobs[1], self.jobs[2])
        self.job.set(self.jobs[0])
        self.jobs_box.place(x=325, y=50)

        self.table = Tk.StringVar(self.view_person)
        self.tablenum_label = Tk.Label(self.view_person, text="Table:")
        self.tablenum_label.place(x=300, y=80)
        self.tablenum_box = Tk.OptionMenu(self.view_person, self.table, 1, 2)
        self.table.set(100)
        self.tablenum_box.place(x=335, y=80)
        
        self.status = Tk.StringVar(self.view_person)
        self.status_label = Tk.Label(self.view_person, text="Status:")
        self.status_label.place(x=0, y=185)
        self.status_listbox = Tk.OptionMenu(self.view_person, self.status, "Invited", "Might Invite", "Coming", "Not Coming")
        self.status.set("Invited")
        self.status_listbox.place(x=50, y=185)

        self.people_nlabel = Tk.Label(self.view_person, text="Notes:")
        self.people_nlabel.place(x=0, y=215)
        self.people_ntext = Tk.Text(self.view_person, height=10)
        self.people_ntext.pack(side="bottom", fill=Tk.X)

        self.n_ent.insert(0,firstname)
        self.ln_ent.insert(0, lastname)
        self.address_text.insert(Tk.CURRENT, address)
        self.relation.set(relationship)
        self.family.set(family)
        self.n_coming.set(numofpep)
        self.status.set(status)
        self.job.set(job)
        self.table.set(table)
        self.people_ntext.insert(Tk.CURRENT, notes)

        self.update_person_image = Tk.PhotoImage(file="update_person.gif")
        self.u_person_but = Tk.Button(self.toolbar1, text="Update", image=self.update_person_image, command=self.update_person_db)
        self.u_person_but.pack(side="left", padx=2, pady=2)
    
    def add_person(self):
        self.add_person_window()

    def update_person_db(self):
        self.var_n = self.n_ent.get() # Get firstname
        self.var_ln = self.ln_ent.get() # Get Lastname
        self.var_address = self.address_text.get("1.0", Tk.END) # Get address
        self.var_relationship = self.relation.get() # Get relationship
        self.var_fam = self.family.get() # Get Family
        self.var_numofpep = self.n_coming.get() # Get number Coming
        self.var_status = self.status.get() # Get Status
        self.var_job = self.job.get() # Get Job
        self.var_tablenum = self.table.get()
        self.var_notes = self.people_ntext.get("1.0", Tk.END) # Get Notes
        
        sql = "UPDATE people SET firstname=(?), lastname=(?), address=(?), relationship=(?), family=(?), numberofpeople=(?), status=(?), job=(?), tablenumber=(?), notes=(?) WHERE firstname=(?) AND lastname=(?)"
        self.res = self.cursor.execute(sql, (self.var_n, self.var_ln, self.var_address, self.var_relationship, self.var_fam, self.var_numofpep, self.var_status, self.var_job, self.var_tablenum, self.var_notes, self.selection, self.selection1))
        self.conn.commit()
        
        self.tree.delete(self.tree.selection())
        self.tree.insert('', 'end', text=self.var_n ,values=[self.var_n, self.var_ln, self.var_status, self.var_relationship])
        self.destroy_window(self.view_person)
        
    def destroy_window(self, window):
        window.destroy()
    
    def quit_main(self):
        self.master.destroy()
        self.cursor.close()
        del self.cursor
        self.conn.close()
    
        
        
def main():     
        
    win = Tk.Tk()
    app = Application(win)
    win.protocol("WM_DELETE_WINDOW", app.quit_main)
    win.mainloop()                     
    
main()
