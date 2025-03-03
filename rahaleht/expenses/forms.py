from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField, DecimalField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, Length
from rahaleht.main.utils import get_lang
from datetime import datetime, timezone, timedelta


time = datetime.now(timezone.utc) + timedelta(hours=2)
year_number = time.year

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
    year = SelectField('', choices=[str(year_number - i) for i in range(10)])


class ExpenseForm(DateForm):
    def __init__(self, lang):
        super(ExpenseForm, self).__init__(lang)
        self.categories.label.text = get_lang(lang, "edit_expense", "category")
        self.categories.choices = [('incomes', get_lang(lang, "incomes", "cat_name")),
                                   ('living_costs', get_lang(lang, "living_costs", "cat_name")),
                                   ('personal_expenses', get_lang(lang, "personal_expenses", "cat_name")),
                                   ('investing', get_lang(lang, "investing", "cat_name"))]
        self.subcategories.label.text = get_lang(lang, "edit_expense", "subcategory")
        self.subcategories.choices = [('salary', get_lang(lang, "incomes", "salary")),
                                      ('tuition', get_lang(lang, "incomes", "tuition")),
                                      ('other_icnomes', get_lang(lang, "incomes", "other")),
                                      ('rent', get_lang(lang, "living_costs", "rent")),
                                      ('utilities', get_lang(lang, "living_costs", "utilities")),
                                      ('groceries', get_lang(lang, "living_costs", "groceries")),
                                      ('transport', get_lang(lang, "living_costs", "transport")),
                                      ('other_living_costs', get_lang(lang, "living_costs", "other")),
                                      ('clothing', get_lang(lang, "personal_expenses", "clothing")),
                                      ('entertainment', get_lang(lang, "personal_expenses", "entertainment")),
                                      ('other_personal_expenses', get_lang(lang, "personal_expenses", "other")),
                                      ('stocks', get_lang(lang, "investing", "stocks")),
                                      ('bonds', get_lang(lang, "investing", "bonds")),
                                      ('fonds', get_lang(lang, "investing", "fonds")),
                                      ('savings', get_lang(lang, "investing", "savings")),
                                      ('other_investments', get_lang(lang, "investing", "other"))]
        self.expense.label.text = get_lang(lang, "edit_expense", "amount")
        self.description.label.text = get_lang(lang, "edit_expense", "description")
        self.submit.label.text = get_lang(lang, "edit_expense", "save")
        self.time.label.text = get_lang(lang, "edit_expense", "date")
    categories = SelectField("")
    subcategories = SelectField("")
    day = DateTimeField("", format='%d')
    time = DateTimeField("", format='%H:%M')
    expense = DecimalField("", places=2, validators=[DataRequired()])
    description = TextAreaField("", validators=[Length(min=0, max=200)])
    submit = SubmitField("")


class EditExpenseForm(ExpenseForm):
    def __init__(self, lang):
        super(EditExpenseForm, self).__init__(lang)
        self.delete.label.text = get_lang(lang, "edit_expense", "delete")

    delete = SubmitField("")