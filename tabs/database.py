import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()
        self.c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)')
        self.c.execute('CREATE TABLE IF NOT EXISTS task_lists (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, user_id INTEGER, shared BOOLEAN, FOREIGN KEY(user_id) REFERENCES users(id))')
        self.c.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, difficulty TEXT, done BOOLEAN, list_id INTEGER, FOREIGN KEY(list_id) REFERENCES task_lists(id))')
        self.c.execute('CREATE TABLE IF NOT EXISTS expences (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, category TEXT, frequency TEXT, cost INTEGER, user_id INTEGER, FOREIGN KEY(user_id) REFERENCES users(id))')
        
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

    def remove_user(self, id):
        # get user name
        self.c.execute('SELECT name FROM users WHERE id = ?', (id,))
        name = self.c.fetchone()[0]
        if name != 'Shared':
            self.c.execute('DELETE FROM users WHERE id = ?', (id,))
            self.c.execute('DELETE FROM task_lists WHERE user_id = ?', (id,))
            self.c.execute('DELETE FROM tasks WHERE list_id IN (SELECT id FROM task_lists WHERE user_id = ?)', (id,))
            self.c.execute('DELETE FROM expences WHERE user_id = ?', (id,))
            self.conn.commit()

    # add, get and remove task lists
    def add_task_list(self, name, shared, user_id):
        self.c.execute('INSERT INTO task_lists (name, shared, user_id) VALUES (?, ?, ?)', (name, shared, user_id))
    
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

    def get_tasks(self, list_id):
        self.c.execute('SELECT * FROM tasks WHERE list_id = ?', (list_id,))
        return self.c.fetchall()

    def remove_task(self, task_id):
        self.c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
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

    def close(self):
        self.conn.close()