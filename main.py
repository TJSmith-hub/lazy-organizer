from nicegui import ui, app
from tabs.tasks import list_ui
from tabs.finance import finance_ui
from tabs.cleaning import cleaning_ui
from tabs.database import Database

def init():
    ui.dark_mode().enable()
    if 'current_user' not in app_data:
        app_data['current_user'] = {}

def set_user(user):
    app_data['current_user'] = dict(user)
    list_ui.refresh()
    finance_ui.refresh()
    cleaning_ui.refresh()
    
def remove_user(user):
    db.remove_user(user)
    set_user(db.get_users()[0])
    user_tabs_ui.refresh()
    
def add_user(user):
    db.add_user(user)
    user_tabs_ui.refresh()

@ui.refreshable
def user_tabs_ui():
    new_user = {'name': ''}
    with ui.row().classes('w-full items-center'):
        
        with ui.tabs().classes('flex-grow').props('no-caps') as user_tabs:
            for user in db.get_users():
                ui.tab(user['name']).on('click', lambda user=user: set_user(user))
                
        user_tabs.set_value(app_data['current_user']['name'])
                
        ui.button(on_click=lambda: remove_user(app_data['current_user']['id']), icon='delete').props('flat fab-mini color=grey')
        ui.input('New User').bind_value(new_user, 'name')
        ui.button(on_click=lambda: add_user(new_user['name']), icon='add').props('flat fab-mini color=grey')

app_data = app.storage.general
db = Database()
init()
user_tabs_ui()

with ui.tabs().classes('w-full').props('no-caps') as tabs:
    tasks = ui.tab('Tasks')
    cleaning = ui.tab('Cleaning')
    finance = ui.tab('Finance')

with ui.tab_panels(tabs, value=tasks).classes('w-full'):
    with ui.tab_panel(tasks):
        list_ui(app_data)
    with ui.tab_panel(cleaning):
        cleaning_ui(app_data)
    with ui.tab_panel(finance):
        finance_ui(app_data)

ui.run()
