from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField, DecimalField, BooleanField
from wtforms.validators import DataRequired, Length
from rahaleht.expenses.utils import get_categories
from rahaleht.main.utils import get_lang, default_lang
from flask_login import current_user


if current_user:
    lang = current_user.language
else:
    lang = default_lang

cat, subcategories = get_categories()


class ExpenseForm(FlaskForm):
    def __init__(self, lang):
        super(ExpenseForm, self).__init__()
        self.categories.label.text = get_lang(lang, "edit_expense", "category")
        self.categories.choices = [get_lang(lang, "incomes", "cat_name"),
                                   get_lang(lang, "living_costs", "cat_name"),
                                   get_lang(lang, "personal_expenses", "cat_name"),
                                   get_lang(lang, "investing", "cat_name")]
        self.subcategories.label.text = get_lang(lang, "edit_expense", "subcategory")
        self.subcategories.choices = [get_lang(lang, "incomes", "salary"),
                                      get_lang(lang, "incomes", "tuition"),
                                      get_lang(lang, "incomes", "other"),
                                      get_lang(lang, "living_costs", "rent"),
                                      get_lang(lang, "living_costs", "utilities"),
                                      get_lang(lang, "living_costs", "groceries"),
                                      get_lang(lang, "living_costs", "transport"),
                                      get_lang(lang, "living_costs", "other"),
                                      get_lang(lang, "personal_expenses", "clothing"),
                                      get_lang(lang, "personal_expenses", "entertainment"),
                                      get_lang(lang, "personal_expenses", "other"),
                                      get_lang(lang, "investing", "stocks"),
                                      get_lang(lang, "investing", "bonds"),
                                      get_lang(lang, "investing", "fonds"),
                                      get_lang(lang, "investing", "savings"),
                                      get_lang(lang, "investing", "other")]
        self.expense.label.text = get_lang(lang, "edit_expense", "amount")
        self.description.label.text = get_lang(lang, "edit_expense", "description")
        self.submit.label.text = get_lang(lang, "edit_expense", "save")
    categories = SelectField("")
    subcategories = SelectField("")
    expense = DecimalField("", places=2, validators=[DataRequired()])
    description = TextAreaField("", validators=[Length(min=0, max=200)])
    submit = SubmitField("")


class DateForm(FlaskForm):
    def __init__(self, lang):
        super(DateForm, self).__init__()
        self.month.choices = [('01', get_lang(lang, "months", "01")), 
                              ('02', get_lang(lang, "months", "02")), 
                              ('03', get_lang(lang, "months", "03")), 
                              ('04', get_lang(lang, "months", "04")), 
                              ('05', get_lang(lang, "months", "05")), 
                              ('06', get_lang(lang, "months", "06")), 
                              ('07', get_lang(lang, "months", "07")), 
                              ('08', get_lang(lang, "months", "08")), 
                              ('09', get_lang(lang, "months", "09")), 
                              ('10', get_lang(lang, "months", "10")), 
                              ('11', get_lang(lang, "months", "11")), 
                              ('12', get_lang(lang, "months", "12"))]

    yearly = BooleanField('')
    month = SelectField('')
    year = SelectField('', choices=[])


class EditExpenseForm(ExpenseForm):
    def __init__(self, lang):
        super(EditExpenseForm, self).__init__(lang)
        self.delete.label.text = get_lang(lang, "edit_expense", "delete")

    delete = SubmitField("")