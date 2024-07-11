from nicegui import ui
from tabs.database import Database

db = Database()

expence_categories = ['Transport', 'Food', 'Entertainment', 'Bills', 'Pets', 'Other']

def add_income(app_data, income):
    if income['income'].replace('.', '').isdigit():
        db.add_income(income['name'], income['frequency'], income['income'], app_data['current_user']['id'])
    finance_ui.refresh()

def delete_income(app_data, income_id):
    db.remove_income(income_id)
    finance_ui.refresh()

def add_expence(app_data, expence):
    if expence['cost'].replace('.', '').isdigit():
        db.add_expence(expence['name'], expence['category'], expence['frequency'], expence['cost'], app_data['current_user']['id'])
    finance_ui.refresh()
    
def delete_expence(app_data, expence_id):
    db.remove_expence(expence_id)
    finance_ui.refresh()

# ui for the finance tab using a table of monthly expenses
@ui.refreshable
def finance_ui(app_data):
    
    with ui.grid(columns=2).classes('w-full gap-2'):
        # display income
        with ui.card().classes('w-full'):
            ui.label('Income')
            # get income
            if app_data['current_user']['name'] == 'Shared':
                income_rows = []
                for user in db.get_users():
                    income_rows += db.get_income(user['id'])
            else:
                income_rows = db.get_income(app_data['current_user']['id'])
            
            with ui.grid(columns='1fr 1fr 1fr auto').classes('w-full items-center'):
                ui.label('Name')
                ui.label('Frequency')
                ui.label('Income')
                ui.label('')
                
                for row in income_rows:
                    ui.label(row['name'])
                    ui.label(row['frequency'])
                    ui.label(row['income'])
                    ui.button(on_click=lambda row=row: delete_income(app_data, row['id']), icon='delete').props('flat fab-mini color=grey')
                
                # add new income card
                if app_data['current_user']['name'] != 'Shared':
                    new_income = {'name': '', 'frequency': '', 'income': ''}
                    ui.input('Name').bind_value(new_income, 'name')
                    ui.select(['Monthly', 'Annually']).bind_value(new_income, 'frequency')
                    ui.input('£', validation={'Must be a number': lambda value: value.replace('.', '').isdigit()}).bind_value(new_income, 'income')
                    ui.button(on_click=lambda new_income=new_income: add_income(app_data, new_income), icon='add').props('flat fab-mini color=grey')

        # display expences
        with ui.card().classes('w-full'):
            ui.label('Expences')
            # get expences
            if app_data['current_user']['name'] == 'Shared':
                expences_rows = []
                for user in db.get_users():
                    expences_rows += db.get_expences(user['id'])
            else:
                expences_rows = db.get_expences(app_data['current_user']['id'])
            
            with ui.grid(columns='1fr 1fr 1fr 1fr auto').classes('w-full items-center gap-0'):
                ui.label('Name')
                ui.label('Category')
                ui.label('Frequency')
                ui.label('Cost')
                ui.label('')
                
                for row in expences_rows:
                    ui.label(row['name'])
                    ui.label(row['category'])
                    ui.label(row['frequency'])
                    ui.label(row['cost'])
                    ui.button(on_click=lambda row=row: delete_expence(app_data, row['id']), icon='delete', ).props('flat fab-mini color=grey size=3')
                
                # add new expence card
                if app_data['current_user']['name'] != 'Shared':
                    new_expence = {'name': '', 'category': '', 'frequency': '', 'cost': ''}
                    ui.input('Name').bind_value(new_expence, 'name')
                    ui.select(expence_categories).bind_value(new_expence, 'category')
                    ui.select(['Weekly', 'Monthly', 'Annually']).bind_value(new_expence, 'frequency')
                    ui.input('£', validation={'Must be a number': lambda value: value.replace('.', '').isdigit()}).bind_value(new_expence, 'cost')
                    ui.button(on_click=lambda: add_expence(app_data, new_expence), icon='add').props('flat fab-mini color=grey')
            
        # display stats

        with ui.card().classes('w-full'):
            ui.label('Stats')

            income = db.get_income(app_data['current_user']['id'])
            total_income = 0
            # normalise income to annually
            for row in income:
                if row['frequency'] == 'Monthly':
                    total_income += row['income'] * 12
                elif row['frequency'] == 'Annually':
                    total_income += row['income']
        
            
            expences = db.get_expences(app_data['current_user']['id'])
            total_expences = 0
            for row in expences:
                if row['frequency'] == 'Weekly':
                    total_expences += row['cost'] * 52
                elif row['frequency'] == 'Monthly':
                    total_expences += row['cost'] * 12
                elif row['frequency'] == 'Annually':
                    total_expences += row['cost']    
            
            with ui.grid(columns='1fr 1fr 1fr 1fr').classes('w-full items-center gap-0'):
                ui.label('Total').classes('border-l-2 border-b-2 p-2')
                ui.label('Annually').classes('border-l-2 border-b-2 p-2')
                ui.label('Monthly').classes('border-l-2 border-b-2 p-2')
                ui.label('Weekly').classes('border-l-2 border-b-2 p-2')
                
                ui.label('Income').classes('border-l-2 p-2')
                ui.label(f'£{round(total_income, 2)}').classes('border-l-2 p-2')
                ui.label(f'£{round(total_income / 12, 2)}').classes('border-l-2 p-2')
                ui.label(f'£{round(total_income / 52, 2)}').classes('border-l-2 p-2')
                
                ui.label('Expences').classes('border-l-2 p-2')
                ui.label(f'£{round(total_expences, 2)}').classes('border-l-2 p-2')
                ui.label(f'£{round(total_expences / 12, 2)}').classes('border-l-2 p-2')
                ui.label(f'£{round(total_expences / 52, 2)}').classes('border-l-2 p-2')
                
                ui.label('Net Worth').classes('border-l-2 p-2')
                ui.label(f'£{round(total_income - total_expences, 2)}').classes('border-l-2 p-2')
                ui.label(f'£{round((total_income - total_expences) / 12, 2)}').classes('border-l-2 p-2')
                ui.label(f'£{round((total_income - total_expences) / 52, 2)}').classes('border-l-2 p-2')

            ui.label('Category').classes('border-l-2 pl-2 text-bold')
            
            category_data = []
            for expense_category in expence_categories:
                category_cost = 0
                for expense in expences:
                    if expense['category'] == expense_category:
                        if expense['frequency'] == 'Weekly':
                            category_cost += expense['cost'] * 52
                        elif expense['frequency'] == 'Monthly':
                            category_cost += expense['cost'] * 12
                        elif expense['frequency'] == 'Annually':
                            category_cost += expense['cost']
                if category_cost != 0:
                    category_data.append({
                        'value': round(category_cost, 2),
                        'name': expense_category
                    })

            with ui.grid(columns='1fr 1fr 1fr 1fr').classes('w-full items-center gap-0'):                
                for category in category_data:
                    ui.label(f'{category["name"]}').classes('border-l-2 p-2')
                    ui.label(f'£{category["value"]}').classes('border-l-2 p-2')
                    ui.label(f'£{round(category["value"]/12, 2)}').classes('border-l-2 p-2')
                    ui.label(f'£{round(category["value"]/52, 2)}').classes('border-l-2 p-2')

        
        with ui.card().classes('w-full'):
            ui.label('Charts')
            

            category_data.append({
                'value': round(total_income - total_expences, 2),
                'name': 'Remaining'
            })

            ui.echart({
                'legend': {'top': '5%', 'left': 'center',
                    'textStyle': {
                        'color': 'gray'
                    }   
                },
                'tooltip': {'trigger': 'item'},
                'series': [{
                    'name': 'Category',
                    'type': 'pie',
                    'radius': ['40%', '70%'],
                    'avoidLabelOverlap': True,
                    'label': {'position': 'inside', 'formatter': '{d}%', 'color':'black',  'fontSize':18},
                    'percentPrecision': 0,
                    'labelLine': {'show': True},
                    'data': category_data,
                }]
            })
