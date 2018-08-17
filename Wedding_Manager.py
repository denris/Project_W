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
        self.jobs = ["None", "Photographer", "Server", "Sermon", "Gift Receiver"]
        self.total_cost = 0.00
        self.budget = 0.00
        self.her = " "
        self.his_dad_fam = " "
        self.her_dad_fam = " "
        self.his_mom_fam = " "
        self.her_mom_fam = " "
                
        self.Sorted = True   # Setting flag for sorting columns
        #=============================Set up Database====================================================================
        try:
            self.cursor.execute("""CREATE TABLE couple(hisname text, hername text)""")  # Create these tables if they don't already exist
            self.cursor.execute("""CREATE TABLE relations(hisdadside text, herdadside text, hismomside text, hermomside text)""")
            self.cursor.execute("""CREATE TABLE people(ID integer PRIMARY KEY AUTOINCREMENT, firstname text, lastname text, address text, phone text, relationship text, family text,\
                                bibleschool int, numberofpeople int, status text, job text, tablenumber int, notes text, CONSTRAINT name_unique UNIQUE (firstname, lastname, address))""")
            self.cursor.execute("""CREATE TABLE items(ID integer PRIMARY KEY AUTOINCREMENT, item text, cost real, quantityneeded int, whereneeded text, buyingstatus text, \
                                importance text, notes text, CONSTRAINT name_unique UNIQUE (item))""")
            self.cursor.execute("""CREATE TABLE budget(budget text, totalcost text)""")
            self.conn.commit()
            self.his = " "
        
            
            #self.message = tkMessageBox.showinfo("Title", "Congratulations, who is getting married?")
            
            ### Add info if first time program opened
            self.add_cupfam_window()
            
        except:
            pass
        #==========================Define our Application================================================
        
        self.toolbar = Tk.Frame(master, background="gray25", bd=1, relief=Tk.RAISED)
        self.toolbar.pack(anchor="n", fill=Tk.X)
        
        self.add_person_image = Tk.PhotoImage(file='add_person.gif')
        self.button = Tk.Button(self.toolbar, text="Add Person", font=("Ariel", 7), image=self.add_person_image, compound=Tk.TOP, relief=Tk.FLAT, highlightbackground="gray25", command=self.add_person)
        self.button.pack(side="left",)

        self.item_img = Tk.PhotoImage(file='add_item.gif')
        self.add_item_button = Tk.Button(self.toolbar, text="Add Item", font=("Ariel", 7), image=self.item_img, highlightbackground="gray25", compound=Tk.TOP, relief=Tk.FLAT, command=self.add_item)
        self.add_item_button.pack(side="left")
        
        self.separator1 = ttk.Separator(self.toolbar, orient=Tk.VERTICAL)
        self.separator1.pack(side="left", fill=Tk.BOTH)

        #self.item_img = Tk.PhotoImage(file='add_item.gif') , image=self.item_img, compound=Tk.TOP
        self.update_cupfam_button = Tk.Button(self.toolbar, text="Cuple & Family", font=("Ariel", 7), highlightbackground="gray25", relief=Tk.FLAT, command=lambda: self.update_view_cupfam_window(self.his, self.her, self.his_dad_fam, self.her_dad_fam, self.his_mom_fam, self.her_mom_fam))
        self.update_cupfam_button.pack(side="left")
        
        
        
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
        self.search = Tk.Entry(self.search_frame)
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
        self.style.configure("Treeview.Heading", font=("Arial", 8, "italic"), background="gray25", foreground="white")
        
        #=============================All People Tab====================================================================

        self.people_dataCols = ("First Name", "Last Name", "Phone Number", "Num of People", "Status", "Job", "Relationship")
        self.all_people_tab = ttk.Frame(self.tabControl) 
        self.tabControl.add(self.all_people_tab, text='People')
        self.all_people_columns = ttk.Frame(self.all_people_tab)
        
        self.all_people = ttk.Treeview(columns=self.people_dataCols, show= 'headings')
        self.create_columns(self.people_dataCols, self.all_people_columns, self.all_people)      # Add the tab
        
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
        self.items_dataCols = ("Item", "Cost", "Quantity Needed", "Where Needed", "Buying Status", "Importance")
        self.items_tab = ttk.Frame(self.tabControl)            # Create a tab 
        self.tabControl.add(self.items_tab, text='Items')      # Add the tab
        self.items_columns = ttk.Frame(self.items_tab)

        self.all_items = ttk.Treeview(columns=self.items_dataCols, show= 'headings')
        self.create_columns(self.items_dataCols, self.items_columns, self.all_items)

        

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
        self.load_cupfam_data()
        self.load_people_data()
        self.load_item_data()
        self.load_budget_data()

        tree.tag_configure("Invited", foreground='purple')
        tree.tag_configure("Coming", foreground='darkgreen')
        tree.tag_configure("Low", foreground='darkgreen')
        tree.tag_configure("Medium", foreground='yellow')
        tree.tag_configure("High", foreground='red')
        tree.tag_configure(self.his_dad_fam, foreground='green')
        tree.tag_configure(self.her_dad_fam, foreground='orange')
        tree.tag_configure(self.his_mom_fam, foreground='purple')
        tree.tag_configure(self.her_mom_fam, foreground='blue')  
        
        
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

    def load_item_data(self):
        try:
            self.all_items.delete(*self.all_items.get_children())
        except:
            pass

        sql = "SELECT item, cost, quantityneeded, whereneeded, buyingstatus, importance FROM items"
        res = self.cursor.execute(sql)
        self.conn.commit()

        for row in res:
            item = row[0]
            cost = row[1]
            quantity = row[2]
            where_need = row[3]
            buying_status = row[4]
            importance = row[5]

            try:
                self.all_items.insert('', 'end', tags=[importance], values=[item, cost, quantity, where_need, buying_status, importance])
            except:
                pass

    def load_budget_data(self):
        ### Setting Budget information ###
        sql_budget = "SELECT * FROM budget"
        res_budget = self.cursor.execute(sql_budget)
        for row in res_budget:
            self.total_cost = row[0]
            self.budget = row[1]

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

        self.load_cupfam_data()

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

        ### Item Cost
        self.item_cost_label = Tk.Label(self.item_middle_frame, text="Cost: $", foreground="white", background="gray12")
        self.item_cost_label.grid(row=1, column=0, sticky="w")
        self.item_cost_ent = Tk.Entry(self.item_middle_frame, highlightbackground="gray12", width=7)
        self.item_cost_ent.grid(row=1, column=1, sticky="w")

        ### Number of Items
        self.item_quantity_label = Tk.Label(self.item_middle_frame, text="Quantity:", foreground="white", background="gray12")
        self.item_quantity_label.grid(row=2, column=0, sticky="w")
        self.item_quantity_ent = Tk.Entry(self.item_middle_frame, highlightbackground="gray12", width=4)
        self.item_quantity_ent.grid(row=2, column=1, sticky="w")

        ### Where Needed
        self.where_needed = Tk.StringVar(self.item_middle_frame)
        self.where_needed_label = Tk.Label(self.item_middle_frame, text="Where Needed:", foreground="white", background="gray12")
        self.where_needed_label.grid(row=3, column=0, sticky="w")
        self.where_needed_listbox = Tk.OptionMenu(self.item_middle_frame, self.where_needed, "None", "Ceremony", "Reception")
        self.where_needed_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.where_needed.set("None")
        self.where_needed_listbox.grid(row=3, column=1, sticky="w")

        ### Buying tatus
        self.buying_status = Tk.StringVar(self.item_middle_frame)
        self.buying_status_label = Tk.Label(self.item_middle_frame, text="Buying Status:", foreground="white", background="gray12")
        self.buying_status_label.grid(row=4, column=0, sticky="w")
        self.buying_status_listbox = Tk.OptionMenu(self.item_middle_frame, self.buying_status, "Might Buy", "Will Buy", "Purchased")
        self.buying_status_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.buying_status.set("None")
        self.buying_status_listbox.grid(row=4, column=1, sticky="w")

        ### Item Importance
        self.item_importance = Tk.StringVar(self.item_middle_frame)
        self.item_importance_label = Tk.Label(self.item_middle_frame, text="Importance:", foreground="white", background="gray12")
        self.item_importance_label.grid(row=5, column=0, sticky="w")
        self.item_importance_listbox = Tk.OptionMenu(self.item_middle_frame, self.item_importance, "Low", "Medium", "High")
        self.item_importance_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.item_importance.set("Low")
        self.item_importance_listbox.grid(row=5, column=1, sticky="w")

        ### Add note box at bottom
        self.item_nlabel = Tk.Label(self.item_bottom_frame, text="Notes:", foreground="white", background="gray12")
        self.item_nlabel.pack(side="top", anchor="w")
        self.item_ntext = Tk.Text(self.item_bottom_frame, height=10)
        self.item_ntext.pack(expand=1, fill=Tk.BOTH)

        
        #self.update_person_image = Tk.PhotoImage(file="update_person.gif")
        self.a_item_but = Tk.Button(self.item_toolbar1, text="Add", font=("Arial", 12, "bold", "italic"), highlightbackground="gray25",  command=self.save_item_db)
        self.a_item_but.pack(side="left")

    def add_cupfam_window(self):
        self.message_window = Tk.Toplevel(self, takefocus=True)
        self.message_window.wm_title("Enter Names & Families")
        self.message_window.geometry("465x175")
        
        self.message_main = Tk.Frame(self.message_window)
        self.message_main.pack(expand=1, fill=Tk.BOTH)
        
        ### Separator Frame ###
        self.sep_top = ttk.Separator(self.message_main, orient=Tk.HORIZONTAL) ### Top Separators
        self.sep_top.grid(row=0, columnspan=5, padx=3, sticky="we")
        self.sep_left = ttk.Separator(self.message_main, orient=Tk.VERTICAL)
        self.sep_left.place(x=3, y=11, height=125)
        
        self.bot_sep_top = ttk.Separator(self.message_main, orient=Tk.HORIZONTAL) ### Bottom Separators
        self.bot_sep_top.grid(row=4, columnspan=5, padx=3, sticky="we")
        self.bot_sep_right = ttk.Separator(self.message_main, orient=Tk.VERTICAL)
        self.bot_sep_right.place(x=461, y=11, height=125)
        self.bot_sep_bot = ttk.Separator(self.message_main, orient=Tk.HORIZONTAL)
        self.bot_sep_bot.grid(row=7, columnspan=5, padx=3, sticky="we")
        
        ### Label for couples Names ###
        self.his_label = Tk.Label(self.message_main, text="His Name:")
        self.his_label.grid(row=2, column=0, padx=5, sticky="e")
        self.his_ent = Tk.Entry(self.message_main, width=15)
        self.his_ent.grid(row=2, column=1, sticky="w")
        
        self.her_label = Tk.Label(self.message_main, text="Her Name:")
        self.her_label.grid(row=2, column=2, sticky="w")
        self.her_ent = Tk.Entry(self.message_main, width=15)
        self.her_ent.grid(row=2, column=3, padx=5, sticky="w")
        
        ### Separator Frame Labels ###
        self.top_label = Tk.Label(self.message_main, font=("Helvetica", 16, "bold italic"), text="Couple's Names")
        self.top_label.grid(row=0, column=1, stick="w")
        
        self.bot_label = Tk.Label(self.message_main, font=("Helvetica", 16, "bold italic"), text="Family Names")
        self.bot_label.grid(row=4, column=1, sticky="w")

        self.his_dadside = Tk.Label(self.message_main, text="His Dad's:")
        self.his_dadside.grid(row=5, column=0, padx=5, sticky="e")
        self.his_dadside_ent = Tk.Entry(self.message_main, width=15)
        self.his_dadside_ent.grid(row=5, column=1, sticky="w")
        
        self.her_dadside = Tk.Label(self.message_main, text="Her Dad's:")
        self.her_dadside.grid(row=5, column=2, sticky="w")
        self.her_dadside_ent = Tk.Entry(self.message_main, width=15)
        self.her_dadside_ent.grid(row=5, column=3, padx=5, sticky="w")
        
        self.his_momside = Tk.Label(self.message_main, text="His Mom's:")
        self.his_momside.grid(row=6, column=0, sticky="e")
        self.his_momside_ent = Tk.Entry(self.message_main, width=15)
        self.his_momside_ent.grid(row=6, column=1, sticky="w")

        self.her_momside = Tk.Label(self.message_main, text="Her Mom's:")
        self.her_momside.grid(row=6, column=2, sticky="w")
        self.her_momside_ent = Tk.Entry(self.message_main, width=15)
        self.her_momside_ent.grid(row=6, column=3, padx=5, sticky="w")
        
        self.cupfamily_b = Tk.Button(self.message_main, text="Submit", command=self.save_cupfam_db)
        self.cupfamily_b.grid(row=8, column=3, sticky="e")
        self.message_window.attributes('-topmost', 'true')  # Bring the message window on top

    def update_view_person_window(self, firstname, lastname, address, phone, relationship, family, bibleschool, numofpep, status, job, table, notes):
        self.view_person = Tk.Toplevel(self, takefocus=True)
        self.view_person.wm_title(" " + firstname + " " + lastname)
        self.view_person.geometry("550x500")
        self.view_person.attributes('-topmost', 'true')
        
        self.sql_fam = "SELECT * FROM relations"
        self.res_fam = self.cursor.execute(self.sql_fam)
        self.conn.commit()
            
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

        self.load_cupfam_data()
        
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

    def update_view_item_window(self, item, cost, quantity, whereneeded, buyingstatus, importance, notes):
        
        self.view_item = Tk.Toplevel(self, takefocus=True)
        self.view_item.wm_title(" " + item + " " + whereneeded)
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

        ### Item Cost
        self.item_cost_label = Tk.Label(self.item_middle_frame, text="Cost: $", foreground="white", background="gray12")
        self.item_cost_label.grid(row=1, column=0, sticky="w")
        self.item_cost_ent = Tk.Entry(self.item_middle_frame, highlightbackground="gray12", width=7)
        self.item_cost_ent.grid(row=1, column=1, sticky="w")

        ### Number of Items
        self.item_quantity_label = Tk.Label(self.item_middle_frame, text="Quantity:", foreground="white", background="gray12")
        self.item_quantity_label.grid(row=2, column=0, sticky="w")
        self.item_quantity_ent = Tk.Entry(self.item_middle_frame, highlightbackground="gray12", width=4)
        self.item_quantity_ent.grid(row=2, column=1, sticky="w")

        ### Where Needed
        self.where_needed = Tk.StringVar(self.item_middle_frame)
        self.where_needed_label = Tk.Label(self.item_middle_frame, text="Where Needed:", foreground="white", background="gray12")
        self.where_needed_label.grid(row=3, column=0, sticky="w")
        self.where_needed_listbox = Tk.OptionMenu(self.item_middle_frame, self.where_needed, "None", "Ceremony", "Reception")
        self.where_needed_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.where_needed.set("None")
        self.where_needed_listbox.grid(row=3, column=1, sticky="w")

        ### Buying tatus
        self.buying_status = Tk.StringVar(self.item_middle_frame)
        self.buying_status_label = Tk.Label(self.item_middle_frame, text="Buying Status:", foreground="white", background="gray12")
        self.buying_status_label.grid(row=4, column=0, sticky="w")
        self.buying_status_listbox = Tk.OptionMenu(self.item_middle_frame, self.buying_status, "Might Buy", "Will Buy", "Purchased")
        self.buying_status_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.buying_status.set("None")
        self.buying_status_listbox.grid(row=4, column=1, sticky="w")

        ### Item Importance
        self.item_importance = Tk.StringVar(self.item_middle_frame)
        self.item_importance_label = Tk.Label(self.item_middle_frame, text="Importance:", foreground="white", background="gray12")
        self.item_importance_label.grid(row=5, column=0, sticky="w")
        self.item_importance_listbox = Tk.OptionMenu(self.item_middle_frame, self.item_importance, "Low", "Medium", "High")
        self.item_importance_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.item_importance.set("Low")
        self.item_importance_listbox.grid(row=5, column=1, sticky="w")

        ### Add note box at bottom
        self.item_nlabel = Tk.Label(self.item_bottom_frame, text="Notes:", foreground="white", background="gray12")
        self.item_nlabel.pack(side="top", anchor="w")
        self.item_ntext = Tk.Text(self.item_bottom_frame, height=10)
        self.item_ntext.pack(expand=1, fill=Tk.BOTH)

        ### Pulling info from tree
        self.item_ent.insert(0,item)
        self.item_cost_ent.insert(0,cost)
        self.item_quantity_ent.insert(0,quantity)
        self.where_needed.set(whereneeded)
        self.buying_status.set(buyingstatus)
        self.item_importance.set(importance)
        self.item_ntext.insert(Tk.CURRENT, notes)

        self.u_item_but = Tk.Button(self.item_toolbar1, text="Save", font=("Arial", 12, "bold", "italic"), highlightbackground="gray25",  command=self.update_item_db)
        self.u_item_but.pack(side="left")

    def update_view_cupfam_window(self, his, her, hisdad, herdad, hismom, hermom):
        self.view_message_window = Tk.Toplevel(self, takefocus=True)
        self.view_message_window.wm_title("Update Names & Families")
        self.view_message_window.geometry("465x175")
        
        self.view_message_main = Tk.Frame(self.view_message_window)
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
        self.his_label = Tk.Label(self.view_message_main, text="His Name:")
        self.his_label.grid(row=2, column=0, padx=5, sticky="e")
        self.his_ent = Tk.Entry(self.view_message_main, width=15)
        self.his_ent.grid(row=2, column=1, sticky="w")
        
        self.her_label = Tk.Label(self.view_message_main, text="Her Name:")
        self.her_label.grid(row=2, column=2, sticky="w")
        self.her_ent = Tk.Entry(self.view_message_main, width=15)
        self.her_ent.grid(row=2, column=3, padx=5, sticky="w")
        
        ### Separator Frame Labels ###
        self.top_label = Tk.Label(self.view_message_main, font=("Helvetica", 16, "bold italic"), text="Couple's Names")
        self.top_label.grid(row=0, column=1, stick="w")
        
        self.bot_label = Tk.Label(self.view_message_main, font=("Helvetica", 16, "bold italic"), text="Family Names")
        self.bot_label.grid(row=4, column=1, sticky="w")

        self.his_dadside = Tk.Label(self.view_message_main, text="His Dad's:")
        self.his_dadside.grid(row=5, column=0, padx=5, sticky="e")
        self.his_dadside_ent = Tk.Entry(self.view_message_main, width=15)
        self.his_dadside_ent.grid(row=5, column=1, sticky="w")
        
        self.her_dadside = Tk.Label(self.view_message_main, text="Her Dad's:")
        self.her_dadside.grid(row=5, column=2, sticky="w")
        self.her_dadside_ent = Tk.Entry(self.view_message_main, width=15)
        self.her_dadside_ent.grid(row=5, column=3, padx=5, sticky="w")
        
        self.his_momside = Tk.Label(self.view_message_main, text="His Mom's:")
        self.his_momside.grid(row=6, column=0, sticky="e")
        self.his_momside_ent = Tk.Entry(self.view_message_main, width=15)
        self.his_momside_ent.grid(row=6, column=1, sticky="w")

        self.her_momside = Tk.Label(self.view_message_main, text="Her Mom's:")
        self.her_momside.grid(row=6, column=2, sticky="w")
        self.her_momside_ent = Tk.Entry(self.view_message_main, width=15)
        self.her_momside_ent.grid(row=6, column=3, padx=5, sticky="w")

        ### Update Enteries
        self.his_ent.insert(0, his)
        self.her_ent.insert(0, her)
        self.his_dadside_ent.insert(0, hisdad)
        self.her_dadside_ent.insert(0, herdad)
        self.his_momside_ent.insert(0, hismom)
        self.her_momside_ent.insert(0, hermom)
        
        self.view_cupfamily_b = Tk.Button(self.view_message_main, text="Submit", command=self.update_cupfam_db)
        self.view_cupfamily_b.grid(row=8, column=3, sticky="e")

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

                sql = "SELECT ID FROM items WHERE item=(?) AND cost=(?)"
                self.itemrowid = self.cursor.execute(sql, (selection, selection1))
                self.conn.commit()
                sql = "SELECT * FROM items WHERE ID=(?)"
                for row in self.itemrowid:
                    self.itemrowid = row
                view = self.cursor.execute(sql, (self.itemrowid))
                self.conn.commit()
                
                for info in view:
                    view_item = info[1]
                    view_cost = info[2]
                    view_quantity = info[3]
                    view_where_needed = info[4]
                    view_buying_status = info[5]
                    view_importance = info[6]
                    view_notes = info[7]
                    
                    self.update_view_item_window(info[1], info[2], info[3], info[4], info[5], info[6], info[7])
            except:
                pass     
        
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
        save_cost = self.item_cost_ent.get() # Get Cost
        save_quantity = self.item_quantity_ent.get() # Get Quantity
        save_where_needed = self.where_needed.get() # Get Where Needed
        save_buying_status = self.buying_status.get() # Get Buying Status
        save_importance = self.item_importance.get() # Get Item Importance
        save_notes = self.item_ntext.get("1.0", Tk.END) # Get Item Notes

        sql = "INSERT INTO items (item, cost, quantityneeded, whereneeded, buyingstatus, importance, notes) VALUES (?,?,?,?,?,?,?)"
        res = self.cursor.execute(sql, (save_item, save_cost, save_quantity, save_where_needed, save_buying_status, save_importance, save_notes))
        self.conn.commit()

        # Update Item Tree
        self.load_item_data()

    def save_budget_db(self):

        sql = "INSERT INTO budget (budget, totalcost) VALUES (?,?)"
        res = self.cursor.execute(sql, ())

        ### Update budget
        self.load_budget_data()

    def save_cupfam_db(self):
        his_name = self.his_ent.get()
        her_name = self.her_ent.get()
        his_dadside_fam = self.his_dadside_ent.get()
        her_dadside_fam = self.her_dadside_ent.get()
        his_momside_fam = self.his_momside_ent.get()
        her_momside_fam = self.her_momside_ent.get()
        
        sql = "INSERT INTO couple(hisname, hername) VALUES (?,?)"
        self.ins_cup = self.cursor.execute(sql, (his_name, her_name,))
        self.conn.commit()

        sql2 = "INSERT INTO relations(hisdadside, herdadside, hismomside, hermomside) VALUES (?,?,?,?)"
        self.ins_fam2 = self.cursor.execute(sql2, (his_dadside_fam, her_dadside_fam, his_momside_fam, her_momside_fam))
        self.conn.commit()
        self.destroy_window(self.message_window)

        self.load_cupfam_data()

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
        update_cost = self.item_cost_ent.get() # Get Cost
        update_quantity = self.item_quantity_ent.get() # Get Quantity
        update_where_needed = self.where_needed.get() # Get Where Needed
        update_buying_status = self.buying_status.get() # Get Buying Status
        update_importance = self.item_importance.get() # Get Item Importance
        update_notes = self.item_ntext.get("1.0", Tk.END) # Get Item Notes

        sql = "UPDATE items SET item=(?), cost=(?), quantityneeded=(?), whereneeded=(?), buyingstatus=(?), importance=(?), notes=(?) WHERE ID=(?)"
        res = self.cursor.execute(sql, (update_item, update_cost, update_quantity, update_where_needed, update_buying_status, update_importance, update_notes, self.itemrowid[0]))

        self.conn.commit()

        self.all_items.delete(*self.all_items.get_children())
        self.load_item_data()
        self.update_window_title(self.view_item, update_item, update_where_needed)
        try:
            self.search_tree.delete(*self.search_tree.get_children())
            self.search_tree.insert('', 'end', tags=[update_importance], values=[update_item, update_cost, update_quantity, update_where_needed, update_buying_status, update_importance, update_notes])
        except:
            pass

    def update_budget_db(self):

        sql = "UPDATE budget SET budget=(?), totalcost=(?)"
        res= self.cursor.execute(sql, ())

        self.load_budget_data()

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
            self.cursor.execute("""CREATE VIRTUAL TABLE itemsearch USING fts4(ID, item, cost, quantityneeded, whereneeded, buyingstatus, importance, notes)""")
            
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
        
        sql_items = "SELECT * FROM itemsearch WHERE item LIKE ('%' || ? || '%') OR whereneeded LIKE ('%' || ? || '%') OR buyingstatus LIKE ('%' || ? || '%') \
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
            self.sear_win_sear = Tk.Entry(self.search_win_frame)
            self.sear_win_sear.pack(anchor="w", fill=Tk.X, pady=2)
            self.sear_win_sear.bind("<Return>", lambda event, arg=self.sear_win_sear: self.search_db(event, arg))
            
            self.tree_cols = ttk.Frame(self.search_window)
            self.search_tree = ttk.Treeview(self.tree_cols, columns=self.people_dataCols, show= 'headings')
                
            self.create_search_columns(self.people_dataCols, self.tree_cols)
            
            for row in res:
                self.search_tree.insert('', 'end', tags=[row[9]], values=[row[1], row[2], row[4], row[8], row[9], row[10], row[5]])
            
            ### If it wasn't in people try items
            if len(self.search_tree.get_children()) == 0:
                
                res = self.cursor.execute(sql_items, (results, results, results, results, results))
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
                res = self.cursor.execute(sql_items, (sear_win_results, sear_win_results, sear_win_results, sear_win_results, sear_win_results))
                
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
        
    def add_person(self):
        self.add_person_window()

    def add_item(self):
        self.add_item_window()

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
    
    if app.total_cost <= app.budget:
        app.total_cost_price_label.configure(fg="green")
    else:
        app.total_cost_price_label.configure(fg="red")
    
    win.protocol("WM_DELETE_WINDOW", app.quit_main)
    win.mainloop()                     
    
main()
