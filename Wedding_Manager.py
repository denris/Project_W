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
        
        master.geometry("1500x800")                           # Create instance      
        master.title("Wedding Central")
        master.configure(background="gray")                 # Add a title 
        
        #=================================================================================================
        # Establish Database Connection
        self.conn = sqlite3.connect("W_management.db") # or use :memory: to put it in RAM
        self.cursor = self.conn.cursor()
        self.jobs = ["Photographer", "Server", "Sermon", "Git Receiver"]
        self.total_cost = 0.00
        self.budget = 0.00
        # Setting flag for sorting columns
        self.Sorted = True

        # Create these tables if they don't already exist
        try:
            self.cursor.execute("""CREATE TABLE couple(hisname text, hername text)""")
            self.cursor.execute("""CREATE TABLE relations(hisdadside text, herdadside text, hismomside text, hermomside text)""")
            self.cursor.execute("""CREATE TABLE people(ID integer PRIMARY KEY AUTOINCREMENT, firstname text, lastname text, address text, phone text, relationship text, family text,\
                                numberofpeople int, status text, job text, tablenumber int, notes text)""")
            self.conn.commit()
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
        
        self.toolbar = Tk.Frame(master, bd=1, background="gray25", relief=Tk.RAISED)
        self.toolbar.pack(anchor="n", fill=Tk.X)
        
        self.add_person_image = Tk.PhotoImage(file='add_person.gif')
        self.button = Tk.Button(self.toolbar, image=self.add_person_image, highlightbackground="gray25", command=self.add_person)
        self.button.pack(side="left",)
        
        self.separator1 = ttk.Separator(self.toolbar, orient=Tk.VERTICAL)
        self.separator1.pack(side="left", padx=1, fill=Tk.BOTH)
        
        #========================Main Frame=========================================================================
       
        self.main_frame = Tk.Frame(master, background="black")
        self.main_frame.pack(expand=1, fill=Tk.BOTH)

        self.bottom_frame = Tk.Frame(master, height=25, background="gray25")
        self.bottom_frame.pack(side="bottom", fill=Tk.X)
        
        ### Fill bottom_frame ###
        self.total_cost_price_label = Tk.Label(self.bottom_frame, text="${:.2f}".format(self.total_cost), foreground="white", background="gray25", font=("Arial", 10,"bold"))
        self.total_cost_price_label.pack(side="right")
        self.total_cost_label = Tk.Label(self.bottom_frame, text="Total Cost:", foreground="white", background="gray25", font=("Arial", 10,"bold"))
        self.total_cost_label.pack(side="right")
        

        self.budget_label = Tk.Label(self.bottom_frame, text="Budget: ${:.2f}".format(self.budget), foreground="white", background="gray25", font=("Arial", 10,"bold"))
        self.budget_label.pack(side="left")
        if self.total_cost <= self.budget:
            self.total_cost_price_label.configure(fg="green")
        else:
            self.total_cost_price_label.configure(fg="red")
        #=================================================================================================
        self.search_frame = Tk.Frame(self.main_frame, background="black")
        self.search_frame.pack(anchor="n", fill=Tk.X, pady=5)
        self.search_label = Tk.Label(self.search_frame, text="Search:", font=("Arial", 11), background="black", foreground="white")
        self.search_label.pack(side="left")
        self.search = Tk.Entry(self.search_frame)
        self.search.pack(anchor="w", fill=Tk.X, pady=2)

        self.search.bind("<Return>", self.search_db)
        #=================================================================================================
        
        self.tabControl = ttk.Notebook(self.main_frame)          # Create Tab Control
        self.tabControl.pack(expand=1, fill=Tk.BOTH)  # Pack to make visible
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(".", font=("Times", 12), size=2, foreground="white", background="gray25")
        self.style.configure("Treeview", foreground='white', fieldbackground="black", background="black")
        self.style.configure("TButton", font=("Ariel", 8, 'bold', 'italic'), relief="sunken")
        self.style.configure("TNotebook", background="black")
        self.style.configure("TNotebook.Tab", tabcolor="white", background="black")
        
        
        self.all_people_tab = ttk.Frame(self.tabControl) 
        self.tabControl.add(self.all_people_tab, text='All')
        self.people_dataCols = ("First Name", "Last Name", "Phone Number", "Num of People", "Status", "Job", "Relationship")
        
        # Adding Frames for the Columns for organization
        self.all_people_columns = ttk.Frame(self.all_people_tab)
        
        # create the tree and scrollbars
             
        self.all_people = ttk.Treeview(columns=self.people_dataCols, show= 'headings')
             
        self.create_columns(self.people_dataCols, self.all_people_columns, self.all_people)      # Add the tab
        
        #===========================Creating Tab Control======================================================================
        
        self.family_tab = ttk.Frame(self.tabControl)            # Create a tab 
        self.tabControl.add(self.family_tab, text='Family')      # Add the tab
        
        self.family_columns = ttk.Frame(self.family_tab)

        self.family_people = ttk.Treeview(columns=self.people_dataCols, show= 'headings')

        self.create_columns(self.people_dataCols, self.family_columns, self.family_people)
        #========================Creating Methods=========================================================================
    
    def create_columns(self, dataCols, columns, tree):
        columns.pack(side=Tk.TOP, fill=Tk.BOTH, expand=Tk.Y)
        ysb = ttk.Scrollbar(orient=Tk.VERTICAL, command= tree.yview)
        xsb = ttk.Scrollbar(orient=Tk.HORIZONTAL, command= tree.xview)
        tree['yscroll'] = ysb.set
        tree['xscroll'] = xsb.set
        tree.tag_configure("Invited", foreground='purple')
        tree.tag_configure("Coming", foreground='darkgreen')
        # add tree and scrollbars to frame
        tree.grid(in_=columns, row=0, column=0, sticky=Tk.NSEW)
        ysb.grid(in_=columns, row=0, column=1, sticky=Tk.NS)
        xsb.grid(in_=columns, row=1, column=0, sticky=Tk.EW)
        
        # set frame resize priorities
        columns.rowconfigure(0, weight=1)
        columns.columnconfigure(0, weight=1)
        
        for n in dataCols:
            tree.heading(n, text=n.title(), command=lambda n=n: self.sort_data(tree, n, self.Sorted))
        
        self.load_people_data()
        tree.bind("<Double-1>", lambda event, arg=tree: self.OnDoubleClick(event, arg))
        tree.bind("<Return>", lambda event, arg=tree: self.OnDoubleClick(event, arg))
        
    def load_people_data(self):
        # Clear the tree
        self.all_people.delete(*self.all_people.get_children())
        
        # add data to the tree 
        sql = "SELECT firstname, lastname, phone, numberofpeople, status, job, relationship FROM people"
        res = self.cursor.execute(sql)
        self.conn.commit()
        for row in res:
            firstname = row[0]
            lastname = row[1]
            phone = row[2]
            numberofpeople = row[3]
            status = row[4]
            job = row[5]
            relationship = row[6]
            
            
            self.all_people.insert('', 'end', tags = [status], values=[firstname, lastname, phone, numberofpeople, status, job, relationship])
            
            try: 
                if family != "None":
                    self.family_people.insert('', 'end', tags = [status], values=[firstname, lastname, phone, numberofpeople, status, job, relationship])
            except:
                pass

    def sort_data(self, tree, col, descending=False):
        # grab values to sort as a list of tuples (column value, column id)
        # e.g. [('Person1', 'I001'), ('Person2', 'I002'), ('Person3', 'I003')]
        data = [[tree.set(child, col), child] for child in tree.get_children('')]
        
        # reorder data
        # tkinter looks after moving other items in the same row
        data.sort(reverse=descending)
        for indx, item in enumerate(data):
            tree.move(item[1], '', indx)   # item[1] = item Identifier
        
        # reverse sort direction for next sort operation
        self.Sorted =  not descending
                
    def add_person_window(self):
        self.person_window = Tk.Toplevel(self, background="gray12")
        self.person_window.wm_title("Add Person")
        self.person_window.geometry("500x500")
        
        self.sql_fam = "SELECT * FROM relations"
        self.res_fam = self.cursor.execute(self.sql_fam)
        self.conn.commit()
        for self.row in self.res_fam:
            self.his_dad_fam = self.row[0]
            self.her_dad_fam = self.row[1]
            self.his_mom_fam = self.row[2]
            self.her_mom_fam = self.row[3]
            
        self.toolbar1 = Tk.Frame(self.person_window, bd=1, relief=Tk.RAISED, background="gray25")
        
        self.toolbar1.pack(side="top", fill=Tk.X)
        
        self.middle_frame = Tk.Frame(self.person_window, background="gray12")
        self.middle_frame.pack(expand=1, fill=Tk.BOTH)
        
        self.bottom_frame = Tk.Frame(self.person_window, background="gray12")
        self.bottom_frame.pack(expand=1, fill=Tk.BOTH)

        self.n_label = Tk.Label(self.middle_frame, text="First:", foreground="white", background="gray12")
        self.n_label.grid(row=0, column=0, sticky="w")
        self.n_ent = Tk.Entry(self.middle_frame, highlightbackground="gray12", width=20)
        self.n_ent.grid(row=0, column=1, sticky="w")
        
        self.ln_label = Tk.Label(self.middle_frame, text="Last:", foreground="white", background="gray12")
        self.ln_label.grid(row=1, column=0, sticky="w")
        self.ln_ent = Tk.Entry(self.middle_frame, highlightbackground="gray12", width=20)
        self.ln_ent.grid(row=1, column=1, sticky="w")

        self.address_label = Tk.Label(self.middle_frame, text="Address:", foreground="white", background="gray12")
        self.address_label.grid(row=2, column=0, sticky="nw")
        self.address_text = Tk.Text(self.middle_frame, highlightbackground="gray12", height=3, width=30)
        self.address_text.grid(row=2, column=1, sticky="w")

        self.phone_label = Tk.Label(self.middle_frame, text="Phone:", foreground="white", background="gray12")
        self.phone_label.grid(row=3, column=0, sticky="w")
        self.phone_ent = Tk.Entry(self.middle_frame, highlightbackground="gray12", width=20)
        self.phone_ent.grid(row=3, column=1, sticky="w")
        
        self.relation = Tk.StringVar(self.middle_frame)
        self.relationship_label = Tk.Label(self.middle_frame, text="Relation:", foreground="white", background="gray12")
        self.relationship_label.grid(row=4, column=0, sticky="w")
        self.relationship_listbox = Tk.OptionMenu(self.middle_frame, self.relation, "Friend", "Cousin", "Aunt", "Uncle", "Aunt & Uncle", "His " + "Friend")
        self.relationship_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.relation.set("Friend")
        self.relationship_listbox.grid(row=4, column=1, sticky="w")

        self.family = Tk.StringVar(self.middle_frame)
        self.family_label = Tk.Label(self.middle_frame, text="Family:", foreground="white", background="gray12")
        self.family_label.grid(row=5, column=0, sticky="w")
        self.family_listbox = Tk.OptionMenu(self.middle_frame, self.family, "None", self.his_dad_fam, self.her_dad_fam, self.his_mom_fam, self.her_mom_fam)
        self.family_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.family.set("None")
        self.family_listbox.grid(row=5, column=1, sticky="w")

        self.n_coming = Tk.StringVar(self.middle_frame)
        self.n_coming_label = Tk.Label(self.middle_frame, text="Number Coming:", foreground="white", background="gray12")
        self.n_coming_label.grid(row=4, column=1, sticky="e")
        self.n_coming_listbox = Tk.OptionMenu(self.middle_frame, self.n_coming, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        self.n_coming_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=3)
        self.n_coming.set(1)
        self.n_coming_listbox.grid(row=4, column=2, sticky="w")
        
        self.job = Tk.StringVar(self.middle_frame)
        self.jobs_label = Tk.Label(self.middle_frame, text="Job:", foreground="white", background="gray12")
        self.jobs_label.grid(row=0, column=2, sticky="w")
        self.jobs_box = Tk.OptionMenu(self.middle_frame, self.job, *self.jobs)
        self.jobs_box.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.job.set(self.jobs[0])
        self.jobs_box.grid(row=0, column=3, sticky="w")

        self.table = Tk.StringVar(self.middle_frame)
        self.tablenum_label = Tk.Label(self.middle_frame, text="Table:", foreground="white", background="gray12")
        self.tablenum_label.grid(row=5, column=1, sticky="e")
        self.tablenum_box = Tk.OptionMenu(self.middle_frame, self.table, 1, 2)
        self.tablenum_box.configure(highlightbackground="black", background="gray12", foreground="white", width=3)
        self.table.set(100)
        self.tablenum_box.grid(row=5, column=2, sticky="w")
        
        self.status = Tk.StringVar(self.middle_frame)
        self.status_label = Tk.Label(self.middle_frame, text="Status:", foreground="white", background="gray12")
        self.status_label.grid(row=1, column=2, sticky="w")
        self.status_listbox = Tk.OptionMenu(self.middle_frame, self.status, "Invited", "Might Invite", "Coming", "Not Coming")
        self.status_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.status.set("Invited")
        self.status_listbox.grid(row=1, column=3, sticky="w")

        self.people_nlabel = Tk.Label(self.bottom_frame, text="Notes:", foreground="white", background="gray12")
        self.people_nlabel.pack(side="top", anchor="w")
        self.people_ntext = Tk.Text(self.bottom_frame, height=10)
        self.people_ntext.pack(expand=1, fill=Tk.BOTH)

        self.save_image = Tk.PhotoImage(file="save.gif")
        self.sbutton = Tk.Button(self.toolbar1, text="Save", font=("Arial", 12, "bold", "italic"), highlightbackground="gray25", command=self.save_person_db)
        self.sbutton.pack(side="left")

    def update_view_person_window(self, firstname, lastname, address, phone, relationship, family, numofpep, status, job, table, notes):
        self.view_person = Tk.Toplevel(self, takefocus=True)
        self.view_person.wm_title("View/Update")
        self.view_person.geometry("500x500")
        
        
        self.sql_fam = "SELECT * FROM relations"
        self.res_fam = self.cursor.execute(self.sql_fam)
        self.conn.commit()
        for self.row in self.res_fam:
            self.his_dad_fam = self.row[0]
            self.her_dad_fam = self.row[1]
            self.his_mom_fam = self.row[2]
            self.her_mom_fam = self.row[3]
            
        self.toolbar1 = Tk.Frame(self.view_person, bd=1, relief=Tk.RAISED, background="gray25")
        
        self.toolbar1.pack(side="top", fill=Tk.X)
        
        self.middle_frame = Tk.Frame(self.view_person, background="gray12")
        self.middle_frame.pack(expand=1, fill=Tk.BOTH)
        
        self.bottom_frame = Tk.Frame(self.view_person, background="gray12")
        self.bottom_frame.pack(expand=1, fill=Tk.BOTH)

        self.n_label = Tk.Label(self.middle_frame, text="First:", foreground="white", background="gray12")
        self.n_label.grid(row=0, column=0, sticky="w")
        self.n_ent = Tk.Entry(self.middle_frame, highlightbackground="gray12", width=20)
        self.n_ent.grid(row=0, column=1, sticky="w")
        
        self.ln_label = Tk.Label(self.middle_frame, text="Last:", foreground="white", background="gray12")
        self.ln_label.grid(row=1, column=0, sticky="w")
        self.ln_ent = Tk.Entry(self.middle_frame, highlightbackground="gray12", width=20)
        self.ln_ent.grid(row=1, column=1, sticky="w")

        self.address_label = Tk.Label(self.middle_frame, text="Address:", foreground="white", background="gray12")
        self.address_label.grid(row=2, column=0, sticky="nw")
        self.address_text = Tk.Text(self.middle_frame, highlightbackground="gray12", height=3, width=30)
        self.address_text.grid(row=2, column=1, sticky="w")

        self.phone_label = Tk.Label(self.middle_frame, text="Phone:", foreground="white", background="gray12")
        self.phone_label.grid(row=3, column=0, sticky="w")
        self.phone_ent = Tk.Entry(self.middle_frame, highlightbackground="gray12", width=20)
        self.phone_ent.grid(row=3, column=1, sticky="w")
        
        self.relation = Tk.StringVar(self.middle_frame)
        self.relationship_label = Tk.Label(self.middle_frame, text="Relation:", foreground="white", background="gray12")
        self.relationship_label.grid(row=4, column=0, sticky="w")
        self.relationship_listbox = Tk.OptionMenu(self.middle_frame, self.relation, "Friend", "Cousin", "Aunt", "Uncle", "Aunt & Uncle", "His " + "Friend")
        self.relationship_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.relation.set("Friend")
        self.relationship_listbox.grid(row=4, column=1, sticky="w")

        self.family = Tk.StringVar(self.middle_frame)
        self.family_label = Tk.Label(self.middle_frame, text="Family:", foreground="white", background="gray12")
        self.family_label.grid(row=5, column=0, sticky="w")
        self.family_listbox = Tk.OptionMenu(self.middle_frame, self.family, "None", self.his_dad_fam, self.her_dad_fam, self.his_mom_fam, self.her_mom_fam)
        self.family_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.family.set("None")
        self.family_listbox.grid(row=5, column=1, sticky="w")

        self.n_coming = Tk.StringVar(self.middle_frame)
        self.n_coming_label = Tk.Label(self.middle_frame, text="Number Coming:", foreground="white", background="gray12")
        self.n_coming_label.grid(row=4, column=1, sticky="e")
        self.n_coming_listbox = Tk.OptionMenu(self.middle_frame, self.n_coming, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        self.n_coming_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=3)
        self.n_coming.set(1)
        self.n_coming_listbox.grid(row=4, column=2, sticky="w")
        
        self.job = Tk.StringVar(self.middle_frame)
        self.jobs_label = Tk.Label(self.middle_frame, text="Job:", foreground="white", background="gray12")
        self.jobs_label.grid(row=0, column=2, sticky="w")
        self.jobs_box = Tk.OptionMenu(self.middle_frame, self.job, *self.jobs)
        self.jobs_box.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.job.set(self.jobs[0])
        self.jobs_box.grid(row=0, column=3, sticky="w")

        self.table = Tk.StringVar(self.middle_frame)
        self.tablenum_label = Tk.Label(self.middle_frame, text="Table:", foreground="white", background="gray12")
        self.tablenum_label.grid(row=5, column=1, sticky="e")
        self.tablenum_box = Tk.OptionMenu(self.middle_frame, self.table, 1, 2)
        self.tablenum_box.configure(highlightbackground="black", background="gray12", foreground="white", width=3)
        self.table.set(100)
        self.tablenum_box.grid(row=5, column=2, sticky="w")
        
        self.status = Tk.StringVar(self.middle_frame)
        self.status_label = Tk.Label(self.middle_frame, text="Status:", foreground="white", background="gray12")
        self.status_label.grid(row=1, column=2, sticky="w")
        self.status_listbox = Tk.OptionMenu(self.middle_frame, self.status, "Invited", "Might Invite", "Coming", "Not Coming")
        self.status_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.status.set("Invited")
        self.status_listbox.grid(row=1, column=3, sticky="w")

        self.people_nlabel = Tk.Label(self.bottom_frame, text="Notes:", foreground="white", background="gray12")
        self.people_nlabel.pack(side="top", anchor="w")
        self.people_ntext = Tk.Text(self.bottom_frame, height=10)
        self.people_ntext.pack(expand=1, fill=Tk.BOTH)

        self.n_ent.insert(0,firstname)
        self.ln_ent.insert(0, lastname)
        self.address_text.insert(Tk.CURRENT, address)
        self.phone_ent.insert(0, phone)
        self.relation.set(relationship)
        self.family.set(family)
        self.n_coming.set(numofpep)
        self.status.set(status)
        self.job.set(job)
        self.table.set(table)
        self.people_ntext.insert(Tk.CURRENT, notes)

        #self.update_person_image = Tk.PhotoImage(file="update_person.gif")
        self.u_person_but = Tk.Button(self.toolbar1, text="Update", font=("Arial", 12, "bold", "italic"), highlightbackground="gray25",  command=self.update_person_db)
        self.u_person_but.pack(side="left")
    
    def OnDoubleClick(self, event, tree):
        # So double clicking heads don't throw error
        try:
            selection = tree.item(tree.selection())['values'][0]
            selection1 = tree.item(tree.selection())['values'][1]
            sql = "SELECT ID FROM people WHERE firstname=(?) AND lastname=(?)"
            self.id = self.cursor.execute(sql, (selection, selection1))
            self.conn.commit()
            sql = "SELECT * FROM people WHERE ID=(?)"
            for row in self.id:
                self.rowid = row
            view = self.cursor.execute(sql, (self.rowid))
            self.conn.commit()
            
            for info in view:
                view_first = info[1]
                view_last = info[2]
                view_addr = info[3]
                view_phone = info[4]
                view_relation = info[5]
                view_fam = info[6]
                view_numofpep = info[7]
                view_stat = info[8]
                view_job = info[9]
                view_table = info[10]
                view_notes = info[11]
                
                self.update_view_person_window(info[1], info[2], info[3], info[4], info[5], \
                                        info[6], info[7], info[8], info[9], info[10], info[11])
        except:
            pass

    def save_person_db(self):
        var_n = self.n_ent.get() # Get firstname
        var_ln = self.ln_ent.get() # Get Lastname
        var_address = self.address_text.get("1.0", Tk.END) # Get address
        var_phone = self.phone_ent.get()
        var_relationship = self.relation.get() # Get relationship
        var_fam = self.family.get() # Get Family
        var_numofpep = self.n_coming.get() # Get number Coming
        var_status = self.status.get() # Get Status
        var_job = self.job.get() # Get Job
        var_tablenum = self.table.get()
        var_notes = self.people_ntext.get("1.0", Tk.END) # Get Notes
        
        sql = "INSERT INTO people (firstname, lastname, address, phone, relationship, family, numberofpeople, status, job, tablenumber, notes) VALUES (?,?,?,?,?,?,?,?,?,?,?)"
        res = self.cursor.execute(sql, (var_n, var_ln, var_address, var_phone, var_relationship, var_fam, var_numofpep, var_status, var_job, var_tablenum, var_notes))
        self.conn.commit()
        
        # Update Tree
        self.family_people.delete(*self.family_people.get_children())
        self.all_people.delete(*self.all_people.get_children())
        self.load_people_data()
        
        
        #self.destroy_window(self.person_window)

    def save_cupfam_db(self):
        self.his_name = self.his_ent.get()
        self.her_name = self.her_ent.get()
        self.his_dadside_fam = self.his_dadside_ent.get()
        self.her_dadside_fam = self.her_dadside_ent.get()
        self.his_momside_fam = self.his_momside_ent.get()
        self.her_momside_fam = self.her_momside_ent.get()
        
        sql = "INSERT INTO couple(hisname, hername) VALUES (?,?)"
        self.ins_cup = self.cursor.execute(sql, (self.his_name, self.her_name,))
        self.conn.commit()

        sql2 = "INSERT INTO relations(hisdadside, herdadside, hismomside, hermomside) VALUES (?,?,?,?)"
        self.ins_fam2 = self.cursor.execute(sql2, (self.his_dadside_fam, self.her_dadside_fam, self.his_momside_fam, self.her_momside_fam))
        self.conn.commit()
        self.destroy_window(self.message_window)

    def update_person_db(self):
        var_n = self.n_ent.get() # Get firstname
        var_ln = self.ln_ent.get() # Get Lastname
        var_address = self.address_text.get("1.0", Tk.END) # Get address
        var_phone = self.phone_ent.get()
        var_relationship = self.relation.get() # Get relationship
        var_fam = self.family.get() # Get Family
        var_numofpep = self.n_coming.get() # Get number Coming
        var_status = self.status.get() # Get Status
        var_job = self.job.get() # Get Job
        var_tablenum = self.table.get()
        var_notes = self.people_ntext.get("1.0", Tk.END) # Get Notes
        
        sql = "UPDATE people SET firstname=(?), lastname=(?), address=(?), phone=(?), relationship=(?), family=(?), numberofpeople=(?), status=(?), job=(?), tablenumber=(?), notes=(?) WHERE ID=(?)"
        res = self.cursor.execute(sql, (var_n, var_ln, var_address, var_phone, var_relationship, var_fam, var_numofpep, var_status, var_job, var_tablenum, var_notes, self.rowid[0]))
        self.conn.commit()
        
        self.family_people.delete(*self.family_people.get_children())
        self.all_people.delete(*self.all_people.get_children())
        self.load_people_data()

    def search_db(self, event):
        results = self.search.get()
        sql = "Select * FROM sqlite_master WHERE type='table'"
        res = self.cursor.execute(sql)
        self.conn.commit()
        for tablerow in res.fetchall():
            table = tablerow
            print table
    def add_person(self):
        self.add_person_window()
        
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
