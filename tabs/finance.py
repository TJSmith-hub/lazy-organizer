from nicegui import ui
from tabs.database import Database

db = Database()

expence_categories = ['Bills', 'Food', 'Transport', 'Entertainment', 'Health', 'Clothing', 'Pets','Savings', 'Other']

def add_income(user_id, income):
    if income['income'].replace('.', '').isdigit():
        db.add_income(income['name'], income['frequency'], income['income'], user_id)
    finance_ui.refresh()

def delete_income(income_id):
    db.remove_income(income_id)
    finance_ui.refresh()

def add_expence(user_id, expence):
    if expence['cost'].replace('.', '').isdigit():
        db.add_expence(expence['name'], expence['category'], expence['frequency'], expence['cost'], user_id)
    finance_ui.refresh()
    
def delete_expence(expence_id):
    db.remove_expence(expence_id)
    finance_ui.refresh()
    
def get_totals(income, expences):
    total_income = 0
    total_expences = 0
    for i in income:
        if i['frequency'] == 'Monthly':
            total_income += i['income'] * 12
        elif i['frequency'] == 'Annually':
            total_income += i['income']
    for e in expences:
        if e['frequency'] == 'Weekly':
            total_expences += e['cost'] * 52
        elif e['frequency'] == 'Monthly':
            total_expences += e['cost'] * 12
        elif e['frequency'] == 'Annually':
            total_expences += e['cost']
    return total_income, total_expences
    
def get_expences_by_category(income, expences):
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
    # sort by value
    category_data = sorted(category_data, key=lambda x: x['value'], reverse=True)
    # add remaining
    total_income, total_expences = get_totals(income, expences)
    category_data.append({
        'value': round(total_income - total_expences, 2),
        'name': 'Remaining'
    })
    return category_data
    
def pi_chart(data):
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
            'data': data,
        }]
    })

# ui for the finance tab using a table of monthly expenses
@ui.refreshable
def finance_ui(app_data):
    
    if app_data['current_user']['name'] == 'Shared':
        income_rows = []
        expences_rows = []
        for user in db.get_users():
            income_rows += db.get_income(user['id'])
            expences_rows += db.get_expences(user['id'])
        total_income, total_expences = get_totals(income_rows, expences_rows)
        category_data = get_expences_by_category(income_rows, expences_rows)
    else:
        income_rows = db.get_income(app_data['current_user']['id'])
        expences_rows = db.get_expences(app_data['current_user']['id'])
        total_income, total_expences = get_totals(income_rows, expences_rows)
        category_data = get_expences_by_category(income_rows, expences_rows)
    
    with ui.grid().classes('grid md:grid-cols-2 gap-2 w-full'):
        # display income
        with ui.card().classes('w-full').style('border-radius:10px;'):
            ui.label('Income')
            with ui.grid(columns='auto 1fr 1fr auto').classes('w-full items-center gap-0'):
                ui.label('Name').classes('border-l-2 border-b-2 p-3')
                ui.label('Frequency').classes('border-l-2 border-b-2 p-3')
                ui.label('Income').classes('border-l-2 border-b-2 p-3')
                ui.label('').classes('p-2')
                
                for row in income_rows:
                    ui.label(row['name']).classes('border-l-2 p-3')
                    ui.label(row['frequency']).classes('border-l-2 p-3')
                    ui.label(row['income']).classes('border-l-2 p-3')
                    if app_data['current_user']['name'] != 'Shared':
                        ui.button(on_click=lambda row=row: delete_income(row['id']), icon='delete').props('flat fab-mini color=grey')
                    else:
                        ui.label(db.get_user(row['user_id'])['name'])
                        
                # add new income
                if app_data['current_user']['name'] != 'Shared':
                    new_income = {'name': '', 'frequency': '', 'income': ''}
                    ui.input('Name').bind_value(new_income, 'name')
                    ui.select(['Monthly', 'Annually']).bind_value(new_income, 'frequency')
                    ui.input('£', validation={'Must be a number': lambda value: value.replace('.', '').isdigit()}).bind_value(new_income, 'income')
                    ui.button(on_click=lambda new_income=new_income: add_income(app_data['current_user']['id'], new_income), icon='add').props('flat fab-mini color=grey')

        # display expences
        with ui.card().classes('w-full').style('border-radius:10px;'):
            ui.label('Expences')
            with ui.grid(columns='1fr 1fr 1fr 1fr auto').classes('w-full items-center gap-0'):
                ui.label('Name').classes('border-l-2 border-b-2 p-3')
                ui.label('Category').classes('border-l-2 border-b-2 p-3')
                ui.label('Frequency').classes('border-l-2 border-b-2 p-3')
                ui.label('Cost').classes('border-l-2 border-b-2 p-3')
                ui.label('')
                
                for row in expences_rows:
                    ui.label(row['name']).classes('border-l-2 p-3')
                    ui.label(row['category']).classes('border-l-2 p-3')
                    ui.label(row['frequency']).classes('border-l-2 p-3')
                    ui.label(row['cost']).classes('border-l-2 p-3')
                    if app_data['current_user']['name'] != 'Shared':
                        ui.button(on_click=lambda row=row: delete_expence(row['id']), icon='delete', ).props('flat fab-mini color=grey size=3')
                    else:
                        ui.label(db.get_user(row['user_id'])['name'])
                # add new expence
                if app_data['current_user']['name'] != 'Shared':
                    new_expence = {'name': '', 'category': '', 'frequency': '', 'cost': ''}
                    ui.input('Name').bind_value(new_expence, 'name')
                    ui.select(expence_categories).bind_value(new_expence, 'category')
                    ui.select(['Weekly', 'Monthly', 'Annually']).bind_value(new_expence, 'frequency')
                    ui.input('£', validation={'Must be a number': lambda value: value.replace('.', '').isdigit()}).bind_value(new_expence, 'cost')
                    ui.button(on_click=lambda: add_expence(app_data['current_user']['id'], new_expence), icon='add').props('flat fab-mini color=grey')
            
        # display stats
        with ui.card().classes('w-full').style('border-radius:10px;'):
            ui.label('Stats') 
            with ui.grid(columns='1fr 1fr 1fr 1fr').classes('w-full items-center gap-0'):
                ui.label('Total').classes('border-l-2 border-b-2 p-3')
                ui.label('Annually').classes('border-l-2 border-b-2 p-3')
                ui.label('Monthly').classes('border-l-2 border-b-2 p-3')
                ui.label('Weekly').classes('border-l-2 border-b-2 p-3')
                
                ui.label('Income').classes('border-l-2 p-3')
                ui.label(f'£{round(total_income, 2)}').classes('border-l-2 p-3')
                ui.label(f'£{round(total_income / 12, 2)}').classes('border-l-2 p-3')
                ui.label(f'£{round(total_income / 52, 2)}').classes('border-l-2 p-3')
                
                ui.label('Expences').classes('border-l-2 p-3')
                ui.label(f'£{round(total_expences, 2)}').classes('border-l-2 p-3')
                ui.label(f'£{round(total_expences / 12, 2)}').classes('border-l-2 p-3')
                ui.label(f'£{round(total_expences / 52, 2)}').classes('border-l-2 p-3')
                
                ui.label('Net Worth').classes('border-l-2 p-3')
                ui.label(f'£{round(total_income - total_expences, 2)}').classes('border-l-2 p-3')
                ui.label(f'£{round((total_income - total_expences) / 12, 2)}').classes('border-l-2 p-3')
                ui.label(f'£{round((total_income - total_expences) / 52, 2)}').classes('border-l-2 p-3')

            ui.label('Category').classes('border-l-2 pl-2 text-bold')

            with ui.grid(columns='1fr 1fr 1fr 1fr').classes('w-full items-center gap-0'):                
                for category in category_data:
                    ui.label(f'{category["name"]}').classes('border-l-2 p-3')
                    ui.label(f'£{category["value"]}').classes('border-l-2 p-3')
                    ui.label(f'£{round(category["value"]/12, 2)}').classes('border-l-2 p-3')
                    ui.label(f'£{round(category["value"]/52, 2)}').classes('border-l-2 p-3')

        
        with ui.card().classes('w-full').style('border-radius:10px;'):
            ui.label('Charts')
            
            with ui.row().classes('items-center w-full'):
                pi_chart([
                    {'value': total_expences, 'name': 'Expences'},
                    {'value': total_income - total_expences, 'name': 'Remaining'}
                ])
                pi_chart(category_data)


