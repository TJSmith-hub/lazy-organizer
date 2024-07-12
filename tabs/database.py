import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()
        
        self.c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT
        )''')
        
        self.c.execute('''CREATE TABLE IF NOT EXISTS task_lists (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT, 
            shared BOOLEAN, 
            user_id INTEGER, 
            FOREIGN KEY(user_id) REFERENCES users(id)
        )''')
        
        self.c.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT, 
            difficulty TEXT, 
            done BOOLEAN, 
            list_id INTEGER, 
            FOREIGN KEY(list_id) REFERENCES task_lists(id)
        )''')
        
        self.c.execute('''CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT, 
            frequency TEXT, 
            income INTEGER, 
            user_id INTEGER, 
            FOREIGN KEY(user_id) REFERENCES users(id)
        )''')
        
        self.c.execute('''CREATE TABLE IF NOT EXISTS expences (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT, 
            category TEXT, 
            frequency TEXT, 
            cost INTEGER, 
            user_id INTEGER, 
            FOREIGN KEY(user_id) REFERENCES users(id))''')
        
        self.c.execute('''CREATE TABLE IF NOT EXISTS cleaning (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT, 
            room TEXT, 
            schedule TEXT,
            done BOOLEAN,
            user_id INTEGER, 
            FOREIGN KEY(user_id) REFERENCES users(id)
        )''')
        
        # add default users
        if len(self.get_users()) == 0:
            self.add_user('Shared')
        
        self.conn.commit()
        
    # add, get and remove users
    def add_user(self, name):
        self.c.execute('INSERT INTO users (name) VALUES (?)', (name,))
        self.conn.commit()

    def get_users(self):
        self.c.execute('SELECT * FROM users')
        return self.c.fetchall()
    
    def get_user(self, id):
        self.c.execute('SELECT * FROM users WHERE id = ?', (id,))
        return self.c.fetchone()

    def remove_user(self, id):
        # get user name
        self.c.execute('SELECT name FROM users WHERE id = ?', (id,))
        name = self.c.fetchone()[0]
        if name != 'Shared':
            self.c.execute('DELETE FROM users WHERE id = ?', (id,))
            self.c.execute('DELETE FROM task_lists WHERE user_id = ?', (id,))
            self.c.execute('DELETE FROM tasks WHERE list_id IN (SELECT id FROM task_lists WHERE user_id = ?)', (id,))
            self.c.execute('DELETE FROM income WHERE user_id = ?', (id,))
            self.c.execute('DELETE FROM expences WHERE user_id = ?', (id,))
            self.conn.commit()

    # add, get and remove task lists
    def add_task_list(self, name, shared, user_id):
        self.c.execute('INSERT INTO task_lists (name, shared, user_id) VALUES (?, ?, ?)', (name, shared, user_id))
        self.conn.commit()
        
    def get_task_lists(self, user_id):
        self.c.execute('SELECT * FROM task_lists WHERE user_id = ?', (user_id,))
        return self.c.fetchall()

    def remove_task_list(self, list_id):
        self.c.execute('DELETE FROM task_lists WHERE id = ?', (list_id,))
        self.c.execute('DELETE FROM tasks WHERE list_id = ?', (list_id,))
        self.conn.commit()
    
    # add, get and remove tasks
    def add_task(self, name, difficulty, done, list_id):
        self.c.execute('INSERT INTO tasks (name, difficulty, done, list_id) VALUES (?, ?, ?, ?)', (name, difficulty, done, list_id))
        self.conn.commit()
        
    def update_task(self, task_id, done):
        self.c.execute('UPDATE tasks SET done = ? WHERE id = ?', (done, task_id))
        self.conn.commit()

    def get_tasks_from_list(self, list_id):
        self.c.execute('SELECT * FROM tasks WHERE list_id = ?', (list_id,))
        return self.c.fetchall()
    
    def get_task(self, task_id):
        self.c.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        return self.c.fetchone()

    def remove_task(self, task_id):
        self.c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        self.conn.commit()
        
    # add, get and remove income
    def add_income(self, name, frequency, income, user_id):
        self.c.execute('INSERT INTO income (name, frequency, income, user_id) VALUES (?, ?, ?, ?)', (name, frequency, income, user_id))
        self.conn.commit()

    def get_income(self, user_id):
        self.c.execute('SELECT * FROM income WHERE user_id = ?', (user_id,))
        return self.c.fetchall()
        
    def remove_income(self, income_id):
        self.c.execute('DELETE FROM income WHERE id = ?', (income_id,))
        self.conn.commit()
            
    # add, get and remove expences
    def add_expence(self, name, category, frequency, cost, user_id):
        self.c.execute('INSERT INTO expences (name, category, frequency, cost, user_id) VALUES (?, ?, ?, ?, ?)', (name, category, frequency, cost, user_id))
        self.conn.commit()

    def get_expences(self, user_id):
        self.c.execute('SELECT * FROM expences WHERE user_id = ?', (user_id,))
        return self.c.fetchall()

    def remove_expence(self, expence_id):
        self.c.execute('DELETE FROM expences WHERE id = ?', (expence_id,))
        self.conn.commit()
        
    def add_cleaning(self, name, room, schedule, done, user_id):
        self.c.execute('INSERT INTO cleaning (name, room, schedule, done, user_id) VALUES (?, ?, ?, ?, ?)', (name, room, schedule, done, user_id))
        self.conn.commit()
    
    def get_cleaning(self, user_id):
        self.c.execute('SELECT * FROM cleaning WHERE user_id = ?', (user_id,))
        return self.c.fetchone()
    
    def get_all_cleaning(self):
        self.c.execute('SELECT * FROM cleaning')
        return self.c.fetchall()
    
    def update_cleaning(self, cleaning_id, done):
        self.c.execute('UPDATE cleaning SET done = ? WHERE id = ?', (done, cleaning_id))
        self.conn.commit()
    
    def remove_cleaning(self, cleaning_id):
        self.c.execute('DELETE FROM cleaning WHERE id = ?', (cleaning_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()