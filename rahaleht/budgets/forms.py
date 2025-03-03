from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, HiddenField, DecimalField, BooleanField, StringField
from wtforms.validators import DataRequired, ValidationError, Length
from rahaleht.main.utils import get_lang, default_lang
from rahaleht.expenses.forms import DateForm
from rahaleht.models import Budget
from datetime import datetime, timezone, timedelta
from flask_login import current_user


lang = current_user.language if current_user else default_lang
time = datetime.now(timezone.utc) + timedelta(hours=2)
year_number = time.year

class BudgetForm(FlaskForm):
    def __init__(self, lang):
        super(BudgetForm, self).__init__(lang)
        self.save.label.text = get_lang(lang, "edit_expense", "save")
        self.name.default = get_lang(lang, "budgets", "default_name")
        self.salary.default = 0
        self.tuition.default = 0
        self.other_incomes.default = 0
        self.rent.default = 0
        self.utilities.default = 0
        self.groceries.default = 0
        self.transport.default = 0
        self.other_living_costs.default = 0
        self.clothing.default = 0
        self.entertainment.default = 0
        self.other_personal_expenses.default = 0
        self.stocks.default = 0
        self.fonds.default = 0
        self.bonds.default = 0
        self.savings.default = 0
        self.other_investments.default = 0
        
    name = StringField('', validators=[DataRequired(), Length(2, 30)])
    default = BooleanField('')
    month = HiddenField('', validators=[DataRequired()])
    year = HiddenField('', validators=[DataRequired()])
    salary = DecimalField('')
    tuition = DecimalField('')
    other_incomes = DecimalField('')
    rent = DecimalField('')
    utilities = DecimalField('')
    groceries = DecimalField('')
    transport = DecimalField('')
    other_living_costs = DecimalField('')
    clothing = DecimalField('')
    entertainment = DecimalField('')
    other_personal_expenses = DecimalField('')
    stocks = DecimalField('')
    bonds = DecimalField('')
    fonds = DecimalField('')
    savings = DecimalField('')
    other_investments = DecimalField('')
    save = SubmitField('')

    def validate_name(self, name):
        print(name.data, get_lang(lang, "budgets", "default_name"))
        if name.data == get_lang(lang, "budgets", "default_name"):
            raise ValidationError(get_lang(lang, "errors", "This field is required."))
        


class EditBudgetForm(BudgetForm):
    def __init__(self, lang):
        super(EditBudgetForm, self).__init__(lang)
        self.delete.label.text = get_lang(lang, "edit_expense", "delete")
    delete = SubmitField("")