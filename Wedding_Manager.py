
import Tkinter as Tk                 # imports
import tkMessageBox
import ttk
import sqlite3
import subprocess
from sys import platform

class Application(ttk.Frame, Tk.Frame, Tk.PhotoImage):

    double_click_flag = False
    

    def __init__(self, master):
        ttk.Frame.__init__(self)
        Tk.Frame.__init__(self)
        Tk.PhotoImage.__init__(self)
        self.master = master
        
        master.geometry("1450x850")    
        master.title("Wedding Central") # Add a title
        master.configure(background="gray")
        #master.attributes('-topmost', 'true')
        # Find what Type of computer it is running on
        if platform == "linux" or platform == "linux2":
            self.platform = "lin"
        elif platform == "darwin":
            self.platform = "mac"
        elif platform == "win32":
            self.platform = "win"

        #print self.platform
    
        #=================================================================================================
        
        

        self.conn = sqlite3.connect("W_management.db") # Establish Database Connection
        self.cursor = self.conn.cursor()

        
        sql = "SELECT Count(*) FROM people"
        names = self.cursor.execute(sql).fetchone()        
        
        ### Things that will be dynamically populated ###
        self.jobs = []
        self.stores = []
        self.tablenum = 0
        self.tables = 0
        self.mul_number = Tk.IntVar()
        self.table_num_pep = 0
        self.is_sections = Tk.IntVar()
        self.old_table_num_pep = self.table_num_pep
        self.stores = []
        self.total_cost = 0.00
        self.str_total_cost = "0.00"
        self.budget = 0.00
        self.str_budget= "0.00"
        self.people_invited = 0
        self.people_coming = 0
        self.people_not_coming = 0
        self.number_tasks = 0
        self.completed_tasks = 0
        self.percent_task = 0.0
        self.his = ""
        self.her = ""
        self.old_firstname = ""
        self.old_lastname = ""
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
                                importance text, store text, notes text, CONSTRAINT name_unique UNIQUE (description))""")
            self.cursor.execute("""CREATE TABLE tasks(ID integer PRIMARY KEY AUTOINCREMENT, task text, whereneeded text, importance text, category text, person text, status text, notes text, CONSTRAINT name_unique UNIQUE (task, category, person, notes))""")
            self.cursor.execute("""CREATE TABLE tables(people text, remaining int, relationship text, family text, notes text)""")
            self.cursor.execute("""CREATE TABLE budget(budget real, totalcost real)""")
            self.cursor.execute("""CREATE TABLE jobs(job text, CONSTRAINT name_unique UNIQUE (job))""")
            self.cursor.execute("""CREATE TABLE tableinfo(numtables int, numpeptable int, sections int, multables int)""")
            
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
            sql = "INSERT INTO jobs (job) VALUES (?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?)"
            res = self.cursor.execute(sql, ("None", "Best Man", "Maid of Honor", "Bridesmaid", "Groomsman", "Bridal Table Servers", "Family Table Servers", "Guest Servers", "Appetizer Servers", "Cleanup", "Dishwashers", "Devotional", "Guest Registrars", \
                                           "Gift Receivers", "Congregational Songs", "Ceremony Ushers", "Master of Ceremonies", "Photography", "Florists", "Cooks", "Prayer For Meal", "Welcome And Prayer", "Meditation", "Vocalists", "Exchange of Vows", \
                                           "Program Attendants", "Ceremony Coordinators", "Reception Coordinators", "Host & Hostess"))
            self.conn.commit()

            ### Init Stores
            sql = "INSERT INTO items (store) VALUES (?),(?),(?),(?)"
            self.cursor.execute(sql, ("None", "Amazon", "Sam's Club", "Walmart"))
            self.conn.commit()

            ### Init Tables
            sql = "INSERT INTO tableinfo (numtables, numpeptable, sections, multables) VALUES (?,?,?,?)"
            res = self.cursor.execute(sql, (self.tables, self.table_num_pep, self.is_sections, self.mul_tables))
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

        self.todo_img = Tk.PhotoImage(file='add_task.gif')
        self.add_todo_button = Tk.Button(self.toolbar, text="Add ToDo", font=("Ariel", 8), image=self.todo_img, highlightbackground="gray25", compound=Tk.TOP, relief=Tk.FLAT, command=self.add_todo)
        self.add_todo_button.pack(side="left")
        
        self.separator1 = ttk.Separator(self.toolbar, orient=Tk.VERTICAL)
        self.separator1.pack(side="left", fill=Tk.BOTH, padx=2)

        self.cupfam_img = Tk.PhotoImage(file='cupfam.gif')
        self.cupfam_button = Tk.Button(self.toolbar, text="Couple", font=("Ariel", 8), image=self.cupfam_img, highlightbackground="gray25", compound=Tk.TOP, relief=Tk.FLAT, command=lambda: self.update_view_cupfam_window(self.his, self.her, self.his_dad_fam, self.her_dad_fam, self.his_mom_fam, self.her_mom_fam))
        self.cupfam_button.pack(side="left")

        self.budget_img = Tk.PhotoImage(file="budget.gif")
        self.budget_button = Tk.Button(self.toolbar, text="Budget", font=("Ariel", 8), image=self.budget_img, highlightbackground="gray25", compound=Tk.TOP, relief=Tk.FLAT, command=lambda: self.update_view_budget_window(self.budget))
        self.budget_button.pack(side="left")

        self.job_img = Tk.PhotoImage(file='jobs.gif')
        self.jobs_button = Tk.Button(self.toolbar, text="Jobs", font=("Ariel", 8), image=self.job_img, highlightbackground="gray25", compound=Tk.TOP, relief=Tk.FLAT, command=self.add_job)
        self.jobs_button.pack(side="left")

        self.tables_img = Tk.PhotoImage(file='tables.gif')
        self.tables_button = Tk.Button(self.toolbar, text="Tables", font=("Ariel", 8), image=self.tables_img, highlightbackground="gray25", compound=Tk.TOP, relief=Tk.FLAT, command=lambda: self.update_view_tableinfo_window(self.tables, self.table_num_pep, self.is_sections.get(), self.mul_number.get()))
        self.tables_button.pack(side="left")

        self.store_img = Tk.PhotoImage(file='stores.gif')
        self.store_button = Tk.Button(self.toolbar, text="Stores", font=("Ariel", 8), image=self.store_img, highlightbackground="gray25", compound=Tk.TOP, relief=Tk.FLAT, command=self.add_store)
        self.store_button.pack(side="left")

        self.separator2 = ttk.Separator(self.toolbar, orient=Tk.VERTICAL)
        self.separator2.pack(side="left", fill=Tk.BOTH, padx=2)

        self.del_person_img = Tk.PhotoImage(file='del_person.gif')
        self.del_people_button = Tk.Button(self.toolbar, text="Del Person", font=("Ariel", 8), image=self.del_person_img, highlightbackground="gray25", compound=Tk.TOP, relief=Tk.FLAT, command=self.del_people)
        self.del_people_button.pack(side="left")

        self.del_item_img = Tk.PhotoImage(file='del_item.gif')
        self.del_item_button = Tk.Button(self.toolbar, text="Del Item", font=("Ariel", 8), image=self.del_item_img, highlightbackground="gray25", compound=Tk.TOP, relief=Tk.FLAT, command=self.del_item)
        self.del_item_button.pack(side="left")

        self.del_todo_img = Tk.PhotoImage(file='del_todo.gif')
        self.del_todo_button = Tk.Button(self.toolbar, text="Del To Do", font=("Ariel", 8), image=self.del_todo_img, highlightbackground="gray25", compound=Tk.TOP, relief=Tk.FLAT, command=self.del_todo)
        self.del_todo_button.pack(side="left")
        
        #======================== Main Frame=========================================================================
        
        self.main_frame = Tk.Frame(master, background="black")
        self.main_frame.pack(expand=1, fill=Tk.BOTH)

        self.bottom_frame = Tk.Frame(master, background="gray25") ### Frame for Budget/Cost
        self.bottom_frame.pack(side="bottom", fill=Tk.X)
        
        self.bottom_frame.grid_columnconfigure(3, weight=1)
        self.bottom_frame.grid_columnconfigure(4, weight=1)
        self.bottom_frame.grid_columnconfigure(6, weight=1)
        self.bottom_frame.grid_columnconfigure(7, weight=2)
        
        #### Fill bottom_frame ###
        # self.budget_label = Tk.Label(self.bottom_frame, text="Budget: ${:.2f}".format(self.budget), foreground="white", background="gray25", font=("Arial", 16,"bold"))
        # self.budget_label.grid(row=0, column=0, sticky="w")
        
        self.total_cost_label = Tk.Label(self.bottom_frame, text="Total Cost:", foreground="white", background="gray25", font=("Arial", 14,"bold"))
        self.total_cost_label.grid(row=0, column=0, sticky="e")
        self.total_cost_price_label = Tk.Label(self.bottom_frame, text="${:.2f}".format(self.total_cost), foreground="white", background="gray25", font=("Arial", 16,"bold"))
        self.total_cost_price_label.grid(row=0, column=1, sticky="w")

        self.invited_label = Tk.Label(self.bottom_frame, text="Invited: {}".format(self.people_invited), foreground="purple", background="gray25", font=("Arial", 16,"bold"))
        self.invited_label.grid(row=0, column=4, sticky="e")
        
        # self.divider = Tk.Label(self.bottom_frame, text=" : ", foreground="white", background="gray25", font=("Arial", 16,"bold"))
        # self.divider.grid(row=0, column=5, sticky="we")
        
        self.coming_label = Tk.Label(self.bottom_frame, text="Coming: {}".format(self.people_coming), foreground="green", background="gray25", font=("Arial", 16,"bold"))
        self.coming_label.grid(row=0, column=6)

        # self.divider2 = Tk.Label(self.bottom_frame, text=" : ", foreground="white", background="gray25", font=("Arial", 16,"bold"))
        # self.divider2.grid(row=0, column=6, sticky='e')

        self.not_coming_label = Tk.Label(self.bottom_frame, text="Not Coming: {}".format(self.people_not_coming), foreground="red", background="gray25", font=("Arial", 16,"bold"))
        self.not_coming_label.grid(row=0, column=7, sticky='w')
        
        self.completed_label = Tk.Label(self.bottom_frame, text="Planning Completed:", foreground="white", background="gray25", font=("Arial", 16,"bold"))
        self.completed_label.grid(row=0, column=9, sticky="e")
        self.planning_completed_label = Tk.Label(self.bottom_frame, text="{:.1f}%".format(self.percent_task), foreground="white", background="gray25", font=("Arial", 16,"bold"))
        self.planning_completed_label.grid(row=0, column=10, sticky="w")

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

        self.people_dataCols = ("First Name", "Last Name", "Address", "Num of People", "Status", "Job", "Relationship")
        self.family_dataCols = ("First Name", "Last Name", "Address", "Num of People", "Status", "Job", "Family")        
        self.items_dataCols = ("Item", "Desciption", "Cost", "Quantity", "Where Needed", "Buying Status", "Store")
        self.table_dataCols = ("Number", "People", "Remaining", "relationship", "family")
        self.todo_dataCols = ("Task", "Where Needed", "Importance", "Category", "Person", "Task Status")
        
        #=============================All People Tab====================================================================

        self.all_people_tab = ttk.Frame(self.tabControl) 
        self.tabControl.add(self.all_people_tab, text='People')
        self.all_people_columns = ttk.Frame(self.all_people_tab)
        
        self.all_people = ttk.Treeview(columns=self.people_dataCols, show= 'headings')
        self.create_columns(self.people_dataCols, self.all_people_columns, self.all_people)      # Add the tab

        #=============================Bridle Party====================================================================
        self.bp_tab = ttk.Frame(self.tabControl)            # Create a tab 
        self.tabControl.add(self.bp_tab, text='Bridal Party')      # Add the tab
        self.bp_columns = ttk.Frame(self.bp_tab)

        self.bp_people = ttk.Treeview(columns=self.people_dataCols, show= 'headings')
        self.create_columns(self.people_dataCols, self.bp_columns, self.bp_people)
        
        #=============================Family Tab====================================================================
        self.family_tab = ttk.Frame(self.tabControl)            # Create a tab 
        self.tabControl.add(self.family_tab, text='Family')      # Add the tab
        self.family_columns = ttk.Frame(self.family_tab)

        self.family_people = ttk.Treeview(columns=self.family_dataCols, show= 'headings')
        self.create_columns(self.family_dataCols, self.family_columns, self.family_people)

        #=============================Bible School Tab====================================================================
        self.bibleschool_tab = ttk.Frame(self.tabControl)            # Create a tab 
        self.tabControl.add(self.bibleschool_tab, text='Bible School')      # Add the tab
        self.bibleschool_columns = ttk.Frame(self.bibleschool_tab)

        self.bibleschool_people = ttk.Treeview(columns=self.people_dataCols, show= 'headings')
        self.create_columns(self.people_dataCols, self.bibleschool_columns, self.bibleschool_people) 

        #=============================Jobs Tab====================================================================
        self.jobs_tab = ttk.Frame(self.tabControl)            # Create a tab 
        self.tabControl.add(self.jobs_tab, text='Jobs')      # Add the tab
        self.jobs_columns = ttk.Frame(self.jobs_tab)

        self.jobs_people = ttk.Treeview(columns=self.people_dataCols, show= 'headings')
        self.create_columns(self.people_dataCols, self.jobs_columns, self.jobs_people)
        
        #=============================To Do Tab====================================================================
        self.todo_tab = ttk.Frame(self.tabControl)            # Create a tab 
        self.tabControl.add(self.todo_tab, text="To Do's")      # Add the tab
        self.todo_columns = ttk.Frame(self.todo_tab)

        self.to_do = ttk.Treeview(columns=self.todo_dataCols, show= 'headings')
        self.create_columns(self.todo_dataCols, self.todo_columns, self.to_do)

        #=============================ALL Items Tab====================================================================
        self.items_tab = ttk.Frame(self.tabControl)            # Create a tab 
        self.tabControl.add(self.items_tab, text='Items')      # Add the tab
        self.items_columns = ttk.Frame(self.items_tab)

        self.all_items = ttk.Treeview(columns=self.items_dataCols, show= 'headings')
        self.create_columns(self.items_dataCols, self.items_columns, self.all_items)

        #=============================ALL Tables Tab====================================================================
        self.table_tab = ttk.Frame(self.tabControl)            # Create a tab 
        self.tabControl.add(self.table_tab, text='Tables')      # Add the tab
        self.table_columns = ttk.Frame(self.table_tab)

        self.all_tables = ttk.Treeview(columns=self.table_dataCols, show= 'headings')
        self.create_columns(self.table_dataCols, self.table_columns, self.all_tables)

        #============================== Order of Service Tab =============================================================
        self.oos_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.oos_tab, text='Order of Service')
        self.ceremony_text = Tk.Text(self.oos_tab, font=("Arial", 18))
        self.ceremony_text.pack(side=Tk.TOP, fill=Tk.BOTH, expand=Tk.Y)

        scrolla = Tk.Scrollbar(self.ceremony_text, command=self.ceremony_text.yview)
        scrolla.pack(side="right", fill=Tk.Y, expand=Tk.Y, anchor="e")
        self.ceremony_text['yscrollcommand'] = scrolla.set

        self.formatted_jobs = ["Welcome And Prayer", "Congregational Songs", "Devotional", "Meditation", "Exchange of Vows", "Maid of Honor", "Best Man", "Bridesmaid", "Groomsman", "Bride's Assistants", \
                          "Ceremony Coordinators", "Ceremony Ushers", "Vocalists", "Guest Registrars", "Program Attendants", "Gift Receivers", "Reception Coordinators", "Master of Ceremonies", \
                          "Prayer For Meal", "Host & Hostess", "Bridal Table Servers", "Family Table Servers", "Special Guest Servers", "Guest Servers", "Appetizer Servers", "Cooks", "Dishwashers", "Cleanup", "Florists", "Photography"]
        
        #============================== Ceremony Tab =============================================================
        self.ceremony_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.ceremony_tab, text='Ceremony')
        self.ceremony_instructions = Tk.Text(self.ceremony_tab, font=("Arial", 18))
        self.ceremony_instructions.pack(side=Tk.TOP, fill=Tk.BOTH, expand=Tk.Y)

        scrollb = Tk.Scrollbar(self.ceremony_instructions, command=self.ceremony_instructions.yview)
        scrollb.pack(side="right", fill=Tk.Y, expand=Tk.Y, anchor="e")
        self.ceremony_instructions['yscrollcommand'] = scrollb.set
        
        #============================== Reception Tab =============================================================
        self.reception_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.reception_tab, text='Reception')
        self.reception_instructions = Tk.Text(self.reception_tab, font=("Arial", 18))
        self.reception_instructions.pack(side=Tk.TOP, fill=Tk.BOTH, expand=Tk.Y)

        scrollc = Tk.Scrollbar(self.reception_instructions, command=self.reception_instructions.yview)
        scrollc.pack(side="right", fill=Tk.Y, expand=Tk.Y, anchor="e")
        self.reception_instructions['yscrollcommand'] = scrollc.set

        #============================== Reception Tab =============================================================
        self.songs_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.songs_tab, text='Songs')
        self.songs_list = Tk.Text(self.songs_tab, font=("Arial", 18))
        self.songs_list.pack(side=Tk.TOP, fill=Tk.BOTH, expand=Tk.Y)

        scrolld = Tk.Scrollbar(self.songs_list, command=self.songs_list.yview)
        scrolld.pack(side="right", fill=Tk.Y, expand=Tk.Y, anchor="e")
        self.songs_list['yscrollcommand'] = scrolld.set

        ### Loading initial data when app is run
        self.load_all_data()

    #========================Creating Methods========================================================================

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
        tree.tag_configure("Coming", foreground='green')
        tree.tag_configure("Might Invite", foreground='yellow')
        tree.tag_configure("Not Coming", foreground='red')
        tree.tag_configure("Low", foreground='green')
        tree.tag_configure("Medium", foreground='yellow')
        tree.tag_configure("High", foreground='red')
        tree.tag_configure("Not Started", foreground='red')
        tree.tag_configure("In Progress", foreground='yellow')
        tree.tag_configure("Done", foreground='green')
        
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
        self.search_tree.tag_configure("Coming", foreground='green')
        self.search_tree.tag_configure("Might Invite", foreground='yellow')
        self.search_tree.tag_configure("Not Coming", foreground='red')
        self.search_tree.tag_configure("Low", foreground='green')
        self.search_tree.tag_configure("Medium", foreground='yellow')
        self.search_tree.tag_configure("High", foreground='red')
        self.search_tree.tag_configure("Not Started", foreground='red')
        self.search_tree.tag_configure("In Progress", foreground='yellow')
        self.search_tree.tag_configure("Done", foreground='green')
                    
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
        try:
            self.bibleschool_people.delete(*self.bibleschool_people.get_children())
        except:
            pass

        self.people_invited = 0
        self.people_coming = 0
        self.people_not_coming = 0
        
        sql = "SELECT firstname, lastname, address, numberofpeople, status, job, relationship, family, bibleschool FROM people"
        res = self.cursor.execute(sql)
        
        for row in res:
            firstname = row[0]
            lastname = row[1]
            address = row[2]
            numberofpeople = row[3]
            status = row[4]
            job = row[5]
            relationship = row[6]
            family = row[7]
            bibleschool = row[8]
            
            ### load how many are invited - want to show invited as long as not "Might Invite"
            if status != "Might Invite":
                self.people_invited += numberofpeople
            ### load how many are coming
            if status == "Coming":
                self.people_coming += numberofpeople
            ### load how many are not coming
            if status == "Not Coming":
                self.people_not_coming += numberofpeople
                
            self.invited_label.configure(text="Invited: {}".format(self.people_invited))
            self.coming_label.configure(text="Coming: {}".format(self.people_coming))
            self.not_coming_label.configure(text="Not Coming: {}".format(self.people_not_coming))
            if job == "None":
                self.all_people.insert('', 'end', tags=[status], values=[firstname, lastname, address, numberofpeople, status, "", relationship])
            else:
                self.all_people.insert('', 'end', tags=[status], values=[firstname, lastname, address, numberofpeople, status, job, relationship])
            
            try: 
                if family != "None":
                    if job == "None":
                        self.family_people.insert('', 'end', tags=[family], values=[firstname, lastname, address, numberofpeople, status, "", family])
                    else:
                        self.family_people.insert('', 'end', tags=[family], values=[firstname, lastname, address, numberofpeople, status, job, family])
            except:
                pass
            try: 
                if job != "None":
                    self.jobs_people.insert('', 'end', tags=[status], values=[firstname, lastname, address, numberofpeople, status, job, relationship])
            except:
                pass
            try: 
                if job == "Best Man" or job == "Maid of Honor" or job == "Bridesmaid" or job == "Groomsman":
                    self.bp_people.insert('', 'end', tags=[status], values=[firstname, lastname, address, numberofpeople, status, job, relationship])
            except:
                pass
            try: 
                if bibleschool == 1:
                    if job == "None":
                        self.bibleschool_people.insert('', 'end', tags=[status], values=[firstname, lastname, address, numberofpeople, status, "", relationship])
                    else:
                        self.bibleschool_people.insert('', 'end', tags=[status], values=[firstname, lastname, address, numberofpeople, status, job, relationship])
            except:
                pass

    def load_item_data(self):
        try:
            self.all_items.delete(*self.all_items.get_children())
        except:
            pass

        sql = "SELECT item, description, cost, quantityneeded, whereneeded, buyingstatus, store, importance FROM items WHERE item!=''"
        res = self.cursor.execute(sql)

        for row in res:
            item = row[0]
            desc = row[1]
            cost = row[2]
            quantity = row[3]
            where_need = row[4]
            buying_status = row[5]
            store = row[6]
            importance = row[7]
            
            try:
                self.all_items.insert('', 'end', tags=[importance], values=[item, desc, cost, quantity, where_need, buying_status, store])
            except:
                pass

    def load_task_data(self):
        try:
            self.to_do.delete(*self.to_do.get_children())
        except:
            pass
        
        self.number_tasks = 0
        self.completed_tasks = 0
        
        sql = "SELECT task, whereneeded, importance, category, person, status FROM tasks"
        res = self.cursor.execute(sql)

        for row in res:
            task = row[0]
            where_need = row[1]
            importance = row[2]
            category = row[3]
            person = row[4]
            status = row[5]

            self.number_tasks += 1

            if status == "Done":
                self.completed_tasks += 1

            self.percent_task = (float(self.completed_tasks) / self.number_tasks) * 100
            self.planning_completed_label.config(text="{:.1f}%".format(self.percent_task))
            
            if int(self.percent_task) >= 0 and int(self.percent_task) <= 49:
                self.planning_completed_label.config(foreground="red")
            elif int(self.percent_task) >= 50 and int(self.percent_task) <= 99:
                self.planning_completed_label.config(foreground="yellow")
            else:
                self.planning_completed_label.config(foreground="green")

            try:
                if category == "None":
                    self.to_do.insert('', 'end', tags=[status], values=[task, where_need, importance, "", person, status])
                # elif where_need == "None":
                #     self.to_do.insert('', 'end', tags=[status], values=[task, "", importance, category, person, status])
                
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

        if self.total_cost <= self.budget:
            self.total_cost_price_label.configure(fg="green", text="${:,.2f}".format(self.total_cost))
        else:
            self.total_cost_price_label.configure(fg="red", text="${:,.2f}".format(self.total_cost))

    def load_table_data(self):
        
        sql = "SELECT * FROM tableinfo"
        res = self.cursor.execute(sql)
        for row in res:
            self.tables = row[0]
            if self.is_sections.get() == 0:
                self.table_num_pep = row[1]
                print self.table_num_pep
            else:
                self.table_num_pep = row[1] * self.mul_number.get()
                print self.table_num_pep
            self.is_sections.set(row[2])
            self.mul_number.set(row[3])
            
    def load_tables_data(self):

        try:
            self.all_tables.delete(*self.all_tables.get_children())
        except:
            pass
        
        sql = "SELECT count(*) FROM tables"
        res = self.cursor.execute(sql)

        for row in res:
            self.number = row[0]
        
        if self.number == self.tables and self.old_table_num_pep > 0:
            pass
                
        sql = "Select rowid, people, remaining, relationship, family, notes from tables"
        res = self.cursor.execute(sql)
        
        for row in res:
            
            try:
                if self.is_sections.get() != 0:
                    condition = True
                    hello = row[1].split(",")
                    
                    while condition:
                        self.all_tables.insert('', 'end', tags=[], values=[row[0], ", ".join(hello[0:(self.table_num_pep / self.mul_number.get())]), row[2], row[3], row[4]])
                        break
                    counter = 0
                    for i in range(self.mul_number.get()-1):
                        counter += self.table_num_pep / self.mul_number.get()
                        self.all_tables.insert('', 'end', tags=[], values=["", ", ".join(hello[counter:(self.table_num_pep / self.mul_number.get()) + counter]), "", row[3], row[4]])
                else:
                    self.all_tables.insert('', 'end', tags=[], values=[row[0], row[1], row[2], row[3], row[4]])
            except:    
                pass

    def load_formatted_jobs(self):
        self.ceremony_text.delete(1.0, Tk.END)
        self.ceremony_text.tag_config("title",underline=1)
        for i in self.formatted_jobs:
            sql = "SELECT firstname,lastname,job FROM people WHERE job=(?)"
            res = self.cursor.execute(sql, (i,))
            title = True
            if self.formatted_jobs.index(i) != 0:
                self.ceremony_text.insert(Tk.END, "\n")
            for row in res:
                while title:
                    self.ceremony_text.insert(Tk.END, row[2] + "\n", ("title"))
                    title = False
                # if i == "Maid of Honor":
                #     self.ceremony_text.insert(Tk.TOP, " - " + row[0] + ' ' + row[1] + "\n")
                # else:
                self.ceremony_text.insert(Tk.END, " - " + row[0] + ' ' + row[1] + "\n")
            
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

    def load_store_data(self):
        self.stores = []

        sql = "SELECT store FROM items"
        res = self.cursor.execute(sql)
        self.conn.commit()

        for row in res:
            if row[0] not in self.stores:
                self.stores.append(row[0])

    def load_all_data(self):
        self.load_budget_data()
        self.load_store_data()
        self.load_job_data()
        self.load_table_data()
        self.load_tables_data()
        self.load_cupfam_data()
        self.load_item_data()
        self.load_task_data()
        self.load_people_data()
        self.load_formatted_jobs()
        
        ### Populate the text tabs except ceremony
        try:
            with open("Wedding Files/ceremony.txt", "r") as file:
                for line in file.read():
                    self.ceremony_instructions.insert(Tk.CURRENT, line)
        except IOError:
            pass
        try:
            with open("Wedding Files/reception.txt", "r") as file:
                for line in file.read():
                    self.reception_instructions.insert(Tk.CURRENT, line)
        except IOError:
            pass
        try:
            with open("Wedding Files/songs_list.txt", "r") as file:
                for line in file.read():
                    self.songs_list.insert(Tk.CURRENT, line)
        except IOError:
            pass

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
        self.is_bibleschool_check = Tk.Checkbutton(self.middle_frame, highlightbackground="black", background="gray12", variable=self.is_bibleschool)
        self.is_bibleschool_check.grid(row=6, column=1, sticky="w")

        self.n_coming = Tk.StringVar(self.middle_frame)
        self.n_coming_label = Tk.Label(self.middle_frame, text="Num Coming:", foreground="white", background="gray12")
        self.n_coming_label.grid(row=4, column=1, sticky="e")
        self.n_coming_listbox = Tk.OptionMenu(self.middle_frame, self.n_coming, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
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
        
        table_list = []
        [table_list.append(i) for i in range(1, self.tables + 1)]

        self.tablenum_box = Tk.OptionMenu(self.middle_frame, self.table, 0, *table_list)
        self.tablenum_box.configure(highlightbackground="black", background="gray12", foreground="white", width=5)
        self.table.set(0)
        self.tablenum_box.grid(row=5, column=2, sticky="w")
                    
        self.status = Tk.StringVar(self.middle_frame)
        self.status_label = Tk.Label(self.middle_frame, text="Status:", foreground="white", background="gray12")
        self.status_label.grid(row=1, column=2, sticky="w")
        self.status_listbox = Tk.OptionMenu(self.middle_frame,self.status, "Invited", "Might Invite", "Coming", "Not Coming", command=lambda event: self.update_optionmenu(self.status, self.status_listbox))
        self.status.set("Invited")
        self.status_listbox.configure(highlightbackground="black", foreground="purple", background="gray12", width=12)
        self.status_listbox.grid(row=1, column=3, sticky="w")

        self.people_nlabel = Tk.Label(self.bottom_frame, text="Notes:", foreground="white", background="gray12")
        self.people_nlabel.pack(side="top", anchor="w")
        self.people_ntext = Tk.Text(self.bottom_frame, height=10)
        self.people_ntext.pack(expand=1, fill=Tk.BOTH)

        #self.save_image = Tk.PhotoImage(file="save.gif")
        self.sbutton = Tk.Button(self.toolbar1, text="Add", font=("Arial", 12, "bold", "italic"), highlightbackground="gray25", command=self.save_person_db)
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

        ### Where Item Needed
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

        ### Item Store
        self.item_store = Tk.StringVar(self.item_middle_frame)
        self.item_store_label = Tk.Label(self.item_middle_frame, text="Store:", foreground="white", background="gray12")
        self.item_store_label.grid(row=7, column=0, sticky="w")
        self.item_store_listbox = Tk.OptionMenu(self.item_middle_frame, self.item_store, *self.stores)
        self.item_store_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.item_store.set(self.stores[0])
        self.item_store_listbox.grid(row=7, column=1, sticky="w")


        ### Add note box at bottom
        self.item_nlabel = Tk.Label(self.item_bottom_frame, text="Notes:", foreground="white", background="gray12")
        self.item_nlabel.pack(side="top", anchor="w")
        self.item_ntext = Tk.Text(self.item_bottom_frame, height=10)
        self.item_ntext.pack(expand=1, fill=Tk.BOTH)

        
        #self.update_person_image = Tk.PhotoImage(file="update_person.gif")
        self.a_item_but = Tk.Button(self.item_toolbar1, text="Add", font=("Arial", 12, "bold", "italic"), highlightbackground="gray25",  command=self.save_item_db)
        self.a_item_but.pack(side="left")

    def add_todo_window(self):
        self.todo_window = Tk.Toplevel(self, takefocus=True)
        self.todo_window.wm_title("Add Item")
        self.todo_window.geometry("550x500")

        self.todo_toolbar1 = Tk.Frame(self.todo_window, bd=1, relief=Tk.RAISED, background="gray25")
        
        self.todo_toolbar1.pack(side="top", fill=Tk.X)
        
        self.todo_middle_frame = Tk.Frame(self.todo_window, background="gray12")
        self.todo_middle_frame.pack(expand=1, fill=Tk.BOTH)
        
        self.todo_bottom_frame = Tk.Frame(self.todo_window, background="gray12")
        self.todo_bottom_frame.pack(expand=1, fill=Tk.BOTH)
        
        ### What Task Needs Done
        self.task_label = Tk.Label(self.todo_middle_frame, text="Task:", foreground="white", background="gray12")
        self.task_label.grid(row=0, column=0, sticky="w")
        self.task_ent = Tk.Entry(self.todo_middle_frame, highlightbackground="gray12", width=50)
        self.task_ent.grid(row=0, column=1, sticky="w", pady=5)

        ### Where Task Needed
        self.where_task_needed = Tk.StringVar(self.todo_middle_frame)
        self.where_task_needed_label = Tk.Label(self.todo_middle_frame, text="Where Needed:", foreground="white", background="gray12")
        self.where_task_needed_label.grid(row=1, column=0, sticky="w")
        self.where_task_needed_listbox = Tk.OptionMenu(self.todo_middle_frame, self.where_task_needed, "None", "Ceremony", "Reception")
        self.where_task_needed_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.where_task_needed.set("None")
        self.where_task_needed_listbox.grid(row=1, column=1, sticky="w")

        ### Task Importance
        self.task_importance = Tk.StringVar(self.todo_middle_frame)
        self.task_importance_label = Tk.Label(self.todo_middle_frame, text="Importance:", foreground="white", background="gray12")
        self.task_importance_label.grid(row=2, column=0, sticky="w")
        self.task_importance_listbox = Tk.OptionMenu(self.todo_middle_frame, self.task_importance, "Low", "Medium", "High")
        self.task_importance_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.task_importance.set("Low")
        self.task_importance_listbox.grid(row=2, column=1, sticky="w")

        ### Task Category
        self.task_category = Tk.StringVar(self.todo_bottom_frame)
        self.task_category_label = Tk.Label(self.todo_middle_frame, text="Category:", foreground="white", background="gray12")
        self.task_category_label.grid(row=3, column=0, sticky="w")
        self.task_category_listbox = Tk.OptionMenu(self.todo_middle_frame, self.task_category, "None", "Shopping", "Contacted", "Made","Labor")
        self.task_category_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.task_category.set("None")
        self.task_category_listbox.grid(row=3, column=1, sticky="w")

        ### Who needs to do Task
        self.task_person = Tk.StringVar(self.todo_bottom_frame)
        self.task_person_label = Tk.Label(self.todo_middle_frame, text="Person:", foreground="white", background="gray12")
        self.task_person_label.grid(row=4, column=0, sticky="w")
        self.task_person_listbox = Tk.OptionMenu(self.todo_middle_frame, self.task_person, "Anyone", self.his, self.her, "Other")
        self.task_person_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.task_person.set("Anyone")
        self.task_person_listbox.grid(row=4, column=1, sticky="w")

        ### Task status
        self.task_status = Tk.StringVar(self.todo_middle_frame)
        self.task_status_label = Tk.Label(self.todo_middle_frame, text="Task Status:", foreground="white", background="gray12")
        self.task_status_label.grid(row=5, column=0, sticky="w")
        self.task_status_listbox = Tk.OptionMenu(self.todo_middle_frame, self.task_status, "Not Started", "In Progress", "Done")
        self.task_status_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.task_status.set("Not Started")
        self.task_status_listbox.grid(row=5, column=1, sticky="w")

        ### Add note box at bottom
        self.task_nlabel = Tk.Label(self.todo_bottom_frame, text="Notes:", foreground="white", background="gray12")
        self.task_nlabel.pack(side="top", anchor="w")
        self.task_ntext = Tk.Text(self.todo_bottom_frame, height=10)
        self.task_ntext.pack(expand=1, fill=Tk.BOTH)

        #self.update_person_image = Tk.PhotoImage(file="update_person.gif")
        self.a_todo_but = Tk.Button(self.todo_toolbar1, text="Add", font=("Arial", 12, "bold", "italic"), highlightbackground="gray25",  command=self.save_todo_db)
        self.a_todo_but.pack(side="left")

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

        self.a_job_but = Tk.Button(self.job_window, text="Add", font=("Arial", 7, "bold"), highlightbackground="gray12", command=self.save_job_db)
        self.a_job_but.grid(row=1, column=1, sticky="e")

    def add_delete_store_window(self):
        self.store_window = Tk.Toplevel(self, takefocus=True, background="gray12")
        self.store_window.wm_title("Add/Delete Store")
        self.store_window.geometry("300x75")

        self.store_label = Tk.Label(self.store_window, text="Store:", foreground="white", background="gray12")
        self.store_label.grid(row=0, column=0)
        self.store_ent = Tk.Entry(self.store_window, highlightbackground="gray12", width=20)
        self.store_ent.grid(row=0, column=1, sticky="w")

        self.d_store_but = Tk.Button(self.store_window, text="Delete", font=("Arial", 7, "bold"), highlightbackground="gray12", command=self.delete_store_db)
        self.d_store_but.grid(row=1, column=1)

        self.a_store_but = Tk.Button(self.store_window, text="Add", font=("Arial", 7, "bold"), highlightbackground="gray12", command=self.save_store_db)
        self.a_store_but.grid(row=1, column=1, sticky="e")
              
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
        self.relationship_listbox = Tk.OptionMenu(self.middle_frame, self.relation, "Our Friend", "Cousin", "Aunt", "Uncle", "Aunt & Uncle", "His " + "Friend")
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
        self.is_bibleschool_check = Tk.Checkbutton(self.middle_frame, highlightbackground="black", background="gray12", variable=self.is_bibleschool)
        self.is_bibleschool_check.grid(row=6, column=1, sticky="w")

        self.n_coming = Tk.StringVar(self.middle_frame)
        self.n_coming_label = Tk.Label(self.middle_frame, text="Num Coming:", foreground="white", background="gray12")
        self.n_coming_label.grid(row=4, column=1, sticky="e")
        self.n_coming_listbox = Tk.OptionMenu(self.middle_frame, self.n_coming, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
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
        
        table_list = []
        [table_list.append(i) for i in range(1, self.tables + 1)]

        self.tablenum_box = Tk.OptionMenu(self.middle_frame, self.table, 0, *table_list)
        self.tablenum_box.configure(highlightbackground="black", background="gray12", foreground="white", width=5)
        self.table.set(0)
        self.tablenum_box.grid(row=5, column=2, sticky="w")
        
        self.status = Tk.StringVar(self.middle_frame)
        self.status_label = Tk.Label(self.middle_frame, text="Status:", foreground="white", background="gray12")
        self.status_label.grid(row=1, column=2, sticky="w")
        self.status_listbox = Tk.OptionMenu(self.middle_frame,self.status, "Invited", "Might Invite", "Coming", "Not Coming", command=lambda event: self.update_optionmenu(self.status, self.status_listbox))
        self.status_listbox.configure(highlightbackground="black", background="gray12", width=12)
        self.status.set(status)
        self.update_optionmenu(self.status, self.status_listbox) ### Set the Update Color
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

    def update_view_item_window(self, item, desc, cost, quantity, whereneeded, buyingstatus, importance, store, notes):
        
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
        
        ### Item Store
        self.item_store = Tk.StringVar(self.item_middle_frame)
        self.item_store_label = Tk.Label(self.item_middle_frame, text="Store:", foreground="white", background="gray12")
        self.item_store_label.grid(row=7, column=0, sticky="w")
        self.item_store_listbox = Tk.OptionMenu(self.item_middle_frame, self.item_store, *self.stores)
        self.item_store_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.item_store.set(self.stores[0])
        self.item_store_listbox.grid(row=7, column=1, sticky="w")

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
        self.item_store.set(store)
        self.item_ntext.insert(Tk.CURRENT, notes)

        self.u_item_but = Tk.Button(self.item_toolbar1, text="Update", font=("Arial", 12, "bold", "italic"), highlightbackground="gray25",  command=self.update_item_db)
        self.u_item_but.pack(side="left")

    def update_view_todo_window(self, task, where_need, importance, category, person, status, notes):
        self.view_task = Tk.Toplevel(self, takefocus=True)
        self.view_task.wm_title(" " + task + " " + status)
        self.view_task.geometry("550x500")

        self.todo_toolbar1 = Tk.Frame(self.view_task, bd=1, relief=Tk.RAISED, background="gray25")
        
        self.todo_toolbar1.pack(side="top", fill=Tk.X)
        
        self.todo_middle_frame = Tk.Frame(self.view_task, background="gray12")
        self.todo_middle_frame.pack(expand=1, fill=Tk.BOTH)
        
        self.todo_bottom_frame = Tk.Frame(self.view_task, background="gray12")
        self.todo_bottom_frame.pack(expand=1, fill=Tk.BOTH)
        
        ### What Task Needs Done
        self.task_label = Tk.Label(self.todo_middle_frame, text="Task:", foreground="white", background="gray12")
        self.task_label.grid(row=0, column=0, sticky="w")
        self.task_ent = Tk.Entry(self.todo_middle_frame, highlightbackground="gray12", width=50)
        self.task_ent.grid(row=0, column=1, sticky="w", pady=5)

        ### Where Task Needed
        self.where_task_needed = Tk.StringVar(self.todo_middle_frame)
        self.where_task_needed_label = Tk.Label(self.todo_middle_frame, text="Where Needed:", foreground="white", background="gray12")
        self.where_task_needed_label.grid(row=1, column=0, sticky="w")
        self.where_task_needed_listbox = Tk.OptionMenu(self.todo_middle_frame, self.where_task_needed, "None", "Ceremony", "Reception")
        self.where_task_needed_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.where_task_needed.set("None")
        self.where_task_needed_listbox.grid(row=1, column=1, sticky="w")

        ### Task Importance
        self.task_importance = Tk.StringVar(self.todo_middle_frame)
        self.task_importance_label = Tk.Label(self.todo_middle_frame, text="Importance:", foreground="white", background="gray12")
        self.task_importance_label.grid(row=2, column=0, sticky="w")
        self.task_importance_listbox = Tk.OptionMenu(self.todo_middle_frame, self.task_importance, "Low", "Medium", "High")
        self.task_importance_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.task_importance.set("Low")
        self.task_importance_listbox.grid(row=2, column=1, sticky="w")

        ### Task Category
        self.task_category = Tk.StringVar(self.todo_bottom_frame)
        self.task_category_label = Tk.Label(self.todo_middle_frame, text="Category:", foreground="white", background="gray12")
        self.task_category_label.grid(row=3, column=0, sticky="w")
        self.task_category_listbox = Tk.OptionMenu(self.todo_middle_frame, self.task_category, "None", "Shopping", "Contacted", "Made","Labor")
        self.task_category_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.task_category.set("None")
        self.task_category_listbox.grid(row=3, column=1, sticky="w")

        ### Who needs to do Task
        self.task_person = Tk.StringVar(self.todo_bottom_frame)
        self.task_person_label = Tk.Label(self.todo_middle_frame, text="Person:", foreground="white", background="gray12")
        self.task_person_label.grid(row=4, column=0, sticky="w")
        self.task_person_listbox = Tk.OptionMenu(self.todo_middle_frame, self.task_person, "Anyone", self.his, self.her, "Other")
        self.task_person_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.task_person.set("Anyone")
        self.task_person_listbox.grid(row=4, column=1, sticky="w")

        ### Task status
        self.task_status = Tk.StringVar(self.todo_middle_frame)
        self.task_status_label = Tk.Label(self.todo_middle_frame, text="Task Status:", foreground="white", background="gray12")
        self.task_status_label.grid(row=5, column=0, sticky="w")
        self.task_status_listbox = Tk.OptionMenu(self.todo_middle_frame, self.task_status, "Not Started", "In Progress", "Done")
        self.task_status_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.task_status.set("Not Started")
        self.task_status_listbox.grid(row=5, column=1, sticky="w")

        ### Add note box at bottom
        self.task_nlabel = Tk.Label(self.todo_bottom_frame, text="Notes:", foreground="white", background="gray12")
        self.task_nlabel.pack(side="top", anchor="w")
        self.task_ntext = Tk.Text(self.todo_bottom_frame, height=10)
        self.task_ntext.pack(expand=1, fill=Tk.BOTH)

        ### Fill fields from db
        self.task_ent.insert(0,task)
        self.where_task_needed.set(where_need)
        self.task_importance.set(importance)
        self.task_category.set(category)
        self.task_person.set(person)
        self.task_status.set(status)
        self.task_ntext.insert(Tk.CURRENT,notes)

        #self.update_person_image = Tk.PhotoImage(file="update_person.gif")
        self.u_todo_but = Tk.Button(self.todo_toolbar1, text="Update", font=("Arial", 12, "bold", "italic"), highlightbackground="gray25",  command=self.update_todo_db)
        self.u_todo_but.pack(side="left")

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
        
    def update_view_tableinfo_window(self, tables, numpeptables, is_sections, is_mul):
        self.view_table_window = Tk.Toplevel(self, takefocus=True, background="gray12")
        self.view_table_window.wm_title("Enter/Update Tables")
        self.view_table_window.geometry("250x125")

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
        self.is_sections.set(is_sections)
        self.mul_number.set(is_mul)

        self.mul_tables_label = Tk.Label(self.view_table_window, text="Sections per\ntable:", foreground="white", background="gray12", justify="left")
        self.mul_tables = Tk.Entry(self.view_table_window, highlightbackground="gray12", width=10, textvariable=self.mul_number)
        
        if is_sections == 1:
            self.mul_tables_label.grid(row=3, column=0, sticky="w")
            self.mul_tables.grid(row=3, column=1, sticky="w")
        else:
            try:
                self.mul_tables_label.grid_remove()
                self.mul_tables.grid_remove()
            except:
                pass

        self.u_tables_sections_label = Tk.Label(self.view_table_window, text="Multiple tables\nper table:", foreground="white", background="gray12", justify="left")
        self.u_tables_sections_label.grid(row=2, column=0, sticky="w")
        self.u_tables_sections = Tk.Checkbutton(self.view_table_window, highlightbackground="black", background="gray12", variable=self.is_sections)
        self.u_tables_sections.grid(row=2, column=1, sticky="w")

        self.u_tables_but = Tk.Button(self.view_table_window, text="Submit", font=("Arial", 7, "bold"), highlightbackground="gray12", command=self.update_tableinfo_db)
        self.u_tables_but.grid(row=2, column=2, sticky="w")

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
        self.relationship_listbox = Tk.OptionMenu(self.tables_middle_frame, self.relation, "Our Friend", "Cousin", "Aunt", "Uncle", "Aunt & Uncle", "His " + "Friend")
        self.relationship_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.relation.set("Our Friend")
        self.relationship_listbox.grid(row=0, column=1, sticky="w")

        self.family = Tk.StringVar(self.tables_middle_frame)
        self.family_label = Tk.Label(self.tables_middle_frame, text="Family:", foreground="white", background="gray12")
        self.family_label.grid(row=0, column=3, sticky="w")
        self.family_listbox = Tk.OptionMenu(self.tables_middle_frame, self.family, "None", self.his_dad_fam, self.her_dad_fam, self.his_mom_fam, self.her_mom_fam)
        self.family_listbox.configure(highlightbackground="black", background="gray12", foreground="white", width=12)
        self.family.set("None")
        self.family_listbox.grid(row=0, column=4, sticky="w")

        self.tables_people_label = Tk.Label(self.tables_middle_frame, text="People:", foreground="white", background="gray12")
        self.tables_people_label.grid(row=1, column=0, sticky="nw")
        if self.is_sections.get() == 0:
            self.tables_people_list = Tk.Listbox(self.tables_middle_frame, height=self.table_num_pep)
        else:
            self.tables_people_list = Tk.Listbox(self.tables_middle_frame, height=self.table_num_pep * self.mul_number.get())
        self.tables_people_list.grid(row=1, column=1, sticky="w")
        
        self.tables_nlabel = Tk.Label(self.tables_bottom_frame, text="Notes:", foreground="white", background="gray12")
        self.tables_nlabel.pack(side="top", anchor="w")
        self.tables_ntext = Tk.Text(self.tables_bottom_frame, height=10)
        self.tables_ntext.pack(expand=1, fill=Tk.BOTH)
        
        self.relation.set(relationship)
        self.family.set(family)
        self.tables_ntext.insert(Tk.CURRENT, notes)
        
        sql = "SELECT firstname, lastname, address FROM people WHERE tablenumber=(?)"
        res = self.cursor.execute(sql, (ID,))
        self.conn.commit()
        
        for row in res:
            self.tables_people_list.insert(0, row[0] + " " + row[1])
        self.tables_people_list.bind("<Double-1>", lambda event, arg=self.tables_people_list.curselection(): self.OnDoubleClick(event, arg))
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
            selection2 = tree.item(tree.selection())['values'][2]

            sql = "SELECT ID FROM people WHERE firstname=(?) AND lastname=(?) AND address=(?)"
            self.peoplerowid = self.cursor.execute(sql, (selection, selection1, selection2))
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
                    view_store = info[8]
                    view_notes = info[9]
                    
                    self.update_view_item_window(info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[8], info[9])
            except:
                try:
                    selection = tree.item(tree.selection())['values'][0]
                    selection1 = tree.item(tree.selection())['values'][1]
                    sql = "SELECT ID FROM tasks WHERE task=(?) AND whereneeded=(?)"
                    self.taskrowid = self.cursor.execute(sql, (selection, selection1))
                    
                    sql = "SELECT * FROM tasks WHERE ID=(?)"
                    for row in self.taskrowid:
                        self.taskrowid = row
                    view = self.cursor.execute(sql, (self.taskrowid))
                    
                    for info in view:
                        view_task = info[1]
                        view_where_need = info[2]
                        view_importance = info[3]
                        view_category = info[4]
                        view_person = info[5]
                        view_status = info[6]
                        view_notes = info[7]

                        self.update_view_todo_window(view_task, view_where_need, view_importance, view_category, view_person, \
                                                     view_status, view_notes)
                except:
                    try:
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
                    except:
                        try:
                            selection = self.tables_people_list.get(Tk.ACTIVE)
                            selection, selection1 = selection.split()[0], selection.split()[1]
                
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
        
        if int(var_tablenum) == 0:
            sql = "INSERT INTO people (firstname, lastname, address, phone, relationship, family, bibleschool, numberofpeople, status, job, tablenumber, notes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
            res = self.cursor.execute(sql, (var_n, var_ln, var_address, var_phone, var_relationship, var_fam, var_bibleschool, var_numofpep, var_status, var_job, var_tablenum, var_notes))
            self.conn.commit()
        else:
            sql = "SELECT people, remaining FROM tables WHERE rowid=(?)"
            res = self.cursor.execute(sql, (var_tablenum,))
            self.conn.commit()
            for row in res:
                old_people = row[0]
                old_remaining = row[1]
                if len(old_people) == 0:
                    var_people = var_n + " " + var_ln
                    var_remaining = old_remaining - int(var_numofpep)
                    if int(var_remaining) >= 0 and int(var_remaining) <= self.table_num_pep:
                        sql = "INSERT INTO people (firstname, lastname, address, phone, relationship, family, bibleschool, numberofpeople, status, job, tablenumber, notes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
                        res = self.cursor.execute(sql, (var_n, var_ln, var_address, var_phone, var_relationship, var_fam, var_bibleschool, var_numofpep, var_status, var_job, var_tablenum, var_notes))
                        self.conn.commit()
                        sql = "UPDATE tables SET people=(?), remaining=(?) WHERE rowid=(?)"
                        res = self.cursor.execute(sql, (var_people, var_remaining, var_tablenum))
                        self.conn.commit()
                    else:
                        tkMessageBox.showerror("Error","Can not add to table!\nPlease choose a different table before saving.")
                else:
                    var_people = old_people + ", " + var_n + " " + var_ln
                    var_remaining = old_remaining - int(var_numofpep)
                    if int(var_remaining) >= 0 and int(var_remaining) <= self.table_num_pep:
                        sql = "INSERT INTO people (firstname, lastname, address, phone, relationship, family, bibleschool, numberofpeople, status, job, tablenumber, notes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
                        res = self.cursor.execute(sql, (var_n, var_ln, var_address, var_phone, var_relationship, var_fam, var_bibleschool, var_numofpep, var_status, var_job, var_tablenum, var_notes))
                        self.conn.commit()
                        sql = "UPDATE tables SET people=(?), remaining=(?) WHERE rowid=(?)"
                        res = self.cursor.execute(sql, (var_people, var_remaining, var_tablenum))
                        self.conn.commit()
                    else:
                        tkMessageBox.showerror("Error","Can not add to table!\nPlease choose a different table before saving.")
        
            self.load_tables_data()
            
        # Update People Tree
        self.load_people_data()
        self.load_formatted_jobs()       

    def save_item_db(self):
        save_item = self.item_ent.get() # Get Item
        save_desc = self.item_desc_ent.get() # Get Description
        save_cost = self.item_cost_ent.get() # Get Cost
        save_quantity = self.item_quantity_ent.get() # Get Quantity
        save_where_needed = self.where_needed.get() # Get Where Needed
        save_buying_status = self.buying_status.get() # Get Buying Status
        save_importance = self.item_importance.get() # Get Item Importance
        save_store = self.item_store.get() # Get Store
        save_notes = self.item_ntext.get("1.0", Tk.END) # Get Item Notes

        sql = "INSERT INTO items (item, description, cost, quantityneeded, whereneeded, buyingstatus, importance, store, notes) VALUES (?,?,?,?,?,?,?,?,?)"
        res = self.cursor.execute(sql, (save_item, save_desc, save_cost, save_quantity, save_where_needed, save_buying_status, save_importance, save_store, save_notes))
        self.conn.commit()

        # Update Item Tree
        self.load_item_data()
        self.load_store_data()
        # Update total_cost
        self.load_budget_data()

    def save_todo_db(self):
        save_task = self.task_ent.get() # Get Task
        save_whereneeded = self.where_task_needed.get() # Get Task Whereneeded
        save_importance = self.task_importance.get() # Get Task Importance
        save_category = self.task_category.get() # Get Task Category
        save_person = self.task_person.get() # Get Task Person
        save_status = self.task_status.get() # Get Task Progress Status
        save_notes = self.task_ntext.get("1.0", Tk.END) # Get Task Notes

        sql = "INSERT INTO tasks (task, whereneeded, importance, category, person, status, notes) VALUES (?,?,?,?,?,?,?)"
        res = self.cursor.execute(sql, (save_task, save_whereneeded, save_importance, save_category, save_person, save_status, \
                                        save_notes))
        self.conn.commit()

        self.load_task_data()

    def save_job_db(self):
        save_job = self.job_ent.get() # Get Job

        sql = "INSERT INTO jobs (job) VALUES (?)"
        res = self.cursor.execute(sql, (save_job,))
        self.conn.commit()

        self.load_job_data()

        # Close Window
        self.job_window.destroy()

    def save_store_db(self):
        save_store = self.store_ent.get() # Get Store

        sql = "INSERT INTO items (store) VALUES (?)"
        res = self.cursor.execute(sql, (save_store,))
        self.conn.commit()

        self.load_store_data()

        # Close Window
        self.store_window.destroy()

    def save_tables_db(self):
       
        sql = "SELECT count(*) FROM tables"
        res = self.cursor.execute(sql)

        for row in res:
            self.number = row[0]
        
        if self.number == self.tables and self.old_table_num_pep > 0:
            sql = "SELECT remaining FROM tables"
            res = self.cursor.execute(sql)
            for row in res:
                old_remaining = row[0]
                
                sql = "UPDATE tables SET remaining=(?) WHERE remaining=(?)"
                res = self.cursor.execute(sql, (self.table_num_pep, self.old_table_num_pep))
                
            different = {}
            sql = "SELECT remaining,rowid from tables WHERE remaining!=(?)"
            res = self.cursor.execute(sql, (self.table_num_pep,))
            for row in res:
                different[row[1]] = row[0]
                
            for key, value in different.iteritems():
                if self.old_table_num_pep > self.table_num_pep:
                    sql = "UPDATE tables SET remaining=(?) WHERE rowid=(?)"
                    update_remaining = value - (self.old_table_num_pep - self.table_num_pep)
                    res = self.cursor.execute(sql, (update_remaining, key))
                    self.conn.commit()
                elif self.old_table_num_pep < self.table_num_pep:
                    sql = "UPDATE tables SET remaining=(?) WHERE rowid=(?)"
                    update_remaining = value + (self.table_num_pep - self.old_table_num_pep)
                    res = self.cursor.execute(sql, (update_remaining, key))
                    self.conn.commit()
                else:
                    pass
        
        elif self.number > self.tables:
            ### Dynamic update if number tables decrease and number at table change
            sql = "SELECT remaining FROM tables"
            res = self.cursor.execute(sql)
            for row in res:
                old_remaining = row[0]
                
                sql = "UPDATE tables SET remaining=(?) WHERE remaining=(?)"
                res = self.cursor.execute(sql, (self.table_num_pep, self.old_table_num_pep))
                self.conn.commit()
            
            different = {}
            sql = "SELECT remaining,rowid from tables WHERE remaining!=(?)"
            res = self.cursor.execute(sql, (self.table_num_pep,))
            for row in res:
                different[row[1]] = row[0]
                
            for key, value in different.iteritems():
                if self.old_table_num_pep > self.table_num_pep:
                    sql = "UPDATE tables SET remaining=(?) WHERE rowid=(?)"
                    update_remaining = value - (self.old_table_num_pep - self.table_num_pep)
                    res = self.cursor.execute(sql, (update_remaining, key))
                    self.conn.commit()
                elif self.old_table_num_pep < self.table_num_pep:
                    sql = "UPDATE tables SET remaining=(?) WHERE rowid=(?)"
                    update_remaining = value + (self.table_num_pep - self.old_table_num_pep)
                    res = self.cursor.execute(sql, (update_remaining, key))
                    self.conn.commit()
                else:
                    pass
            
            for row in range((self.number - self.tables)):
                sql = "DELETE FROM tables WHERE rowid = (SELECT MAX(rowid) FROM tables)"
                res = self.cursor.execute(sql)
                self.conn.commit()
            
        else:
            ### Dynamic update if number tables increase and number at table change
            sql = "SELECT remaining FROM tables"
            res = self.cursor.execute(sql)
            for row in res:
                old_remaining = row[0]
                
                sql = "UPDATE tables SET remaining=(?) WHERE remaining=(?)"
                res = self.cursor.execute(sql, (self.table_num_pep, self.old_table_num_pep))
                self.conn.commit()
            
            different = {}
            sql = "SELECT remaining,rowid from tables WHERE remaining!=(?)"
            res = self.cursor.execute(sql, (self.table_num_pep,))
            for row in res:
                different[row[1]] = row[0]
                
            for key, value in different.iteritems():
                if self.old_table_num_pep > self.table_num_pep:
                    sql = "UPDATE tables SET remaining=(?) WHERE rowid=(?)"
                    update_remaining = value - (self.old_table_num_pep - self.table_num_pep)
                    res = self.cursor.execute(sql, (update_remaining, key))
                    self.conn.commit()
                elif self.old_table_num_pep < self.table_num_pep:
                    sql = "UPDATE tables SET remaining=(?) WHERE rowid=(?)"
                    update_remaining = value + (self.table_num_pep - self.old_table_num_pep)
                    res = self.cursor.execute(sql, (update_remaining, key))
                    self.conn.commit()
                else:
                    pass
            
            for row in range((self.tables - self.number)):
                sql = "INSERT INTO tables(people, remaining, relationship, family, notes) VALUES (?,?,?,?,?)"
                res = self.cursor.execute(sql, ("", self.table_num_pep, "", "None", ""))
                self.conn.commit()
        
                
        ### Reload Data
        self.load_tables_data()

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
        
        ### Save old table number before it gets updated
        sql = "SELECT tablenumber, firstname, lastname FROM people WHERE ID=(?)"
        res = self.cursor.execute(sql, (self.peoplerowid))
        self.conn.commit()
        
        for row in res:
            self.tablenum = row[0]
            self.old_firstname = row[1]
            self.old_lastname = row[2]
       
        if int(update_tablenum) == self.tablenum: 
            sql = "UPDATE people SET firstname=(?), lastname=(?), address=(?), phone=(?), relationship=(?), family=(?), bibleschool=(?), numberofpeople=(?), status=(?), job=(?), tablenumber=(?), notes=(?) WHERE ID=(?)"
            res = self.cursor.execute(sql, (update_n, update_ln, update_address, update_phone, update_relationship, update_fam, update_bibleschool, update_numofpep, update_status, \
                                            update_job, update_tablenum, update_notes, self.peoplerowid[0]))
            self.conn.commit()
        else:
            sql = "SELECT people, remaining FROM tables WHERE rowid=(?)"
            res = self.cursor.execute(sql, (int(update_tablenum),))
            for row in res:
                old_people = row[0]
                old_remaining = row[1]
                print row
                old_people = old_people.split()
            sql = "UPDATE tables SET people=(?),remaining=(?) WHERE rowid=(?)"
            ## If adding people
            new_people = update_n + " " + update_ln
            res = self.cursor.execute(sql, (new_people, old_remaining - int(update_numofpep), int(update_tablenum)))
            self.conn.commit()
            sql = "UPDATE people SET tablenumber=(?) WHERE ID=(?)"
            res = self.cursor.execute(sql, (int(update_tablenum), self.peoplerowid[0]))
            self.conn.commit()
            for row in res:
                pass

            self.load_tables_data()

        self.load_tables_data() # Updating the tables when people are updated
        self.load_formatted_jobs() # Loading the text box in a nice format
        
        ### Dynamically update people tabs
    
        self.load_people_data()
        ### Dynamically update the title of the person being edited
        self.update_window_title(self.view_person, update_n, update_ln)
        
        ### Dynamically updating the search tree
        try:
            self.search_tree.delete(*self.search_tree.get_children())
            self.search_tree.insert('', 'end', tags=[update_status], values=[update_n, update_ln, update_phone, update_numofpep, update_status, update_job, update_relationship])
        except:
            pass
        
        self.view_person.destroy()

    def update_item_db(self):
        update_item = self.item_ent.get() # Get Item
        update_desc = self.item_desc_ent.get() # Get Item Desc
        update_cost = self.item_cost_ent.get() # Get Cost
        update_quantity = self.item_quantity_ent.get() # Get Quantity
        update_where_needed = self.where_needed.get() # Get Where Needed
        update_buying_status = self.buying_status.get() # Get Buying Status
        update_importance = self.item_importance.get() # Get Item Importance
        update_store = self.item_store.get() # Get Store
        update_notes = self.item_ntext.get("1.0", Tk.END) # Get Item Notes

        sql = "UPDATE items SET item=(?), description=(?), cost=(?), quantityneeded=(?), whereneeded=(?), buyingstatus=(?), importance=(?), store=?, notes=(?) WHERE ID=(?)"
        res = self.cursor.execute(sql, (update_item, update_desc, update_cost, update_quantity, update_where_needed, update_buying_status, update_importance, update_store, update_notes, self.itemrowid[0]))

        self.conn.commit()
        
        self.load_item_data() # Reload the items tree to reflect changes
        
        self.load_budget_data() # Update the Buget/Total

        self.update_window_title(self.view_item, update_item, update_desc)
        try:
            self.search_tree.delete(*self.search_tree.get_children())
            self.search_tree.insert('', 'end', tags=[update_importance], values=[update_item, update_desc, update_cost, update_quantity, update_where_needed, update_buying_status, update_importance, update_notes])
        except:
            pass


        # Close out the window
        self.view_item.destroy()

    def update_todo_db(self):
        update_task = self.task_ent.get() # Get Task
        update_whereneeded = self.where_task_needed.get() # Get Task Whereneeded
        update_importance = self.task_importance.get() # Get Task Importance
        update_category = self.task_category.get() # Get Task Category
        update_person = self.task_person.get() # Get Task Person
        update_status = self.task_status.get() # Get Task Progress Status
        update_notes = self.task_ntext.get("1.0", Tk.END) # Get Task Notes

        sql = "UPDATE tasks SET task=(?), whereneeded=(?), importance=(?), category=(?), person=(?), status=(?), notes=(?) WHERE ID=(?)"
        res = self.cursor.execute(sql, (update_task, update_whereneeded, update_importance, update_category, update_person, update_status, \
                                        update_notes, self.taskrowid[0]))
        self.conn.commit()
        self.load_task_data()
        self.update_window_title(self.view_task, update_task, update_status)

        # Close Window
        self.todo_window.destroy()

    def update_budget_db(self):
        view_bugdet = self.total_budget_ent.get() # Get budget value

        sql = "UPDATE budget SET budget=(?)"
        res= self.cursor.execute(sql, (view_bugdet,))
        self.conn.commit()

        self.load_budget_data()

    def update_tableinfo_db(self):
        view_tables = self.tables_ent.get() # Get number of tables
        view_numpeptable = self.numpeptable_ent.get() # Get number of people at table
        view_sections = self.is_sections.get() # Get if multiple tables per section
        view_multables = self.mul_number.get() # Get the number of tables in sections
        
        sql = "SELECT numpeptable FROM tableinfo"
        res = self.cursor.execute(sql)
        for row in res:
            self.old_table_num_pep = row[0]

        if view_sections == 1:
            self.mul_tables_label.grid(row=3, column=0, sticky="w")
            self.mul_tables.grid(row=3, column=1, sticky="w")
        else:
            print "destroy"
            try:
                self.mul_tables_label.grid_remove()
                self.mul_tables.grid_remove()
            except:
                pass
        
            
        sql = "UPDATE tableinfo SET numtables=(?), numpeptable=(?), sections=(?), multables=(?)"
        res= self.cursor.execute(sql, (view_tables, view_numpeptable, view_sections, view_multables))
        self.conn.commit()

        self.load_table_data()
        self.save_tables_db()

    def update_tables_db(self):
        view_relationship = self.relation.get()
        view_family = self.family.get()
        view_people = self.tables_people_list.get(0, Tk.END)
        view_table_notes = self.tables_ntext.get("1.0", Tk.END)
        if self.is_sections.get() == 0:
            view_remaining = self.table_num_pep - len(view_people)
        else:
            view_remaining = self.table_num_pep * self.mul_number.get() - len(view_people)
        print view_remaining
        view_people = ", ".join(view_people)

        sql = "UPDATE tables SET relationship=(?), family=(?), people=(?), notes=(?), remaining=(?) WHERE rowid=(?)"
        
        res = self.cursor.execute(sql, (view_relationship, view_family, view_people, view_table_notes, view_remaining, self.tablerowid))
        self.conn.commit()

        self.load_tables_data()

    def update_tables_people_db(self, old_firstname, old_lastname, update_n, update_ln, update_address, update_phone, update_relationship, update_fam, update_bibleschool, update_numofpep, update_status, \
                                update_job, update_tablenum, update_notes):      
        old_name = old_firstname + ' ' + old_lastname
        print self.table_num_pep
        try:
            self.tables_people_list.delete(self.tables_people_list.index(Tk.ACTIVE))
        except:
            pass

        sql = "SELECT people,rowid,remaining FROM tables"
        res = self.cursor.execute(sql)
        for row in res:
            test_name = update_n + " " + update_ln
            old_people = row[0]
            old_table = row[1]
            list_old_people = old_people.split(", ")
            old_remaining = row[2] 
            
            if self.tablenum == 0 and int(update_tablenum) > 0: # If not originally at table, can update
                sql = "SELECT people, remaining FROM tables WHERE rowid=(?)"
                res = self.cursor.execute(sql, (update_tablenum,))
                for row in res:
                    old_people = row[0]
                    old_remaining = row[1]
                    
                    print "old people: " + str(old_people)
                    print "old remaining: " + str(old_remaining)

                    if len(old_people) == 0:
                        print "We're here"
                        update_people = update_n + " " + update_ln
                        update_remaining = old_remaining - int(update_numofpep)
                        print update_remaining
                        print self.table_num_pep
                        ### Make sure Table is not full before updating
                        if update_remaining >= 0 and update_remaining <= self.table_num_pep:
                            sql = "UPDATE tables SET people=(?), remaining=(?) WHERE rowid=(?)"
                            if self.is_sections.get() == 0:
                                res = self.cursor.execute(sql, (update_people, update_remaining, update_tablenum))
                            else:
                                res = self.cursor.execute(sql, (update_people, update_remaining, update_tablenum))
                            self.conn.commit()
                            sql = "UPDATE people SET firstname=(?), lastname=(?), address=(?), phone=(?), relationship=(?), family=(?), bibleschool=(?), numberofpeople=(?), status=(?), job=(?), tablenumber=(?), notes=(?) WHERE ID=(?)"
                            res = self.cursor.execute(sql, (update_n, update_ln, update_address, update_phone, update_relationship, update_fam, update_bibleschool, update_numofpep, update_status, \
                                        update_job, update_tablenum, update_notes, self.peoplerowid[0]))
                            self.conn.commit()
                        else:
                            tkMessageBox.showerror("Error","Can not add to table!\nPlease choose a different table before updating.")
                    else:
                        update_people = old_people + ", " + update_n + " " + update_ln
                        update_remaining = old_remaining - int(update_numofpep)
                        
                        if update_remaining >= 0 and update_remaining <= self.table_num_pep:
                            sql = "UPDATE tables SET people=(?), remaining=(?) WHERE rowid=(?)"
                            if self.is_sections.get():
                                res = self.cursor.execute(sql, (update_people, update_remaining, update_tablenum))
                            else:
                                res = self.cursor.execute(sql, (update_people, update_remaining, update_tablenum))
                            self.conn.commit()
                            sql = "UPDATE people SET firstname=(?), lastname=(?), address=(?), phone=(?), relationship=(?), family=(?), bibleschool=(?), numberofpeople=(?), status=(?), job=(?), tablenumber=(?), notes=(?) WHERE ID=(?)"
                            res = self.cursor.execute(sql, (update_n, update_ln, update_address, update_phone, update_relationship, update_fam, update_bibleschool, update_numofpep, update_status, \
                                        update_job, update_tablenum, update_notes, self.peoplerowid[0]))
                            self.conn.commit()
                        else:
                            tkMessageBox.showerror("Error","Can not add to table!\nPlease choose a different table before updating.")
            elif self.tablenum != 0 and int(update_tablenum) == 0: # Remove from table if were at and don't want there anymore
                sql = "SELECT people, remaining FROM tables WHERE rowid=(?)"
                res = self.cursor.execute(sql, (self.tablenum,))
                self.conn.commit()
                for row in res:
                    old_people = row[0]
                    old_remaining = row[1]
                    list_old_people = old_people.split(", ")
                    
                    if update_n + " " + update_ln == old_name:
                        list_old_people.remove(update_n + " " + update_ln)
                    else:
                        list_old_people.remove(old_name)

                    if len(list_old_people) > 0:
                        update_people = ", ".join(list_old_people)
                    else:
                        update_people = ""
                        
                    update_remaining = old_remaining + int(update_numofpep)
                    
                    if update_remaining >= 0 and update_remaining <= self.table_num_pep:
                        sql = "UPDATE tables SET people=(?), remaining=(?) WHERE rowid=(?)"
                        res = self.cursor.execute(sql, (update_people, update_remaining, self.tablenum))
                        self.conn.commit()
                        sql = "UPDATE people SET firstname=(?), lastname=(?), address=(?), phone=(?), relationship=(?), family=(?), bibleschool=(?), numberofpeople=(?), status=(?), job=(?), tablenumber=(?), notes=(?) WHERE ID=(?)"
                        res = self.cursor.execute(sql, (update_n, update_ln, update_address, update_phone, update_relationship, update_fam, update_bibleschool, update_numofpep, update_status, \
                                    update_job, update_tablenum, update_notes, self.peoplerowid[0]))
                        self.conn.commit()
                    else:
                        tkMessageBox.showerror("Error","Can not add to table!\nPlease choose a different table before updating.")            
            
            if test_name in list_old_people or old_name in list_old_people and int(update_tablenum) != old_table and int(update_tablenum) > 0:
                
                sql = "SELECT people,remaining FROM tables WHERE rowid=(?)"
                res = self.cursor.execute(sql, (update_tablenum,))
                self.conn.commit()
                
                for row in res:
                    new_table = row[0]
                    new_table_list = new_table.split(", ")
                    
                    new_remaining = row[1]
                    if new_table_list == [u""]:
                        update_people = update_n + " " + update_ln
                        update_remaining = self.table_num_pep - int(update_numofpep)
                        
                        if update_remaining >= 0 and update_remaining <= self.table_num_pep:
                            sql = "UPDATE tables SET people=(?), remaining=(?) WHERE rowid=(?)"
                            res = self.cursor.execute(sql, (update_people, update_remaining, update_tablenum))                            
                            self.conn.commit()
                            sql = "UPDATE people SET firstname=(?), lastname=(?), address=(?), phone=(?), relationship=(?), family=(?), bibleschool=(?), numberofpeople=(?), status=(?), job=(?), tablenumber=(?), notes=(?) WHERE ID=(?)"
                            res = self.cursor.execute(sql, (update_n, update_ln, update_address, update_phone, update_relationship, update_fam, update_bibleschool, update_numofpep, update_status, \
                                        update_job, update_tablenum, update_notes, self.peoplerowid[0]))
                            self.conn.commit()
                        else:
                            tkMessageBox.showerror("Error","Can not add to table!\nPlease choose a different table before updating.")
                        # Remove from old table
                        if update_n + " " + update_ln == old_name:
                            list_old_people.remove(update_n + " " + update_ln)
                        else:
                            list_old_people.remove(old_name)
                        
                        if len(list_old_people) > 0:
                            update_people = ", ".join(list_old_people)
                        else:
                            update_people = ""
                        
                        update_remaining = old_remaining + int(update_numofpep)
                        
                        if update_remaining >= 0 and update_remaining <= self.table_num_pep:
                            sql = "UPDATE tables SET people=(?), remaining=(?) WHERE rowid=(?)"
                            res = self.cursor.execute(sql, (update_people, update_remaining, old_table))
                            self.conn.commit()
                            sql = "UPDATE people SET firstname=(?), lastname=(?), address=(?), phone=(?), relationship=(?), family=(?), bibleschool=(?), numberofpeople=(?), status=(?), job=(?), tablenumber=(?), notes=(?) WHERE ID=(?)"
                            res = self.cursor.execute(sql, (update_n, update_ln, update_address, update_phone, update_relationship, update_fam, update_bibleschool, update_numofpep, update_status, \
                                        update_job, update_tablenum, update_notes, self.peoplerowid[0]))
                            self.conn.commit()
                        else:
                            tkMessageBox.showerror("Error","Can not add to table!\nPlease choose a different table before updating.")
                    elif new_table_list != [u""]:
                        # Add to new table
                        update_people = new_table + ", " + update_n + " " + update_ln
                        
                        update_remaining = new_remaining - int(update_numofpep)
                        if update_remaining >= 0 and update_remaining <= self.table_num_pep:
                            sql = "UPDATE tables SET people=(?), remaining=(?) WHERE rowid=(?)"
                            res = self.cursor.execute(sql, (update_people, update_remaining, update_tablenum))
                            self.conn.commit()
                            sql = "UPDATE people SET firstname=(?), lastname=(?), address=(?), phone=(?), relationship=(?), family=(?), bibleschool=(?), numberofpeople=(?), status=(?), job=(?), tablenumber=(?), notes=(?) WHERE ID=(?)"
                            res = self.cursor.execute(sql, (update_n, update_ln, update_address, update_phone, update_relationship, update_fam, update_bibleschool, update_numofpep, update_status, \
                                        update_job, update_tablenum, update_notes, self.peoplerowid[0]))
                            self.conn.commit()
                        else:
                            tkMessageBox.showerror("Error","Can not add to table!\nPlease choose a different table before updating.")
                        # Remove from old table
                        
                        if update_n + " " + update_ln == old_name:
                            list_old_people.remove(update_n + " " + update_ln)
                        else:
                            list_old_people.remove(old_name)
                        
                        if len(list_old_people) > 0:
                            update_people = ", ".join(list_old_people)
                        else:
                            update_people = ""
                        
                        update_remaining = old_remaining + int(update_numofpep)
                        
                        if update_remaining >= 0 and update_remaining <= self.table_num_pep:
                            sql = "UPDATE tables SET people=(?), remaining=(?) WHERE rowid=(?)"
                            res = self.cursor.execute(sql, (update_people, update_remaining, old_table))
                            self.conn.commit()
                            sql = "UPDATE people SET firstname=(?), lastname=(?), address=(?), phone=(?), relationship=(?), family=(?), bibleschool=(?), numberofpeople=(?), status=(?), job=(?), tablenumber=(?), notes=(?) WHERE ID=(?)"
                            res = self.cursor.execute(sql, (update_n, update_ln, update_address, update_phone, update_relationship, update_fam, update_bibleschool, update_numofpep, update_status, \
                                        update_job, update_tablenum, update_notes, self.peoplerowid[0]))
                            self.conn.commit()
                        else:
                            tkMessageBox.showerror("Error","Can not add to table!\nPlease choose a different table before updating.")
                        
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
                if type(cost) == float or type(cost) == int:
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

        # Close Window
        self.view_message_window.destroy()

    def update_optionmenu(self, variable, listbox, event=None):
        print variable.get()
        if variable.get() == "Invited":
            listbox.configure(foreground="purple")
        elif variable.get() == "Coming":
            listbox.configure(foreground="green")
        elif variable.get() == "Might Invite":
            listbox.configure(foreground="yellow")
        elif variable.get() == "Not Coming":
            listbox.configure(foreground="red")

    def search_db(self, event, search):
        
        
        self.cursor.execute("""CREATE VIRTUAL TABLE IF NOT EXISTS peoplesearch USING fts4(ID, firstname, lastname, address, phone, relationship, family, bibleschool, \
                            numberofpeople, status, job, tablenumber, notes)""")
        self.cursor.execute("""CREATE VIRTUAL TABLE IF NOT EXISTS itemsearch USING fts4(ID, item, description, cost, quantityneeded, whereneeded, buyingstatus, importance, store, notes)""")
        self.cursor.execute("""CREATE VIRTUAL TABLE IF NOT EXISTS todosearch USING fts4(ID, task, whereneeded, importance, category, person, status, notes)""")
        
        self.conn.commit()
        
        
        results = self.search.get()
        
        try:
            sear_win_results = self.sear_win_sear.get()
        except:
            pass

        sql = "INSERT INTO peoplesearch SELECT * FROM people"
        res = self.cursor.execute(sql)
        sql = "INSERT INTO itemsearch SELECT * FROM items"
        res = self.cursor.execute(sql)
        sql = "INSERT INTO todosearch SELECT * FROM tasks"
        res = self.cursor.execute(sql)
        self.conn.commit()
        
        sql = "SELECT * FROM peoplesearch WHERE (firstname || ' ' || lastname) LIKE ('%' || ? || '%') OR address LIKE ('%' || ? || '%') OR phone LIKE ('%' || ? || '%') \
                OR relationship LIKE ('%' || ? || '%') OR family LIKE ('%' || ? || '%') OR numberofpeople LIKE ('%' || ? || '%') OR status LIKE ('%' || ? || '%') OR notes LIKE ('%' || ? || '%')"
        sql_items = "SELECT * FROM itemsearch WHERE item LIKE ('%' || ? || '%') OR description LIKE ('%' || ? || '%') OR whereneeded LIKE ('%' || ? || '%') OR buyingstatus LIKE ('%' || ? || '%') \
                OR importance LIKE ('%' || ? || '%') OR notes LIKE ('%' || ? || '%')"
        sql_todos = "SELECT * FROM todosearch WHERE task LIKE ('%' || ? || '%') OR whereneeded LIKE ('%' || ? || '%') OR importance LIKE ('%' || ? || '%') OR category LIKE ('%' || ? || '%') \
                     OR person LIKE ('%' || ? || '%') OR status LIKE ('%' || ? || '%') OR notes LIKE ('%' || ? || '%')"

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
                self.search_tree.insert('', 'end', tags=[row[9]], values=[row[1], row[2], row[3], row[8], row[9], row[10], row[5]])
            
            ### If it wasn't in people try items
            if len(self.search_tree.get_children()) == 0:
                
                res = self.cursor.execute(sql_items, (results, results, results, results, results, results))
                self.conn.commit()

                self.search_tree = ttk.Treeview(self.tree_cols, columns=self.items_dataCols, show= 'headings')

                self.create_search_columns(self.items_dataCols, self.tree_cols)           

                for row in res:
                    self.search_tree.insert('', 'end', tags=[row[6]], values=[row[1], row[2], row[3], row[4], row[5], row[6], row[7]])
                
                ### if still no results check todo's
                if len(self.search_tree.get_children()) == 0:
                    res = self.cursor.execute(sql_todos, (results, results, results, results, results, results, results))
                    
                    self.search_tree = ttk.Treeview(self.tree_cols, columns=self.todo_dataCols, show= 'headings')

                    self.create_search_columns(self.todo_dataCols, self.tree_cols)           

                    for row in res:
                        self.search_tree.insert('', 'end', tags=[row[6]], values=[row[1], row[2], row[3], row[4], row[5], row[6]])

                    sql = "DROP TABLE peoplesearch"
                    self.cursor.execute(sql)
                    self.conn.commit()

                    sql = "DROP TABLE itemsearch"
                    self.cursor.execute(sql)
                    self.conn.commit()

                    sql = "DROP TABLE todosearch"
                    self.cursor.execute(sql)
                    self.conn.commit()
                
            else:
            
                sql = "DROP TABLE peoplesearch"
                self.cursor.execute(sql)
                self.conn.commit()

                sql = "DROP TABLE itemsearch"
                self.cursor.execute(sql)
                self.conn.commit()

                sql = "DROP TABLE todosearch"
                self.cursor.execute(sql)
                self.conn.commit()
            
            
        else:
            self.update_window_title(self.search_window, "Search Results For:", sear_win_results)
            
            res = self.cursor.execute(sql, (sear_win_results, sear_win_results, sear_win_results, sear_win_results, sear_win_results, sear_win_results, sear_win_results, sear_win_results))
            self.conn.commit()
            self.search_tree = ttk.Treeview(self.tree_cols, columns=self.people_dataCols, show= 'headings')
            
            self.create_search_columns(self.people_dataCols, self.tree_cols)
            
            for row in res:
                self.search_tree.insert('', 'end', tags=[row[9]], values=[row[1], row[2], row[3], row[8], row[9], row[10], row[5]])
            
            ### If not in people search items
            if len(self.search_tree.get_children()) == 0:
                res = self.cursor.execute(sql_items, (sear_win_results, sear_win_results, sear_win_results, sear_win_results, sear_win_results, sear_win_results))
                
                self.search_tree = ttk.Treeview(self.tree_cols, columns=self.items_dataCols, show= 'headings')
                self.create_search_columns(self.items_dataCols, self.tree_cols)

                for row in res:
                    self.search_tree.insert('', 'end', tags=[row[6]], values=[row[1], row[2], row[3], row[4], row[5], row[6], row[7]])

                if len(self.search_tree.get_children()) == 0:
                    
                    res = self.cursor.execute(sql_todos, (sear_win_results, sear_win_results, sear_win_results, sear_win_results, sear_win_results, sear_win_results, \
                                                          sear_win_results))
                
                    self.search_tree = ttk.Treeview(self.tree_cols, columns=self.todo_dataCols, show= 'headings')
                    self.create_search_columns(self.todo_dataCols, self.tree_cols)

                    for row in res:
                        self.search_tree.insert('', 'end', tags=[row[6]], values=[row[1], row[2], row[3], row[4], row[5], row[6]])

                    sql = "DROP TABLE peoplesearch"
                    self.cursor.execute(sql)
                    self.conn.commit()

                    sql = "DROP TABLE itemsearch"
                    self.cursor.execute(sql)
                    self.conn.commit()

                    sql = "DROP TABLE todosearch"
                    self.cursor.execute(sql)
                    self.conn.commit()
            else:
                sql = "DROP TABLE peoplesearch"
                self.cursor.execute(sql)
                self.conn.commit()

                sql = "DROP TABLE itemsearch"
                self.cursor.execute(sql)
                self.conn.commit()

                sql = "DROP TABLE todosearch"
                self.cursor.execute(sql)
                self.conn.commit()

    def delete_job_db(self):
        delete_job = self.job_ent.get() # Get Job
                
        sql = "DELETE FROM jobs WHERE job LIKE (?)"
        res = self.cursor.execute(sql, (delete_job,))
        self.conn.commit()
        
        self.load_job_data()

        # Close Window
        self.job_window.destroy()

    def delete_store_db(self):
        delete_store = self.store_ent.get() # Get Store

        sql = "DELETE FROM items WHERE store LIKE (?) AND item IS NULL"
        res = self.cursor.execute(sql, (delete_store,))
        self.conn.commit()
        
        self.load_store_data()

        # Cose Window
        self.store_window.destroy()
           
    def add_person(self):
        self.add_person_window()
            
    def add_item(self):
        self.add_item_window()

    def add_todo(self):
        self.add_todo_window()

    def add_job(self):
        self.add_delete_job_window()

    def add_store(self):
        self.add_delete_store_window()

    def del_people(self):
        people_trees = [self.all_people, self.bp_people, self.family_people, self.bibleschool_people, self.jobs_people]
        keys = range(len(people_trees))
        values = []
        for tree in people_trees:
            values.append(tree.selection())
        selections = dict(zip(keys,values))
        print selections
        current = self.tabControl.index(self.tabControl.select())
        
        def del_from_tree():
            counter = 0
            for tree in people_trees:
                try:
                    selection = tree.item(selections[counter])['values'][0]
                    selection1 = tree.item(selections[counter])['values'][1]
                    selection2 = tree.item(selections[counter])['values'][2]
                except:
                    print "Not all people"
                
                try:
                    selection = tree.item(selections[counter][counter])['values'][0]
                    selection1 = tree.item(selections[counter][counter])['values'][1]
                    selection2 = tree.item(selections[counter][counter])['values'][2]
                    print selection
                    print selection1
                    print selection2
                except:
                    print "Not all people"
                counter += 1
            print self.all_people.item(selections[0][0])['values']
            print self.all_people.item(selections[0][1])['values']
            sql = "SELECT ID FROM people WHERE firstname=(?) AND lastname=(?) AND phone=(?)"
            peoplerowid = self.cursor.execute(sql, (selection, selection1, selection2))
            
            for row in peoplerowid:
                sql = "DELETE FROM people WHERE ID=(?)"
                self.cursor.execute(sql, (row[0],))
                self.conn.commit()
                self.load_people_data()

        if self.tabControl.tab(current, 'text') == 'People':
            del_from_tree()
        elif self.tabControl.tab(current, 'text') == 'Bridal Party':
            del_from_tree()
        elif self.tabControl.tab(current, 'text') == 'Family':
            del_from_tree()
        elif self.tabControl.tab(current, 'text') == 'Bible School':
            del_from_tree()
        elif self.tabControl.tab(current, 'text') == 'Jobs':
            del_from_tree()
        else:
            tkMessageBox.showerror("Error","Please select a Person and try again.")

    def del_item(self):
        pass
        # selection = tree.item(tree.selection())['values'][0]
        # selection1 = tree.item(tree.selection())['values'][1]

        # sql = "SELECT ID FROM items WHERE item=(?) AND description=(?)"
        # itemrowid = self.cursor.execute(sql, (selection, selection1))
        # self.conn.commit()
        # for row in itemrowid:
        #     sql = "DELETE FROM items WHERE ID=(?)"
        #     self.cursor.execute(sql, (row[0],))
        #     self.conn.commit()
        #     self.load_item_data()

    def del_todo(self):
        pass
        
    def update_window_title(self, window, firstname, lastname):
        window.wm_title(" " + firstname + " " + lastname)
        
    def create_tab(self, tab, columns, tree, datacols, name):
        pass

    def destroy_window(self, window):
        window.destroy()

    def quit_main(self):
        with open("Wedding Files/order_of_service.txt", "w") as file:
            file.write(self.ceremony_text.get("1.0", Tk.END).encode("UTF-8"))
        with open("Wedding Files/ceremony.txt", "w") as file:
            file.write(self.ceremony_instructions.get("1.0", Tk.END).encode("UTF-8"))
        with open("Wedding Files/reception.txt", "w") as file:
            file.write(self.reception_instructions.get("1.0", Tk.END).encode("UTF-8"))
        with open("Wedding Files/songs_list.txt", "w") as file:
            file.write(self.songs_list.get("1.0", Tk.END).encode("UTF-8"))
        

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

