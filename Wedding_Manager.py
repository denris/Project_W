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
        
        master.geometry("1000x600")    
        master.title("Wedding Central") # Add a title
        master.configure(background="gray")
        #master.attributes('-topmost', 'true')
        
        #=================================================================================================
        
        self.conn = sqlite3.connect("W_management.db") # Establish Database Connection
        self.cursor = self.conn.cursor()
        
        ### Things that will be dynamically populated ###
        self.jobs = []
        self.tables = 0
        self.table_num_pep = 0
        self.stores = []
        self.total_cost = 0.00
        self.str_total_cost = "0.00"
        self.budget = 0.00
        self.str_budget= "0.00"
        self.his = ""
        self.her = ""
        self.his_dad_fam = ""
        self.her_dad_fam = ""
        self.his_mom_fam = ""
        self.her_mom_fam = ""

        self.Sorted = True   # Setting flag for sorting columns
        #=============================Set up Database====================================================================
        try:
            self.cursor.execute("""CREATE TABLE couple(hisname text, hername text)""")  # Create these tables if they don't already exist
            self.cursor.execute("""CREATE TABLE relations(hisdadside text, herdadside text, hismomside text, hermomside text)""")
            self.cursor.execute("""CREATE TABLE people(ID integer PRIMARY KEY AUTOINCREMENT, firstname text, lastname text, address text, phone text, relationship text, family text,\
                                bibleschool int, numberofpeople int, status text, job text, tablenumber int, notes text, CONSTRAINT name_unique UNIQUE (firstname, lastname, address))""")
            self.cursor.execute("""CREATE TABLE items(ID integer PRIMARY KEY AUTOINCREMENT, item text, description text, cost real, quantityneeded int, whereneeded text, buyingstatus text, \
                                importance text, notes text, CONSTRAINT name_unique UNIQUE (description))""")
            self.cursor.execute("""CREATE TABLE tables(people text, remaining int, relationship text, family text, notes text)""")
            self.cursor.execute("""CREATE TABLE budget(budget real, totalcost real)""")
            self.cursor.execute("""CREATE TABLE jobs(job text, CONSTRAINT name_unique UNIQUE (job))""")
            self.cursor.execute("""CREATE TABLE tableinfo(numtables int, numpeptable int)""")
            
            self.conn.commit()

            #self.message = tkMessageBox.showinfo("Title", "Congratulations, who is getting married?")
            
            ### Init cupfam incase somehow info doesn't get entered
            sql = "INSERT INTO couple(hisname, hername) VALUES (?,?)"
            self.ins_cup = self.cursor.execute(sql, (self.his, self.her,))
            self.conn.commit()

            sql2 = "INSERT INTO relations(hisdadside, herdadside, hismomside, hermomside) VALUES (?,?,?,?)"
            self.ins_fam2 = self.cursor.execute(sql2, (self.his_dad_fam, self.her_dad_fam, self.his_mom_fam, self.her_mom_fam))
            self.conn.commit()

            ### Init budget
            sql = "INSERT INTO budget (budget, totalcost) VALUES (?,?)"
            res = self.cursor.execute(sql, (self.budget, self.total_cost))
            self.conn.commit()

            ### Init Jobs
            sql = "INSERT INTO jobs (job) VALUES (?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?)"
            res = self.cursor.execute(sql, ("None", "Best Man", "Maid of Honor", "Bridesmaid", "Groomsman", "Bridle Table Server", "Server", "Cleanup", "Devotional", "Guest Register", \
                                            "Gift Receiver", "Usher", "Master of Ceremony", "Photographer", "Prayer For Meal", "Welcome And Prayer", "Sermon", "Singer", "Vows",))
            self.conn.commit()

            ### Init Tables
            sql = "INSERT INTO tableinfo (numtables, numpeptable) VALUES (?,?)"
            res = self.cursor.execute(sql, (self.tables, self.table_num_pep))
            self.conn.commit()
            
            ### Add info if first time program opened
            self.update_view_cupfam_window(self.his, self.her, self.his_dad_fam, self.her_dad_fam, self.his_mom_fam, self.her_mom_fam)
            
        except:
            pass
        #==========================Define our Application================================================
        
        self.toolbar = Tk.Frame(master, background="gray25", bd=1, relief=Tk.RAISED)
        self.toolbar.pack(anchor="n", fill=Tk.X)
        
        self.add_person_image = Tk.PhotoImage(file='add_person.gif')
        self.button = Tk.Button(self.toolbar, text="Add Person", font=("Ariel", 8), image=self.add_person_image, compound=Tk.TOP, relief=Tk.FLAT, highlightbackground="gray25", command=self.add_person)
        self.button.pack(side="left")

        self.item_img = Tk.PhotoImage(file='add_item.gif')
        self.add_item_button = Tk.Button(self.toolbar, text="Add Item", font=("Ariel", 8), image=self.item_img, highlightbackground="gray25", compound=Tk.TOP, relief=Tk.FLAT, command=self.add_item)
        self.add_item_button.pack(side="left")
        
        self.separator1 = ttk.Separator(self.toolbar, orient=Tk.VERTICAL)
        self.separator1.pack(side="left", fill=Tk.BOTH, padx=2)

        #self.cupfam_img = Tk.PhotoImage(file='cupfam.gif'), image=self.cupfam_img
        self.cupfam_button = Tk.Button(self.toolbar, text="Couple", font=("Ariel", 8), highlightbackground="gray25", compound=Tk.TOP, relief=Tk.FLAT, command=lambda: self.update_view_cupfam_window(self.his, self.her, self.his_dad_fam, self.her_dad_fam, self.his_mom_fam, self.her_mom_fam))
        self.cupfam_button.pack(side="left")

        #self.bug_img = Tk.PhotoImage(file="budget.gif"), image=self.budget_img
        self.budget_button = Tk.Button(self.toolbar, text="Budget", font=("Ariel", 8), highlightbackground="gray25", compound=Tk.TOP, relief=Tk.FLAT, command=lambda: self.update_view_budget_window(self.budget))
        self.budget_button.pack(side="left")

        #self.job_img = Tk.PhotoImage(file='job_img.gif'), image=self.job_img
        self.jobs_button = Tk.Button(self.toolbar, text="Jobs", font=("Ariel", 8), highlightbackground="gray25", compound=Tk.TOP, relief=Tk.FLAT, command=self.add_job)
        self.jobs_button.pack(side="left")

        #self.tables_img = Tk.PhotoImage(file='tables_img.gif'), image=self.tables_img
        self.tables_button = Tk.Button(self.toolbar, text="Tables", font=("Ariel", 8), highlightbackground="gray25", compound=Tk.TOP, relief=Tk.FLAT, command=lambda: self.update_view_tableinfo_window(self.tables, self.table_num_pep))
        self.tables_button.pack(side="left")
        
        #======================== Main Frame=========================================================================
        
        self.main_frame = Tk.Frame(master, background="black")
        self.main_frame.pack(expand=1, fill=Tk.BOTH)

        self.bottom_frame = Tk.Frame(master, background="gray25") ### Frame for Budget/Cost
        self.bottom_frame.pack(side="bottom", fill=Tk.X)
        
        ### Fill bottom_frame ###
        self.total_cost_price_label = Tk.Label(self.bottom_frame, text="${:.2f}".format(self.total_cost), foreground="white", background="gray25", font=("Arial", 16,"bold"))
        self.total_cost_price_label.pack(side="right")
        self.total_cost_label = Tk.Label(self.bottom_frame, text="Total Cost:", foreground="white", background="gray25", font=("Arial", 14,"bold"))
        self.total_cost_label.pack(side="right")
        
        self.budget_label = Tk.Label(self.bottom_frame, text="Budget: ${:.2f}".format(self.budget), foreground="white", background="gray25", font=("Arial", 16,"bold"))
        self.budget_label.pack(side="left")
        
        
        #=================================================================================================
        
        self.search_frame = Tk.Frame(self.main_frame, background="black")
        self.search_frame.pack(anchor="n", fill=Tk.X, pady=5)
        self.search_label = Tk.Label(self.search_frame, text="Search:", font=("Arial", 11), background="black", foreground="white")
        self.search_label.pack(side="left")
        self.search = Tk.Entry(self.search_frame, highlightbackground="black")
        self.search.pack(anchor="w", fill=Tk.X, pady=2)

        self.search.bind("<Return>", lambda event, arg=self.search: self.search_db(event, arg))
        
        #===========================Creating Tab Control======================================================================
        
        self.tabControl = ttk.Notebook(self.main_frame)          # Create Tab Control
        self.tabControl.pack(expand=1, fill=Tk.BOTH)  # Pack to make visible
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", font=("Ariel", 12), foreground="white", fieldbackground="black", background="black")
        self.style.configure("TNotebook.Tab", font=("Ariel", 10, "bold"))
        self.style.configure("TNotebook", background="black")
        self.style.configure("Treeview.Heading", font=("Arial", 10, "italic"), background="gray25", foreground="white")
        
        #=============================All People Tab====================================================================

        self.people_dataCols = ("First Name", "Last Name", "Phone Number", "Num of People", "Status", "Job", "Relationship")
        self.all_people_tab = ttk.Frame(self.tabControl) 
        self.tabControl.add(self.all_people_tab, text='People')
        self.all_people_columns = ttk.Frame(self.all_people_tab)
        
        self.all_people = ttk.Treeview(columns=self.people_dataCols, show= 'headings')
        self.create_columns(self.people_dataCols, self.all_people_columns, self.all_people)      # Add the tab

        #=============================Bridle Party====================================================================
        self.bp_tab = ttk.Frame(self.tabControl)            # Create a tab 
        self.tabControl.add(self.bp_tab, text='Bridle Party')      # Add the tab
        self.bp_columns = ttk.Frame(self.bp_tab)

        self.bp_people = ttk.Treeview(columns=self.people_dataCols, show= 'headings')
        self.create_columns(self.people_dataCols, self.bp_columns, self.bp_people)
        
        #=============================Family Tab====================================================================
        self.family_tab = ttk.Frame(self.tabControl)            # Create a tab 
        self.tabControl.add(self.family_tab, text='Family')      # Add the tab
        self.family_columns = ttk.Frame(self.family_tab)

        self.family_people = ttk.Treeview(columns=self.people_dataCols, show= 'headings')
        self.create_columns(self.people_dataCols, self.family_columns, self.family_people) 

        #=============================Jobs Tab====================================================================
        self.jobs_tab = ttk.Frame(self.tabControl)            # Create a tab 
        self.tabControl.add(self.jobs_tab, text='Jobs')      # Add the tab
        self.jobs_columns = ttk.Frame(self.jobs_tab)

        self.jobs_people = ttk.Treeview(columns=self.people_dataCols, show= 'headings')
        self.create_columns(self.people_dataCols, self.jobs_columns, self.jobs_people)

        #=============================ALL Items Tab====================================================================
        self.items_dataCols = ("Item", "Desciption", "Cost", "Quantity", "Where Needed", "Buying Status", "Importance")
        self.items_tab = ttk.Frame(self.tabControl)            # Create a tab 
        self.tabControl.add(self.items_tab, text='Items')      # Add the tab
        self.items_columns = ttk.Frame(self.items_tab)

        self.all_items = ttk.Treeview(columns=self.items_dataCols, show= 'headings')
        self.create_columns(self.items_dataCols, self.items_columns, self.all_items)

        #=============================ALL Tables Tab====================================================================
        self.table_dataCols = ("Number", "People", "Remaining", "relationship", "family")
        self.table_tab = ttk.Frame(self.tabControl)            # Create a tab 
        self.tabControl.add(self.table_tab, text='Tables')      # Add the tab
        self.table_columns = ttk.Frame(self.table_tab)

        self.all_tables = ttk.Treeview(columns=self.table_dataCols, show= 'headings')
        self.create_columns(self.table_dataCols, self.table_columns, self.all_tables)

        self.load_budget_data()
        self.load_job_data()
        self.load_table_data()
        self.load_cupfam_data()
        self.load_item_data()
        self.load_people_data()

    #========================Creating Methods=========================================================================

    def create_columns(self, dataCols, columns, tree):
        columns.pack(side=Tk.TOP, fill=Tk.BOTH, expand=Tk.Y)
        ysb = ttk.Scrollbar(orient=Tk.VERTICAL, command= tree.yview)
        xsb = ttk.Scrollbar(orient=Tk.HORIZONTAL, command= tree.xview)
        tree['yscroll'] = ysb.set
        tree['xscroll'] = xsb.set
        
        # add tree and scrollbars to frame
        tree.grid(in_=columns, row=0, column=0, sticky=Tk.NSEW)
        ysb.grid(in_=columns, row=0, column=1, sticky=Tk.NS)
        xsb.grid(in_=columns, row=1, column=0, sticky=Tk.EW)
        
        # set frame resize priorities
        columns.rowconfigure(0, weight=1)
        columns.columnconfigure(0, weight=1)
        
        for n in dataCols:
            tree.heading(n, text=n.title(), command=lambda n=n: self.sort_data(tree, n, self.Sorted))
            tree.column(n, minwidth=0, width=100)         
        
        ### Load all needed application data
        tree.tag_configure("Invited", foreground='purple')
        tree.tag_configure("Coming", foreground='darkgreen')
        tree.tag_configure("Low", foreground='darkgreen')
        tree.tag_configure("Medium", foreground='yellow')
        tree.tag_configure("High", foreground='red')
        
        tree.bind("<Double-1>", lambda event, arg=tree: self.OnDoubleClick(event, arg))
        tree.bind("<Return>", lambda event, arg=tree: self.OnDoubleClick(event, arg))    
        
    def create_search_columns(self, dataCols, columns):
        columns.pack(side=Tk.TOP, fill=Tk.BOTH, expand=Tk.Y)
        ysb = ttk.Scrollbar(columns, orient=Tk.VERTICAL, command= self.search_tree.yview)
        xsb = ttk.Scrollbar(columns, orient=Tk.HORIZONTAL, command= self.search_tree.xview)
        self.search_tree['yscroll'] = ysb.set
        self.search_tree['xscroll'] = xsb.set
        
        ### Configure Tags
        self.search_tree.tag_configure("Invited", foreground='purple')
        self.search_tree.tag_configure("Coming", foreground='darkgreen')
        self.search_tree.tag_configure("Low", foreground='darkgreen')
        self.search_tree.tag_configure("Medium", foreground='yellow')
        self.search_tree.tag_configure("High", foreground='red')
                    
        # add tree and scrollbars to frame
        self.search_tree.grid(in_=columns, row=0, column=0, sticky=Tk.NSEW)
        ysb.grid(in_=columns, row=0, column=1, sticky=Tk.NS)
        xsb.grid(in_=columns, row=1, column=0, sticky=Tk.EW)
        
        # set frame resize priorities
        self.tree_cols.rowconfigure(0, weight=1)
        self.tree_cols.columnconfigure(0, weight=1)
        
        for n in dataCols:
            self.search_tree.heading(n, text=n.title(), command=lambda n=n: self.sort_data(self.search_tree, n, self.Sorted))
            self.search_tree.column(n, minwidth=0, width=100)
        self.search_tree.delete(*self.search_tree.get_children())

        self.search_tree.bind("<Double-1>", lambda event, arg=self.search_tree: self.OnDoubleClick(event, arg))
        self.search_tree.bind("<Return>", lambda event, arg=self.search_tree: self.OnDoubleClick(event, arg))

    def load_people_data(self):
        # Clear the tree
        self.all_people.delete(*self.all_people.get_children())
        try:
            self.family_people.delete(*self.family_people.get_children())
        except:
            pass
        try:
            self.jobs_people.delete(*self.jobs_people.get_children())
        except:
            pass
        try:
            self.bp_people.delete(*self.bp_people.get_children())
        except:
            pass

        sql = "SELECT firstname, lastname, phone, numberofpeople, status, job, relationship, family FROM people"
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
            family = row[7]
            
            self.all_people.insert('', 'end', tags=[status], values=[firstname, lastname, phone, numberofpeople, status, job, relationship])
            
            
            try: 
                if family != "None":
                    self.family_people.insert('', 'end', tags=[family], values=[firstname, lastname, phone, numberofpeople, status, job, relationship])
            except:
                pass
            try: 
                if job != "None":
                    self.jobs_people.insert('', 'end', tags=[job], values=[firstname, lastname, phone, numberofpeople, status, job, relationship])
            except:
                pass
            try: 
                if job == "Best Man" or job == "Maid of Honor" or job == "Bridesmaid" or job == "Groomsman":
                    self.bp_people.insert('', 'end', tags=[job], values=[firstname, lastname, phone, numberofpeople, status, job, relationship])
            except:
                pass

    def load_item_data(self):
        try:
            self.all_items.delete(*self.all_items.get_children())
        except:
            pass

        sql = "SELECT item, description, cost, quantityneeded, whereneeded, buyingstatus, importance FROM items"
        res = self.cursor.execute(sql)
        self.conn.commit()

        for row in res:
            item = row[0]
            desc = row[1]
            cost = row[2]
            quantity = row[3]
            where_need = row[4]
            buying_status = row[5]
            importance = row[6]
            
            try:
                self.all_items.insert('', 'end', tags=[importance], values=[item, desc, cost, quantity, where_need, buying_status, importance])
            except:
                pass
            
    def load_budget_data(self):
        ### Setting Budget information ###
        self.update_total_cost_db()

        sql_budget = "SELECT * FROM budget"
        res_budget = self.cursor.execute(sql_budget)
        for row in res_budget:
            self.budget = row[0]
            self.total_cost = row[1]            
        
        if len(str(self.budget)) >= 6:
            self.str_budget = str(self.budget) 
            self.str_budget = self.str_budget[:-5] + ',' + self.str_budget[-5:] + "0"
        else:
            self.str_budget = str(self.budget) + "0"
            
        if len(str(self.total_cost)) >= 6:
            self.str_total_cost = str(self.total_cost) 
            self.str_total_cost = self.str_total_cost[:-5] + ',' + self.str_total_cost[-5:] + "0"
        else:
            self.str_total_cost = str(self.total_cost) + "0"
            

        self.budget_label.configure(text="Budget: ${}".format(self.str_budget))

        if self.total_cost <= self.budget:
            self.total_cost_price_label.configure(fg="green", text="${}".format(self.str_total_cost))
        else:
            self.total_cost_price_label.configure(fg="red", text="${}".format(self.str_total_cost))

    def load_table_data(self):
        
        sql = "SELECT * FROM tableinfo"
        res = self.cursor.execute(sql)
        self.conn.commit()
        for row in res:
            self.tables = row[0]
            self.table_num_pep = row[1]

        self.load_tables_data()

    def load_tables_data(self):

        try:
            self.all_tables.delete(*self.all_tables.get_children())
        except:
            pass

        sql = "SELECT count(*) FROM tables"
        res = self.cursor.execute(sql)

        for row in res:
            self.number = row[0]
        
        if self.number == self.tables:
            pass
        elif self.number > self.tables:
            for row in range((self.number - self.tables)):
                sql = "DELETE FROM tables WHERE rowid = (SELECT MAX(rowid) FROM tables)"
                res = self.cursor.execute(sql)
                self.conn.commit()
        else:
            for row in range((self.tables - self.number)):
                sql = "INSERT INTO tables(people, remaining, relationship, family, notes) VALUES (?,?,?,?,?)"
                res = self.cursor.execute(sql, ("", 0, "Our Friend", "None", ""))
                self.conn.commit()
        
        sql = "Select rowid, people, remaining, relationship, family, notes from tables"
        res = self.cursor.execute(sql)
        self.conn.commit()
        
        for row in res:
            
            try:
                self.all_tables.insert('', 'end', tags=[], values=[row[0]])
            except:    
                pass
    
    def load_cupfam_data(self):
        ### Setting the family instance variables ###
        sql_coup = "SELECT * FROM couple"
        res_coup = self.cursor.execute(sql_coup)
        for row in res_coup:
            self.his = row[0]
            self.her = row[1]

        sql_fam = "SELECT * FROM relations"
        res_fam = self.cursor.execute(sql_fam)
        self.conn.commit()
        for row in res_fam:
            self.his_dad_fam = row[0]
            self.her_dad_fam = row[1]
            self.his_mom_fam = row[2]
            self.her_mom_fam = row[3]
        try:
            self.family_people.tag_configure(self.his_dad_fam, foreground='green')
            self.family_people.tag_configure(self.her_dad_fam, foreground='orange')
            self.family_people.tag_configure(self.his_mom_fam, foreground='purple')
            self.family_people.tag_configure(self.her_mom_fam, foreground='blue')
        except:
            pass

    def load_job_data(self):
        self.jobs = []
        
        sql = "SELECT * FROM jobs"
        res = self.cursor.execute(sql)
        self.conn.commit()

        for row in res:
            if row[0] not in self.jobs:
                self.jobs.append(row[0])          

    def sort_data(self, tree, col, descending=False):
        # grab values to sort as a list of tuples (column value, column id)
        # e.g. [('Person1', 'I001'), ('Person2', 'I002'), ('Person3', 'I003')]
        data = [[tree.set(child, col), child] for child in tree.get_children('')]
        
        data.sort(reverse=descending)  # reorder data
        for indx, item in enumerate(data): # tkinter looks after moving other items in the same row
            tree.move(item[1], '', indx)   # item[1] = item Identifier
        
        # reverse sort direction for next sort operation
        self.Sorted =  not descending
                
    def add_person_window(self):
        self.person_window = Tk.Toplevel(self, background="gray12")
        self.person_window.wm_title("Add Person")
        self.person_window.geometry("550x500")
                    
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
        self.relationship_listbox = Tk.OptionMenu(self.middle_frame, self.relation, "Our Friend", "His Friend", "Her Friend", "Cousin", "Aunt", "Uncle", "Aunt & Uncle")
        self.relationship_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.relation.set("Our Friend")
        self.relationship_listbox.grid(row=4, column=1, sticky="w")

        self.family = Tk.StringVar(self.middle_frame)
        self.family_label = Tk.Label(self.middle_frame, text="Family:", foreground="white", background="gray12")
        self.family_label.grid(row=5, column=0, sticky="w")
        self.family_listbox = Tk.OptionMenu(self.middle_frame, self.family, "None", self.his_dad_fam, self.her_dad_fam, self.his_mom_fam, self.her_mom_fam)
        self.family_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.family.set("None")
        self.family_listbox.grid(row=5, column=1, sticky="w")
        
        self.is_bibleschool = Tk.IntVar()
        self.is_bibleschool_label = Tk.Label(self.middle_frame, text="Bibleschool:", highlightbackground="black", foreground="white", background="gray12")
        self.is_bibleschool_label.grid(row=6, column=0, sticky="w")
        self.is_bibleschool_check = Tk.Checkbutton(self.middle_frame, background="gray12", variable=self.is_bibleschool)
        self.is_bibleschool_check.grid(row=6, column=1, sticky="w")

        self.n_coming = Tk.StringVar(self.middle_frame)
        self.n_coming_label = Tk.Label(self.middle_frame, text="Num Coming:", foreground="white", background="gray12")
        self.n_coming_label.grid(row=4, column=1, sticky="e")
        self.n_coming_listbox = Tk.OptionMenu(self.middle_frame, self.n_coming, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        self.n_coming_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=5)
        self.n_coming.set(1)
        self.n_coming_listbox.grid(row=4, column=2, sticky="w")

        self.job = Tk.StringVar(self.middle_frame)
        self.jobs_label = Tk.Label(self.middle_frame, text="Job/Role:", foreground="white", background="gray12")
        self.jobs_label.grid(row=0, column=2, sticky="w")
        self.jobs_box = Tk.OptionMenu(self.middle_frame, self.job, *self.jobs)
        self.jobs_box.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.job.set(self.jobs[0])
        self.jobs_box.grid(row=0, column=3, sticky="w")

        self.table = Tk.StringVar(self.middle_frame)
        self.tablenum_label = Tk.Label(self.middle_frame, text="Table:", foreground="white", background="gray12")
        self.tablenum_label.grid(row=5, column=1, sticky="e")
        self.tablenum_box = Tk.OptionMenu(self.middle_frame, self.table, 1, 2)
        self.tablenum_box.configure(highlightbackground="black", background="gray12", foreground="white", width=5)
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

    def add_item_window(self):
        self.item_window = Tk.Toplevel(self, takefocus=True)
        self.item_window.wm_title("Add Item")
        self.item_window.geometry("550x500")

        self.item_toolbar1 = Tk.Frame(self.item_window, bd=1, relief=Tk.RAISED, background="gray25")
        
        self.item_toolbar1.pack(side="top", fill=Tk.X)
        
        self.item_middle_frame = Tk.Frame(self.item_window, background="gray12")
        self.item_middle_frame.pack(expand=1, fill=Tk.BOTH)
        
        self.item_bottom_frame = Tk.Frame(self.item_window, background="gray12")
        self.item_bottom_frame.pack(expand=1, fill=Tk.BOTH)
        
        ### Add Item name label and box
        self.item_label = Tk.Label(self.item_middle_frame, text="Item:", foreground="white", background="gray12")
        self.item_label.grid(row=0, column=0, sticky="w")
        self.item_ent = Tk.Entry(self.item_middle_frame, highlightbackground="gray12", width=20)
        self.item_ent.grid(row=0, column=1, sticky="w")

        ### Add Item description
        self.item_desc_label = Tk.Label(self.item_middle_frame, text="Description:", foreground="white", background="gray12")
        self.item_desc_label.grid(row=1, column=0, sticky="w")
        self.item_desc_ent = Tk.Entry(self.item_middle_frame, highlightbackground="gray12", width=35)
        self.item_desc_ent.grid(row=1, column=1, sticky="w")

        ### Item Cost
        self.item_cost_label = Tk.Label(self.item_middle_frame, text="Cost: $", foreground="white", background="gray12")
        self.item_cost_label.grid(row=2, column=0, sticky="w")
        self.item_cost_ent = Tk.Entry(self.item_middle_frame, highlightbackground="gray12", width=7)
        self.item_cost_ent.grid(row=2, column=1, sticky="w")

        ### Number of Items
        self.item_quantity_label = Tk.Label(self.item_middle_frame, text="Quantity:", foreground="white", background="gray12")
        self.item_quantity_label.grid(row=3, column=0, sticky="w")
        self.item_quantity_ent = Tk.Entry(self.item_middle_frame, highlightbackground="gray12", width=4)
        self.item_quantity_ent.grid(row=3, column=1, sticky="w")

        ### Where Needed
        self.where_needed = Tk.StringVar(self.item_middle_frame)
        self.where_needed_label = Tk.Label(self.item_middle_frame, text="Where Needed:", foreground="white", background="gray12")
        self.where_needed_label.grid(row=4, column=0, sticky="w")
        self.where_needed_listbox = Tk.OptionMenu(self.item_middle_frame, self.where_needed, "None", "Ceremony", "Reception")
        self.where_needed_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.where_needed.set("None")
        self.where_needed_listbox.grid(row=4, column=1, sticky="w")

        ### Buying tatus
        self.buying_status = Tk.StringVar(self.item_middle_frame)
        self.buying_status_label = Tk.Label(self.item_middle_frame, text="Buying Status:", foreground="white", background="gray12")
        self.buying_status_label.grid(row=5, column=0, sticky="w")
        self.buying_status_listbox = Tk.OptionMenu(self.item_middle_frame, self.buying_status, "Might Buy", "Will Buy", "Purchased")
        self.buying_status_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.buying_status.set("None")
        self.buying_status_listbox.grid(row=5, column=1, sticky="w")

        ### Item Importance
        self.item_importance = Tk.StringVar(self.item_middle_frame)
        self.item_importance_label = Tk.Label(self.item_middle_frame, text="Importance:", foreground="white", background="gray12")
        self.item_importance_label.grid(row=6, column=0, sticky="w")
        self.item_importance_listbox = Tk.OptionMenu(self.item_middle_frame, self.item_importance, "Low", "Medium", "High")
        self.item_importance_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.item_importance.set("Low")
        self.item_importance_listbox.grid(row=6, column=1, sticky="w")

        ### Add note box at bottom
        self.item_nlabel = Tk.Label(self.item_bottom_frame, text="Notes:", foreground="white", background="gray12")
        self.item_nlabel.pack(side="top", anchor="w")
        self.item_ntext = Tk.Text(self.item_bottom_frame, height=10)
        self.item_ntext.pack(expand=1, fill=Tk.BOTH)

        
        #self.update_person_image = Tk.PhotoImage(file="update_person.gif")
        self.a_item_but = Tk.Button(self.item_toolbar1, text="Add", font=("Arial", 12, "bold", "italic"), highlightbackground="gray25",  command=self.save_item_db)
        self.a_item_but.pack(side="left")

    def add_delete_job_window(self):
        self.job_window = Tk.Toplevel(self, takefocus=True, background="gray12")
        self.job_window.wm_title("Add/Delete Job")
        self.job_window.geometry("300x75")

        self.job_label = Tk.Label(self.job_window, text="Job/Role:", foreground="white", background="gray12")
        self.job_label.grid(row=0, column=0)
        self.job_ent = Tk.Entry(self.job_window, highlightbackground="gray12", width=20)
        self.job_ent.grid(row=0, column=1, sticky="w")

        self.d_job_but = Tk.Button(self.job_window, text="Delete", font=("Arial", 7, "bold"), highlightbackground="gray12", command=self.delete_job_db)
        self.d_job_but.grid(row=1, column=1)

        self.a_job_but = Tk.Button(self.job_window, text="Submit", font=("Arial", 7, "bold"), highlightbackground="gray12", command=self.save_job_db)
        self.a_job_but.grid(row=1, column=1, sticky="e")
              
    def update_view_person_window(self, firstname, lastname, address, phone, relationship, family, bibleschool, numofpep, status, job, table, notes):
        self.view_person = Tk.Toplevel(self, takefocus=True)
        self.view_person.wm_title(" " + firstname + " " + lastname)
        self.view_person.geometry("550x500")
        self.view_person.attributes('-topmost', 'true')
            
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

        self.is_bibleschool = Tk.IntVar()
        self.is_bibleschool_label = Tk.Label(self.middle_frame, text="Bibleschool:", highlightbackground="black", foreground="white", background="gray12")
        self.is_bibleschool_label.grid(row=6, column=0, sticky="w")
        self.is_bibleschool_check = Tk.Checkbutton(self.middle_frame, background="gray12", variable=self.is_bibleschool)
        self.is_bibleschool_check.grid(row=6, column=1, sticky="w")

        self.n_coming = Tk.StringVar(self.middle_frame)
        self.n_coming_label = Tk.Label(self.middle_frame, text="Num Coming:", foreground="white", background="gray12")
        self.n_coming_label.grid(row=4, column=1, sticky="e")
        self.n_coming_listbox = Tk.OptionMenu(self.middle_frame, self.n_coming, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        self.n_coming_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=5)
        self.n_coming.set(1)
        self.n_coming_listbox.grid(row=4, column=2, sticky="w")
        
        self.job = Tk.StringVar(self.middle_frame)
        self.jobs_label = Tk.Label(self.middle_frame, text="Job/Role:", foreground="white", background="gray12")
        self.jobs_label.grid(row=0, column=2, sticky="w")
        self.jobs_box = Tk.OptionMenu(self.middle_frame, self.job, *self.jobs)
        self.jobs_box.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.job.set(self.jobs[0])
        self.jobs_box.grid(row=0, column=3, sticky="w")

        self.table = Tk.StringVar(self.middle_frame)
        self.tablenum_label = Tk.Label(self.middle_frame, text="Table:", foreground="white", background="gray12")
        self.tablenum_label.grid(row=5, column=1, sticky="e")
        self.tablenum_box = Tk.OptionMenu(self.middle_frame, self.table, 1, 2)
        self.tablenum_box.configure(highlightbackground="black", background="gray12", foreground="white", width=5)
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
        self.is_bibleschool.set(bibleschool)
        self.n_coming.set(numofpep)
        self.status.set(status)
        self.job.set(job)
        self.table.set(table)
        self.people_ntext.insert(Tk.CURRENT, notes)

        #self.update_person_image = Tk.PhotoImage(file="update_person.gif")
        self.u_person_but = Tk.Button(self.toolbar1, text="Update", font=("Arial", 12, "bold", "italic"), highlightbackground="gray25",  command=self.update_person_db)
        self.u_person_but.pack(side="left")

    def update_view_item_window(self, item, desc, cost, quantity, whereneeded, buyingstatus, importance, notes):
        
        self.view_item = Tk.Toplevel(self, takefocus=True)
        self.view_item.wm_title(" " + item + " " + desc)
        self.view_item.geometry("550x500")

        self.item_toolbar1 = Tk.Frame(self.view_item, bd=1, relief=Tk.RAISED, background="gray25")
        
        self.item_toolbar1.pack(side="top", fill=Tk.X)
        
        self.item_middle_frame = Tk.Frame(self.view_item, background="gray12")
        self.item_middle_frame.pack(expand=1, fill=Tk.BOTH)
        
        self.item_bottom_frame = Tk.Frame(self.view_item, background="gray12")
        self.item_bottom_frame.pack(expand=1, fill=Tk.BOTH)
        
        ### Add Item name label and box
        self.item_label = Tk.Label(self.item_middle_frame, text="Item:", foreground="white", background="gray12")
        self.item_label.grid(row=0, column=0, sticky="w")
        self.item_ent = Tk.Entry(self.item_middle_frame, highlightbackground="gray12", width=20)
        self.item_ent.grid(row=0, column=1, sticky="w")

        ### Add Item description
        self.item_desc_label = Tk.Label(self.item_middle_frame, text="Description:", foreground="white", background="gray12")
        self.item_desc_label.grid(row=1, column=0, sticky="w")
        self.item_desc_ent = Tk.Entry(self.item_middle_frame, highlightbackground="gray12", width=35)
        self.item_desc_ent.grid(row=1, column=1, sticky="w")

        ### Item Cost
        self.item_cost_label = Tk.Label(self.item_middle_frame, text="Cost: $", foreground="white", background="gray12")
        self.item_cost_label.grid(row=2, column=0, sticky="w")
        self.item_cost_ent = Tk.Entry(self.item_middle_frame, highlightbackground="gray12", width=7)
        self.item_cost_ent.grid(row=2, column=1, sticky="w")

        ### Number of Items
        self.item_quantity_label = Tk.Label(self.item_middle_frame, text="Quantity:", foreground="white", background="gray12")
        self.item_quantity_label.grid(row=3, column=0, sticky="w")
        self.item_quantity_ent = Tk.Entry(self.item_middle_frame, highlightbackground="gray12", width=4)
        self.item_quantity_ent.grid(row=3, column=1, sticky="w")

        ### Where Needed
        self.where_needed = Tk.StringVar(self.item_middle_frame)
        self.where_needed_label = Tk.Label(self.item_middle_frame, text="Where Needed:", foreground="white", background="gray12")
        self.where_needed_label.grid(row=4, column=0, sticky="w")
        self.where_needed_listbox = Tk.OptionMenu(self.item_middle_frame, self.where_needed, "None", "Ceremony", "Reception")
        self.where_needed_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.where_needed.set("None")
        self.where_needed_listbox.grid(row=4, column=1, sticky="w")

        ### Buying tatus
        self.buying_status = Tk.StringVar(self.item_middle_frame)
        self.buying_status_label = Tk.Label(self.item_middle_frame, text="Buying Status:", foreground="white", background="gray12")
        self.buying_status_label.grid(row=5, column=0, sticky="w")
        self.buying_status_listbox = Tk.OptionMenu(self.item_middle_frame, self.buying_status, "Might Buy", "Will Buy", "Purchased")
        self.buying_status_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.buying_status.set("None")
        self.buying_status_listbox.grid(row=5, column=1, sticky="w")

        ### Item Importance
        self.item_importance = Tk.StringVar(self.item_middle_frame)
        self.item_importance_label = Tk.Label(self.item_middle_frame, text="Importance:", foreground="white", background="gray12")
        self.item_importance_label.grid(row=6, column=0, sticky="w")
        self.item_importance_listbox = Tk.OptionMenu(self.item_middle_frame, self.item_importance, "Low", "Medium", "High")
        self.item_importance_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.item_importance.set("Low")
        self.item_importance_listbox.grid(row=6, column=1, sticky="w")

        ### Add note box at bottom
        self.item_nlabel = Tk.Label(self.item_bottom_frame, text="Notes:", foreground="white", background="gray12")
        self.item_nlabel.pack(side="top", anchor="w")
        self.item_ntext = Tk.Text(self.item_bottom_frame, height=10)
        self.item_ntext.pack(expand=1, fill=Tk.BOTH)

        ### Pulling info from tree
        self.item_ent.insert(0,item)
        self.item_desc_ent.insert(0,desc)
        self.item_cost_ent.insert(0,cost)        
        self.item_quantity_ent.insert(0,quantity)
        self.where_needed.set(whereneeded)
        self.buying_status.set(buyingstatus)
        self.item_importance.set(importance)
        self.item_ntext.insert(Tk.CURRENT, notes)

        self.u_item_but = Tk.Button(self.item_toolbar1, text="Save", font=("Arial", 12, "bold", "italic"), highlightbackground="gray25",  command=self.update_item_db)
        self.u_item_but.pack(side="left")

    def update_view_budget_window(self, budget):
        self.view_budget_window = Tk.Toplevel(self, takefocus=True, background="gray12")
        self.view_budget_window.wm_title("Enter/Update Budget")
        self.view_budget_window.geometry("200x75")

        self.total_budget_Label = Tk.Label(self.view_budget_window, text="Budget:", foreground="white", background="gray12")
        self.total_budget_Label.grid(row=0, column=0)
        self.total_budget_ent = Tk.Entry(self.view_budget_window, highlightbackground="gray12", width=8)
        self.total_budget_ent.grid(row=0, column=1, sticky="w")

        self.total_budget_ent.insert(0, budget)

        self.u_budget_but = Tk.Button(self.view_budget_window, text="Submit", font=("Arial", 7, "bold"), highlightbackground="gray12", command=self.update_budget_db)
        self.u_budget_but.grid(row=1, column=1, sticky="e")
        
    def update_view_tableinfo_window(self, tables, numpeptables):
        self.view_table_window = Tk.Toplevel(self, takefocus=True, background="gray12")
        self.view_table_window.wm_title("Enter/Update Tables")
        self.view_table_window.geometry("250x100")

        self.tables_label = Tk.Label(self.view_table_window, text="Num Tables:", foreground="white", background="gray12")
        self.tables_label.grid(row=0, column=0, sticky="w")
        self.tables_ent = Tk.Entry(self.view_table_window, highlightbackground="gray12", width=10)
        self.tables_ent.grid(row=0, column=1, sticky="w")

        self.numpeptable_label = Tk.Label(self.view_table_window, text="Num Per Table:", foreground="white", background="gray12")
        self.numpeptable_label.grid(row=1, column=0)
        self.numpeptable_ent = Tk.Entry(self.view_table_window, highlightbackground="gray12", width=10)
        self.numpeptable_ent.grid(row=1, column=1, sticky="w")

        self.tables_ent.insert(0, tables)
        self.numpeptable_ent.insert(0, numpeptables)

        self.u_tables_but = Tk.Button(self.view_table_window, text="Submit", font=("Arial", 7, "bold"), highlightbackground="gray12", command=self.update_tableinfo_db)
        self.u_tables_but.grid(row=2, column=1, sticky="e")

    def update_view_tables_window(self, ID, people, relationship, family, notes):
        self.view_tables_window = Tk.Toplevel(self, takefocus=True)
        self.view_tables_window.wm_title(" " + "Table" + " " + str(ID))
        self.view_tables_window.geometry("550x500")
        self.view_tables_window.attributes('-topmost', 'true')
            
        self.tables_toolbar1 = Tk.Frame(self.view_tables_window, bd=1, relief=Tk.RAISED, background="gray25")
        
        self.tables_toolbar1.pack(side="top", fill=Tk.X)
        
        self.tables_middle_frame = Tk.Frame(self.view_tables_window, background="gray12")
        self.tables_middle_frame.pack(expand=1, fill=Tk.BOTH)
        
        self.tables_bottom_frame = Tk.Frame(self.view_tables_window, background="gray12")
        self.tables_bottom_frame.pack(expand=1, fill=Tk.BOTH)

        self.relation = Tk.StringVar(self.tables_middle_frame)
        self.relationship_label = Tk.Label(self.tables_middle_frame, text="Relation:", foreground="white", background="gray12")
        self.relationship_label.grid(row=0, column=0, sticky="w")
        self.relationship_listbox = Tk.OptionMenu(self.tables_middle_frame, self.relation, "Friend", "Cousin", "Aunt", "Uncle", "Aunt & Uncle", "His " + "Friend")
        self.relationship_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.relation.set("Friend")
        self.relationship_listbox.grid(row=0, column=1, sticky="w")

        self.family = Tk.StringVar(self.tables_middle_frame)
        self.family_label = Tk.Label(self.tables_middle_frame, text="Family:", foreground="white", background="gray12")
        self.family_label.grid(row=0, column=3, sticky="w")
        self.family_listbox = Tk.OptionMenu(self.tables_middle_frame, self.family, "None", self.his_dad_fam, self.her_dad_fam, self.his_mom_fam, self.her_mom_fam)
        self.family_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.family.set("None")
        self.family_listbox.grid(row=0, column=4, sticky="w")

        self.tables_people_label = Tk.Label(self.tables_middle_frame, text="People:", foreground="white", background="gray12")
        self.tables_people_label.grid(row=1, column=0, sticky="w")
        self.tables_people_list = Tk.Listbox(self.tables_middle_frame)
        self.tables_people_list.grid(row=1, column=1, sticky="w")
        

        self.tables_nlabel = Tk.Label(self.tables_bottom_frame, text="Notes:", foreground="white", background="gray12")
        self.tables_nlabel.pack(side="top", anchor="w")
        self.tables_ntext = Tk.Text(self.tables_bottom_frame, height=10)
        self.tables_ntext.pack(expand=1, fill=Tk.BOTH)
        
        self.relation.set(relationship)
        self.family.set(family)
        self.tables_ntext.insert(Tk.CURRENT, notes)
        #self.tables_people_list.insert(0, "Bill")
        
        #self.update_person_image = Tk.PhotoImage(file="update_person.gif")
        self.u_tables_but = Tk.Button(self.tables_toolbar1, text="Update", font=("Arial", 12, "bold", "italic"), highlightbackground="gray25",  command=self.update_tables_db)
        self.u_tables_but.pack(side="left")

    def update_view_cupfam_window(self, his, her, hisdad, herdad, hismom, hermom):
        self.view_message_window = Tk.Toplevel(self, takefocus=True, background="gray12")
        self.view_message_window.wm_title("Enter/Update Names & Families")
        self.view_message_window.geometry("465x175")
        
        self.view_message_main = Tk.Frame(self.view_message_window,background="gray12")
        self.view_message_main.pack(expand=1, fill=Tk.BOTH)
        
        ### Separator Frame ###
        self.sep_top = ttk.Separator(self.view_message_main, orient=Tk.HORIZONTAL) ### Top Separators
        self.sep_top.grid(row=0, columnspan=5, padx=3, sticky="we")
        self.sep_left = ttk.Separator(self.view_message_main, orient=Tk.VERTICAL)
        self.sep_left.place(x=3, y=11, height=125)
        
        self.bot_sep_top = ttk.Separator(self.view_message_main, orient=Tk.HORIZONTAL) ### Bottom Separators
        self.bot_sep_top.grid(row=4, columnspan=5, padx=3, sticky="we")
        self.bot_sep_right = ttk.Separator(self.view_message_main, orient=Tk.VERTICAL)
        self.bot_sep_right.place(x=461, y=11, height=125)
        self.bot_sep_bot = ttk.Separator(self.view_message_main, orient=Tk.HORIZONTAL)
        self.bot_sep_bot.grid(row=7, columnspan=5, padx=3, sticky="we")
        
        ### Label for couples Names ###
        self.his_label = Tk.Label(self.view_message_main, text="His Name:", foreground="white", background="gray12")
        self.his_label.grid(row=2, column=0, padx=5, sticky="w")
        self.his_ent = Tk.Entry(self.view_message_main, width=15, highlightbackground="gray12")
        self.his_ent.grid(row=2, column=1, sticky="w")
        
        self.her_label = Tk.Label(self.view_message_main, text="Her Name:", foreground="white", background="gray12")
        self.her_label.grid(row=2, column=2, sticky="w")
        self.her_ent = Tk.Entry(self.view_message_main, width=15, highlightbackground="gray12")
        self.her_ent.grid(row=2, column=3, padx=5, sticky="w")
        
        ### Separator Frame Labels ###
        self.top_label = Tk.Label(self.view_message_main, font=("Helvetica", 16, "bold italic"), text="Couple's Names", foreground="white", background="gray12")
        self.top_label.grid(row=0, column=1, stick="w")
        
        self.bot_label = Tk.Label(self.view_message_main, font=("Helvetica", 16, "bold italic"), text="Family Names", foreground="white", background="gray12")
        self.bot_label.grid(row=4, column=1, sticky="w")

        self.his_dadside = Tk.Label(self.view_message_main, text="His Dad's:", foreground="white", background="gray12")
        self.his_dadside.grid(row=5, column=0, padx=5, sticky="w")
        self.his_dadside_ent = Tk.Entry(self.view_message_main, width=15, highlightbackground="gray12")
        self.his_dadside_ent.grid(row=5, column=1, sticky="w")
        
        self.her_dadside = Tk.Label(self.view_message_main, text="Her Dad's:", foreground="white", background="gray12")
        self.her_dadside.grid(row=5, column=2, sticky="w")
        self.her_dadside_ent = Tk.Entry(self.view_message_main, width=15, highlightbackground="gray12")
        self.her_dadside_ent.grid(row=5, column=3, padx=5, sticky="w")
        
        self.his_momside = Tk.Label(self.view_message_main, text="His Mom's:", foreground="white", background="gray12")
        self.his_momside.grid(row=6, column=0, sticky="e")
        self.his_momside_ent = Tk.Entry(self.view_message_main, width=15, highlightbackground="gray12")
        self.his_momside_ent.grid(row=6, column=1, sticky="w")

        self.her_momside = Tk.Label(self.view_message_main, text="Her Mom's:", foreground="white", background="gray12")
        self.her_momside.grid(row=6, column=2, sticky="w")
        self.her_momside_ent = Tk.Entry(self.view_message_main, width=15, highlightbackground="gray12")
        self.her_momside_ent.grid(row=6, column=3, padx=5, sticky="w")

        ### Update Enteries
        self.his_ent.insert(0, his)
        self.her_ent.insert(0, her)
        self.his_dadside_ent.insert(0, hisdad)
        self.her_dadside_ent.insert(0, herdad)
        self.his_momside_ent.insert(0, hismom)
        self.her_momside_ent.insert(0, hermom)
        
        self.view_cupfamily_b = Tk.Button(self.view_message_main, text="Submit", command=self.update_cupfam_db, highlightbackground="gray12")
        self.view_cupfamily_b.grid(row=8, column=3, sticky="e")
        self.view_message_window.attributes('-topmost', 'true')  # Bring the message window on top

    def OnDoubleClick(self, event, tree):
        # So double clicking heads don't throw error
        try:
            selection = tree.item(tree.selection())['values'][0]
            selection1 = tree.item(tree.selection())['values'][1]

            sql = "SELECT ID FROM people WHERE firstname=(?) AND lastname=(?)"
            self.peoplerowid = self.cursor.execute(sql, (selection, selection1))
            self.conn.commit()
            sql = "SELECT * FROM people WHERE ID=(?)"
            for row in self.peoplerowid:
                self.peoplerowid = row
            view = self.cursor.execute(sql, (self.peoplerowid))
            self.conn.commit()
            
            for info in view:
                view_first = info[1]
                view_last = info[2]
                view_addr = info[3]
                view_phone = info[4]
                view_relation = info[5]
                view_fam = info[6]
                view_bibleschool = info[7]
                view_numofpep = info[8]
                view_stat = info[9]
                view_job = info[10]
                view_table = info[11]
                view_notes = info[12]
                
                self.update_view_person_window(info[1], info[2], info[3], info[4], info[5], \
                                        info[6], info[7], info[8], info[9], info[10], info[11], info[12])
        except:
            try:
                selection = tree.item(tree.selection())['values'][0]
                selection1 = tree.item(tree.selection())['values'][1]

                sql = "SELECT ID FROM items WHERE item=(?) AND description=(?)"
                self.itemrowid = self.cursor.execute(sql, (selection, selection1))
                self.conn.commit()
                sql = "SELECT * FROM items WHERE ID=(?)"
                for row in self.itemrowid:
                    self.itemrowid = row
                view = self.cursor.execute(sql, (self.itemrowid))
                self.conn.commit()
                
                for info in view:
                    view_item = info[1]
                    view_desc = info[2]
                    view_cost = info[3]
                    view_quantity = info[4]
                    view_where_needed = info[5]
                    view_buying_status = info[6]
                    view_importance = info[7]
                    view_notes = info[8]
                    
                    self.update_view_item_window(info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[8])
            except:
                
                selection = tree.item(tree.selection())['values'][0]
                #selection1 = tree.item(tree.selection())['values'][1]
                self.tablerowid = selection
                sql = "SELECT * FROM tables WHERE rowid=(?)"
                view = self.cursor.execute(sql, (selection,))
                self.conn.commit()
                

                for info in view:
                    people = info[0]
                    relationship = info[2]
                    family = info[3]
                    notes = info[4]

                    self.update_view_tables_window(self.tablerowid, people, relationship, family, notes)
                   
        
    def save_person_db(self):
        var_n = self.n_ent.get() # Get firstname
        var_ln = self.ln_ent.get() # Get Lastname
        var_address = self.address_text.get("1.0", Tk.END) # Get address
        var_phone = self.phone_ent.get()
        var_relationship = self.relation.get() # Get relationship
        var_fam = self.family.get() # Get Family
        var_bibleschool = self.is_bibleschool.get() # Get if they went to Bibleschool with them
        var_numofpep = self.n_coming.get() # Get number Coming
        var_status = self.status.get() # Get Status
        var_job = self.job.get() # Get Job
        var_tablenum = self.table.get()
        var_notes = self.people_ntext.get("1.0", Tk.END) # Get Notes
        
        sql = "INSERT INTO people (firstname, lastname, address, phone, relationship, family, bibleschool, numberofpeople, status, job, tablenumber, notes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
        res = self.cursor.execute(sql, (var_n, var_ln, var_address, var_phone, var_relationship, var_fam, var_bibleschool, var_numofpep, var_status, var_job, var_tablenum, var_notes))
        self.conn.commit()
        
        # Update People Tree
        self.load_people_data()        

    def save_item_db(self):
        save_item = self.item_ent.get() # Get Item
        save_desc = self.item_desc_ent.get() # Get Description
        save_cost = self.item_cost_ent.get() # Get Cost
        save_quantity = self.item_quantity_ent.get() # Get Quantity
        save_where_needed = self.where_needed.get() # Get Where Needed
        save_buying_status = self.buying_status.get() # Get Buying Status
        save_importance = self.item_importance.get() # Get Item Importance
        save_notes = self.item_ntext.get("1.0", Tk.END) # Get Item Notes

        sql = "INSERT INTO items (item, description, cost, quantityneeded, whereneeded, buyingstatus, importance, notes) VALUES (?,?,?,?,?,?,?,?)"
        res = self.cursor.execute(sql, (save_item, save_desc, save_cost, save_quantity, save_where_needed, save_buying_status, save_importance, save_notes))
        self.conn.commit()

        # Update Item Tree
        self.load_item_data()
        # Update total_cost
        self.load_budget_data()

    def save_job_db(self):
        save_job = self.job_ent.get() # Get Job

        sql = "INSERT INTO jobs (job) VALUES (?)"
        res = self.cursor.execute(sql, (save_job,))
        self.conn.commit()

        self.load_job_data()

    def update_person_db(self):
        update_n = self.n_ent.get() # Get firstname
        update_ln = self.ln_ent.get() # Get Lastname
        update_address = self.address_text.get("1.0", Tk.END) # Get address
        update_phone = self.phone_ent.get()
        update_relationship = self.relation.get() # Get relationship
        update_fam = self.family.get() # Get Family
        update_bibleschool = self.is_bibleschool.get() # Get if they went to Bibleschool with them
        update_numofpep = self.n_coming.get() # Get number Coming
        update_status = self.status.get() # Get Status
        update_job = self.job.get() # Get Job
        update_tablenum = self.table.get()
        update_notes = self.people_ntext.get("1.0", Tk.END) # Get Notes
        
        sql = "UPDATE people SET firstname=(?), lastname=(?), address=(?), phone=(?), relationship=(?), family=(?), bibleschool=(?), numberofpeople=(?), status=(?), job=(?), tablenumber=(?), notes=(?) WHERE ID=(?)"
        res = self.cursor.execute(sql, (update_n, update_ln, update_address, update_phone, update_relationship, update_fam, update_bibleschool, update_numofpep, update_status, \
                                        update_job, update_tablenum, update_notes, self.peoplerowid[0]))
        self.conn.commit()
        
        self.family_people.delete(*self.family_people.get_children())
        self.all_people.delete(*self.all_people.get_children())
        self.load_people_data()
        self.update_window_title(self.view_person, update_n, update_ln)
        try:
            self.search_tree.delete(*self.search_tree.get_children())
            self.search_tree.insert('', 'end', tags=[update_status], values=[update_n, update_ln, update_phone, update_numofpep, update_status, update_job, update_relationship])
        except:
            pass

    def update_item_db(self):
        update_item = self.item_ent.get() # Get Item
        update_desc = self.item_desc_ent.get() # Get Item Desc
        update_cost = self.item_cost_ent.get() # Get Cost
        update_quantity = self.item_quantity_ent.get() # Get Quantity
        update_where_needed = self.where_needed.get() # Get Where Needed
        update_buying_status = self.buying_status.get() # Get Buying Status
        update_importance = self.item_importance.get() # Get Item Importance
        update_notes = self.item_ntext.get("1.0", Tk.END) # Get Item Notes

        sql = "UPDATE items SET item=(?), description=(?), cost=(?), quantityneeded=(?), whereneeded=(?), buyingstatus=(?), importance=(?), notes=(?) WHERE ID=(?)"
        res = self.cursor.execute(sql, (update_item, update_desc, update_cost, update_quantity, update_where_needed, update_buying_status, update_importance, update_notes, self.itemrowid[0]))

        self.conn.commit()

        self.all_items.delete(*self.all_items.get_children())
        
        self.load_item_data() # Reload the items tree to reflect changes
        
        self.load_budget_data() # Update the Buget/Total

        self.update_window_title(self.view_item, update_item, update_desc)
        try:
            self.search_tree.delete(*self.search_tree.get_children())
            self.search_tree.insert('', 'end', tags=[update_importance], values=[update_item, update_desc, update_cost, update_quantity, update_where_needed, update_buying_status, update_importance, update_notes])
        except:
            pass

    def update_budget_db(self):
        view_bugdet = self.total_budget_ent.get() # Get budget value

        sql = "UPDATE budget SET budget=(?)"
        res= self.cursor.execute(sql, (view_bugdet,))
        self.conn.commit()

        self.load_budget_data()

    def update_tableinfo_db(self):
        view_tables = self.tables_ent.get() # Get number of tables
        view_numpeptable = self.numpeptable_ent.get() # Get number of people at table

        sql = "UPDATE tableinfo SET numtables=(?), numpeptable=(?)"
        res= self.cursor.execute(sql, (view_tables, view_numpeptable))
        self.conn.commit()

        self.load_table_data()

    def update_tables_db(self):
        view_relationship = self.relation.get()
        view_family = self.family.get()
        view_people = self.tables_people_list.get(0, Tk.END)
        view_table_notes = self.tables_ntext.get("1.0", Tk.END)

        sql = "UPDATE tables SET relationship=(?), family=(?), people=(?), notes=(?) WHERE rowid=(?)"
        res = self.cursor.execute(sql, (view_relationship, view_family, view_people, view_table_notes, self.tablerowid))
        self.conn.commit()

        self.load_table_data()

    def update_total_cost_db(self):
        # Reset cost so same items don't get added more than once
        self.total_cost = 0.00
        
        sql = "SELECT cost, quantityneeded, buyingstatus from items"
        res= self.cursor.execute(sql)
        self.conn.commit()

        for row in res:
            cost = row[0]
            quantity = row[1]
            buyingstatus = row[2]

            # Only update cost if will buy or purchased
            if buyingstatus == "Will Buy" or buyingstatus == "Purchased":
                self.total_cost += float(cost) * int(quantity)

        sql = "UPDATE budget SET totalcost=(?)"
        res= self.cursor.execute(sql, (self.total_cost,))
        self.conn.commit()

    def update_cupfam_db(self):
        update_his_name = self.his_ent.get()
        update_her_name = self.her_ent.get()
        update_his_dadside_fam = self.his_dadside_ent.get()
        update_her_dadside_fam = self.her_dadside_ent.get()
        update_his_momside_fam = self.his_momside_ent.get()
        update_her_momside_fam = self.her_momside_ent.get()
        
        sql = "UPDATE couple SET hisname=(?), hername=(?)"
        self.ins_cup = self.cursor.execute(sql, (update_his_name, update_her_name,))
        self.conn.commit()

        sql2 = "UPDATE relations SET hisdadside=(?), herdadside=(?), hismomside=(?), hermomside=(?)"
        self.ins_fam2 = self.cursor.execute(sql2, (update_his_dadside_fam, update_her_dadside_fam, update_his_momside_fam, update_her_momside_fam))
        self.conn.commit()

        self.load_cupfam_data()

    def search_db(self, event, search):
        
        try:
            self.cursor.execute("""CREATE VIRTUAL TABLE peoplesearch USING fts4(ID, firstname, lastname, address, phone, relationship, family, bibleschool, \
                                numberofpeople, status, job, tablenumber, notes)""")
            self.cursor.execute("""CREATE VIRTUAL TABLE itemsearch USING fts4(ID, item, description, cost, quantityneeded, whereneeded, buyingstatus, importance, notes)""")
            
            self.conn.commit()
        except:
            pass
        
        results = self.search.get()
        
        try:
            sear_win_results = self.sear_win_sear.get()
        except:
            pass

        sql = "INSERT INTO peoplesearch SELECT * FROM people"
        res = self.cursor.execute(sql)
        sql = "INSERT INTO itemsearch SELECT * FROM items"
        res = self.cursor.execute(sql)
        self.conn.commit()
        
        sql = "SELECT * FROM peoplesearch WHERE (firstname || ' ' || lastname) LIKE ('%' || ? || '%') OR address LIKE ('%' || ? || '%') OR phone LIKE ('%' || ? || '%') \
                OR relationship LIKE ('%' || ? || '%') OR family LIKE ('%' || ? || '%') OR numberofpeople LIKE ('%' || ? || '%') OR status LIKE ('%' || ? || '%') OR notes LIKE ('%' || ? || '%')"
        
        sql_items = "SELECT * FROM itemsearch WHERE item LIKE ('%' || ? || '%') OR description LIKE ('%' || ? || '%') OR whereneeded LIKE ('%' || ? || '%') OR buyingstatus LIKE ('%' || ? || '%') \
                OR importance LIKE ('%' || ? || '%') OR notes LIKE ('%' || ? || '%')"

        if search == self.search:
            
            res = self.cursor.execute(sql, (results, results, results, results, results, results, results, results))
            self.conn.commit()
            
            ### Making the Search Window Appear ###
            self.search_window = Tk.Toplevel(self, background="black")
            self.search_window.geometry("800x480")
            self.search_window.wm_title(" " + "Search Results For: " + results)
            
            #=============================Search Tree====================================================================
            self.search_win_frame = Tk.Frame(self.search_window, background="black")
            self.search_win_frame.pack(anchor="n", fill=Tk.X, pady=5)
            
            self.sear_win_sear_label = Tk.Label(self.search_win_frame, text="Search:", font=("Arial", 11), foreground="white", background="black", pady=2)
            self.sear_win_sear_label.pack(side="left")
            self.sear_win_sear = Tk.Entry(self.search_win_frame, highlightbackground="black")
            self.sear_win_sear.pack(anchor="w", fill=Tk.X, pady=2)
            self.sear_win_sear.bind("<Return>", lambda event, arg=self.sear_win_sear: self.search_db(event, arg))
            
            self.tree_cols = ttk.Frame(self.search_window)
            self.search_tree = ttk.Treeview(self.tree_cols, columns=self.people_dataCols, show= 'headings')
                
            self.create_search_columns(self.people_dataCols, self.tree_cols)
            
            for row in res:
                self.search_tree.insert('', 'end', tags=[row[9]], values=[row[1], row[2], row[4], row[8], row[9], row[10], row[5]])
            
            ### If it wasn't in people try items
            if len(self.search_tree.get_children()) == 0:
                
                res = self.cursor.execute(sql_items, (results, results, results, results, results, results))
                self.conn.commit()

                self.search_tree = ttk.Treeview(self.tree_cols, columns=self.items_dataCols, show= 'headings')

                self.create_search_columns(self.items_dataCols, self.tree_cols)           

                for row in res:
                    self.search_tree.insert('', 'end', tags=[row[6]], values=[row[1], row[2], row[3], row[4], row[5], row[6], row[7]])
                

                sql = "DROP TABLE peoplesearch"
                self.cursor.execute(sql)
                self.conn.commit()

                sql = "DROP TABLE itemsearch"
                self.cursor.execute(sql)
                self.conn.commit()
            else:
            
                sql = "DROP TABLE peoplesearch"
                self.cursor.execute(sql)
                self.conn.commit()

                sql = "DROP TABLE itemsearch"
                self.cursor.execute(sql)
                self.conn.commit()
            
            
        else:
            self.update_window_title(self.search_window, "Search Results For:", sear_win_results)
            
            res = self.cursor.execute(sql, (sear_win_results, sear_win_results, sear_win_results, sear_win_results, sear_win_results, sear_win_results, sear_win_results, sear_win_results))
            self.conn.commit()
            self.search_tree = ttk.Treeview(self.tree_cols, columns=self.people_dataCols, show= 'headings')
            
            self.create_search_columns(self.people_dataCols, self.tree_cols)
            
            for row in res:
                self.search_tree.insert('', 'end', tags=[row[9]], values=[row[1], row[2], row[4], row[8], row[9], row[10], row[5]])
            
            ### If not in people search items
            if len(self.search_tree.get_children()) == 0:
                res = self.cursor.execute(sql_items, (sear_win_results, sear_win_results, sear_win_results, sear_win_results, sear_win_results, sear_win_results))
                
                self.search_tree = ttk.Treeview(self.tree_cols, columns=self.items_dataCols, show= 'headings')
                self.create_search_columns(self.items_dataCols, self.tree_cols)

                for row in res:
                    self.search_tree.insert('', 'end', tags=[row[6]], values=[row[1], row[2], row[3], row[4], row[5], row[6], row[7]])

                sql = "DROP TABLE peoplesearch"
                self.cursor.execute(sql)
                self.conn.commit()

                sql = "DROP TABLE itemsearch"
                self.cursor.execute(sql)
                self.conn.commit()
            else:
                sql = "DROP TABLE peoplesearch"
                self.cursor.execute(sql)
                self.conn.commit()

                sql = "DROP TABLE itemsearch"
                self.cursor.execute(sql)
                self.conn.commit()

    def delete_job_db(self):
        delete_job = self.job_ent.get() # Get Job
                
        sql = "DELETE FROM jobs WHERE job LIKE (?)"
        res = self.cursor.execute(sql, (delete_job,))
        self.conn.commit()
        
        self.load_job_data()
           
    def add_person(self):
        self.add_person_window()

    def add_item(self):
        self.add_item_window()

    def add_job(self):
        self.add_delete_job_window()

    def update_window_title(self, window, firstname, lastname):
        window.wm_title(" " + firstname + " " + lastname)
        
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
