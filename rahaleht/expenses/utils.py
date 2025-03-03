from rahaleht.main.utils import get_lang


def get_categories():
    categories = ['incomes', 'living_costs', 'personal_expenses', 'investing']
    subcategories = {
                    'incomes': ['salary', 'tuition', 'other_incomes'],
                    'living_costs': ['rent', 'utilities', 'groceries', 'transport', 'other_living_costs'],
                    'personal_expenses': ['clothing', 'entertainment', 'other_personal_expenses'],
                    'investing': ['stocks', 'bonds', 'fonds', 'savings', 'other_investments']
                    } 
    return categories, subcategories

def get_categories_names(lang):
    subcategories = {
        'incomes': [get_lang(lang, "incomes", "salary"),
                    get_lang(lang, "incomes", "tuition"),
                    get_lang(lang, "incomes", "other_incomes")],
        'living_costs': [get_lang(lang, "living_costs", "rent"),
                         get_lang(lang, "living_costs", "utilities"),
                         get_lang(lang, "living_costs", "groceries"),
                         get_lang(lang, "living_costs", "transport"),
                         get_lang(lang, "living_costs", "other_living_costs")],
        'personal_expenses': [get_lang(lang, "personal_expenses", "clothing"),
                              get_lang(lang, "personal_expenses", "entertainment"),
                              get_lang(lang, "personal_expenses", "other_personal_expenses")],
        'investing': [get_lang(lang, "investing", "stocks"),
                      get_lang(lang, "investing", "bonds"),
                      get_lang(lang, "investing", "fonds"),
                      get_lang(lang, "investing", "savings"),
                      get_lang(lang, "investing", "other_investments")]
    }
    return subcategories


def sort_by_month(expenses, month):
    valid_expenses = []
    for expense in expenses:
        if expense.date.month == month:
            valid_expenses.append(expense)
    return valid_expenses