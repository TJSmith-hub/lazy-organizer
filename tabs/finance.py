from nicegui import ui

# ui for the finance tab using a table of monthly expenses
@ui.refreshable
def expences_ui(app_data):
    ui.label('Expences')
    if app_data['current_user']['name'] != 'Shared':
        for user in app_data['users']:
            if user['name'] == app_data['current_user']['name']:
                expences_data = user['expences']
    else:
        expences_data = []
    
    expences_columns = ['Name', 'Category', 'Frequency', 'Cost']
    expences_rows = []

    for expence in expences_data:
        expences_rows.append([expence['name'], expence['category'], expence['frequency'], expence['cost']])

    ui.grid(columns=expences_columns, rows=expences_rows)
    
    if app_data['current_user']['name'] != 'Shared':
        new_expence = {'name': '', 'category': '', 'frequency': '', 'cost': ''}
        with ui.card().style('margin: 10px; border-radius:10px;'):
            with ui.row():
                ui.input('Name').bind_value(new_expence, 'name')
                ui.select(['Groceries', 'Utilities', 'Entertainment', 'Other']).bind_value(new_expence, 'category')
                ui.select(['Weekly', 'Monthly', 'Yearly']).bind_value(new_expence, 'frequency')
                ui.input('cost').bind_value(new_expence, 'cost')
                ui.button(on_click=lambda: add_expence(app_data, new_expence), icon='add').props('flat fab-mini color=grey')
        
        
def add_expence(app_data, expence):
    for user in app_data['users']:
        if user['name'] == app_data['current_user']['name']:
            user['expences'].append(expence)
    expences_ui.refresh()