from nicegui import ui
from tabs.database import Database

db = Database()

def add_task_list(app_data, task_list):
    db.add_task_list(task_list['name'], task_list['shared'], app_data['current_user']['id'])
    list_ui.refresh()
    
def remove_task_list(app_data, task_list_id):
    db.remove_task_list(task_list_id)
    list_ui.refresh()
    
def add_task(app_data, task, list_id):
    db.add_task(task['name'], task['difficulty'], task['done'], list_id)
    list_ui.refresh()
            
def remove_task(app_data, task_id):
    db.remove_task(task_id)
    list_ui.refresh()
    
def toggle_done(app_data, task_id):
    db.update_task(task_id, not bool(db.get_task(task_id)['done']))
    list_ui.refresh()

ColorMap = {'Easy': 'lightgreen', 'Medium': 'lightyellow', 'Hard': 'lightcoral'}

@ui.refreshable
def tasks_list_ui(app_data, task_list):
    with ui.row().classes('items-center w-full'):
        ui.label(task_list['name']).classes('flex-grow text-2xl')
        ui.button(on_click=lambda: remove_task_list(app_data, task_list['id']), icon='delete').props('flat fab-mini color=grey')
    tasks = db.get_tasks_from_list(task_list['id'])
    if len(tasks) == 0:
        ui.label('List is empty.')
    else:
        for item in tasks:
            with ui.row().classes('items-center w-full').style(f'background-color: {ColorMap[item[2]]}; border-radius: 10px;'):
                ui.checkbox(value=bool(item['done']), on_change=lambda item=item: toggle_done(app_data, item['id']))
                ui.label(item[1]).classes('flex-grow text-black')
                ui.button(on_click=lambda item=item: remove_task(app_data, item['id']), icon='delete').props('flat fab-mini color=grey')

    new_task = {'name': '', 'difficulty': 'Easy', 'done': False}

    with ui.row().classes('items-center'):
        ui.input('Name').classes('flex-grow').bind_value(new_task, 'name')
        ui.select(['Easy', 'Medium', 'Hard']).bind_value(new_task, 'difficulty')
        ui.button(on_click=lambda new_task=new_task: add_task(app_data, new_task, task_list['id']), icon='add').props('flat fab-mini color=grey')
        
@ui.refreshable
def list_ui(app_data):
    
    
    # Get current visible task lists
    if app_data['current_user']['name'] == 'Shared':
        task_lists = []
        for user in db.get_users():
            user_task_lists = db.get_task_lists(user['id'])
            for l in user_task_lists:
                if l['shared']:
                    task_lists.append(l)
    else:
        task_lists = db.get_task_lists(app_data['current_user']['id'])

    for l in task_lists:
        print(l['name'])
    
    # Display task list cards
    with ui.row():
        for l in task_lists:
            with ui.card().style('margin: 10px; border-radius:10px;'):
                tasks_list_ui(app_data, l)
    
    # New task list form card
    if app_data['current_user']['id'] != 'Shared':
        new_list= {'name': '', 'shared': False}
        
        with ui.card().style('margin: 10px; border-radius:10px;'):
            ui.input('New list name').bind_value(new_list, 'name')
            with ui.row():
                ui.checkbox('Shared').bind_value(new_list, 'shared')
                ui.button(on_click=lambda: add_task_list(app_data, new_list), icon='add').props('flat fab-mini color=grey')
