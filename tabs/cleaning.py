from nicegui import ui
from tabs.database import Database

db = Database()

rooms = ['Kitchen', 'Living Room', 'Bedroom']
schedules = ['Daily', 'Weekly', 'Monthly']

def add_cleaning(cleaning_item):
    db.add_cleaning(cleaning_item['name'], cleaning_item['room'], cleaning_item['schedule'], cleaning_item['done'], cleaning_item['user_id'])
    cleaning_ui.refresh()
    
def remove_cleaning(cleaning_id):
    db.remove_cleaning(cleaning_id)
    cleaning_ui.refresh()
    
def toggle_done(cleaning_id):
    db.update_cleaning(cleaning_id, not bool(db.get_cleaning(cleaning_id)['done']))
    cleaning_ui.refresh()
    
def reset_cleaning(schedule):
    cleaning_items = db.get_all_cleaning()
    for c in cleaning_items:
        if c['schedule'] == schedule:
            db.update_cleaning(c['id'], False)
    cleaning_ui.refresh()

@ui.refreshable
def cleaning_ui(app_data):
    users = dict(db.get_users())
    cleaning_items = db.get_all_cleaning()
    
    with ui.tabs().classes('w-full').props('no-caps') as tabs:
        sort_room = ui.tab('Rooms')
        sort_schedule = ui.tab('Schedules')
        sort_user = ui.tab('Users')

    with ui.tab_panels(tabs, value=sort_room).classes('w-full'):
        with ui.tab_panel(sort_room):
            # sort items into rooms
            with ui.grid().classes('grid md:grid-cols-3 gap-2 w-full'):
                for r in rooms:
                    with ui.card().style('border-radius:10px;'):
                        ui.label(r)
                        with ui.grid(columns='2fr 1fr 1fr auto auto').classes('w-full items-center gap-0'):
                            ui.label('Name').classes('border-l-2 border-b-2 p-3')
                            ui.label('Schedule').classes('border-l-2 border-b-2 p-3')
                            ui.label('User').classes('border-l-2 border-b-2 p-3')
                            ui.label('')
                            ui.label('')
                            
                            for c in cleaning_items:
                                if c['room'] == r:
                                    if c['done']:
                                        ui.label(c['name']).classes('border-l-2 p-3 line-through')
                                        ui.label(c['schedule']).classes('border-l-2 p-3 line-through')
                                        ui.label(users[c['user_id']]).classes('border-l-2 p-3 line-through')
                                    else:
                                        ui.label(c['name']).classes('border-l-2 p-3')
                                        ui.label(c['schedule']).classes('border-l-2 p-3')
                                        ui.label(users[c['user_id']]).classes('border-l-2 p-3')
                                    ui.checkbox(value=bool(c['done']), on_change=lambda c=c: toggle_done(c['id']))
                                    ui.button(on_click=lambda c=c: remove_cleaning(c['id']), icon='delete').props('flat fab-mini color=grey')
        
        with ui.tab_panel(sort_schedule):
            # sort items into schedules
            with ui.grid().classes('grid md:grid-cols-3 gap-2 w-full'):
                for s in schedules:
                    with ui.card().style('border-radius:10px;'):
                        ui.label(s)
                        with ui.grid(columns='2fr 1fr 1fr auto auto').classes('w-full items-center gap-0'):
                            ui.label('Name').classes('border-l-2 border-b-2 p-3')
                            ui.label('Room').classes('border-l-2 border-b-2 p-3')
                            ui.label('User').classes('border-l-2 border-b-2 p-3')
                            ui.button(on_click=lambda s=s: reset_cleaning(s), icon='replay').props('flat fab-mini color=grey').classes('border-l-2 border-b-2 p-3')
                            ui.label('')
                            
                            for c in cleaning_items:
                                if c['schedule'] == s:
                                    if c['done']:
                                        ui.label(c['name']).classes('border-l-2 p-3 line-through')
                                        ui.label(c['room']).classes('border-l-2 p-3 line-through')
                                        ui.label(users[c['user_id']]).classes('border-l-2 p-3 line-through')
                                    else:
                                        ui.label(c['name']).classes('border-l-2 p-3')
                                        ui.label(c['room']).classes('border-l-2 p-3')
                                        ui.label(users[c['user_id']]).classes('border-l-2 p-3')
                                    ui.checkbox(value=bool(c['done']), on_change=lambda c=c: toggle_done(c['id']))
                                    ui.button(on_click=lambda c=c: remove_cleaning(c['id']), icon='delete').props('flat fab-mini color=grey')

        with ui.tab_panel(sort_user):
            # sort items into users
            with ui.grid().classes('grid md:grid-cols-3 gap-2 w-full'):
                print(users)
                for u_id, u_name in users.items():
                    with ui.card().style('border-radius:10px;'):
                        ui.label(u_name)
                        with ui.grid(columns='2fr 1fr 1fr auto auto').classes('w-full items-center gap-0'):
                            ui.label('Name').classes('border-l-2 border-b-2 p-3')
                            ui.label('Room').classes('border-l-2 border-b-2 p-3')
                            ui.label('Schedule').classes('border-l-2 border-b-2 p-3')
                            ui.label('')
                            ui.label('')
                            
                            for c in cleaning_items:
                                if c['user_id'] == u_id:
                                    if c['done']:
                                        ui.label(c['name']).classes('border-l-2 p-3 line-through')
                                        ui.label(c['room']).classes('border-l-2 p-3 line-through')
                                        ui.label(c['schedule']).classes('border-l-2 p-3 line-through')
                                    else:
                                        ui.label(c['name']).classes('border-l-2 p-3')
                                        ui.label(c['room']).classes('border-l-2 p-3')
                                        ui.label(c['schedule']).classes('border-l-2 p-3')
                                    ui.checkbox(value=bool(c['done']), on_change=lambda c=c: toggle_done(c['id']))
                                    ui.button(on_click=lambda c=c: remove_cleaning(c['id']), icon='delete').props('flat fab-mini color=grey')
        
    # ui card to add new clearning item
    with ui.card():
        with ui.row().classes('items-center'):
            cleaning_item = {'name': '', 'room': rooms[0], 'schedule': schedules[0], 'done': False, 'user_id': app_data['current_user']['id']}
            ui.input('Name').bind_value(cleaning_item, 'name')
            ui.select(rooms).bind_value(cleaning_item, 'room')
            ui.select(schedules).bind_value(cleaning_item, 'schedule')
            ui.select(users).bind_value(cleaning_item, 'user_id')
            ui.button(on_click=lambda: add_cleaning(cleaning_item), icon='add').props('flat fab-mini color=grey')