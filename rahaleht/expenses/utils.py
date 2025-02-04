def get_categories():
    categories = ['incomes', 'living_costs', 'personal_expenses', 'investing']
    subcategories = {'incomes': ['salary', 'parents', 'grants'], 
                      'living_costs': ['food', 'rent', 'household_costs', 'clothes'], 
                      'personal_expenses': ['subscriptions', 'other'], 
                      'investing': ['stocks', 'fonds', 'savings']
                      }
    return categories, subcategories


def sort_by_month(expenses, month):
    valid_expenses = []
    for expense in expenses:
        if expense.date.month == month:
            valid_expenses.append(expense)
    return valid_expenses