from rahaleht.main.utils import get_lang, default_lang
from flask_login import current_user


if current_user:
    lang = current_user.language
else:
    lang = default_lang


def get_categories():
    categories = [get_lang(lang, "incomes", "cat_name"), 
                  get_lang(lang, "living_costs", "cat_name"), 
                  get_lang(lang, "personal_expenses", "cat_name"), 
                  get_lang(lang, "investing", "cat_name")]
    subcategories = {categories[0]: [get_lang(lang, "incomes", "salary"),
                                 get_lang(lang, "incomes", "tuition"),
                                 get_lang(lang, "incomes", "other")], 
                     categories[1]: [get_lang(lang, "living_costs", "rent"),
                                      get_lang(lang, "living_costs", "utilities"),
                                      get_lang(lang, "living_costs", "groceries"),
                                      get_lang(lang, "living_costs", "transport"),
                                      get_lang(lang, "living_costs", "other")], 
                     categories[2]: [get_lang(lang, "personal_expenses", "clothing"),
                                           get_lang(lang, "personal_expenses", "entertainment"),
                                           get_lang(lang, "personal_expenses", "other")], 
                     categories[3]: [get_lang(lang, "investing", "stocks"),
                                   get_lang(lang, "investing", "bonds"),
                                   get_lang(lang, "investing", "fonds"), 
                                   get_lang(lang, "investing", "savings"),
                                   get_lang(lang, "investing", "other")]
                  }
    return categories, subcategories


def sort_by_month(expenses, month):
    valid_expenses = []
    for expense in expenses:
        if expense.date.month == month:
            valid_expenses.append(expense)
    return valid_expenses