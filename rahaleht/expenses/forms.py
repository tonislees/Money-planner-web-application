from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField, DecimalField, BooleanField
from wtforms.validators import DataRequired, Length
from rahaleht.expenses.utils import get_categories


class ExpenseForm(FlaskForm):
    cat, catsub = get_categories()
    categories = SelectField('Category', choices=[(cat[0], 'Incomes'), (cat[1], 'Living costs'), (cat[2], 'Personal Expenses'), (cat[3], 'Investing')])
    subcategories = SelectField('Subcategory', choices=['salary', 'parents', 'grants', 'food', 'rent', 'household_costs', 'clothes', 'subscriptions', 'other', 'stocks', 'fonds', 'savings'])
    expense = DecimalField('Expense', places=2, validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(min=0, max=200)])
    submit = SubmitField('Save')


class DateForm(FlaskForm):
    yearly = BooleanField('')
    month = SelectField('', choices=[('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'), ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'), ('09', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')])
    year = SelectField('', choices=[])


class EditExpenseForm(FlaskForm):
    cat, catsub = get_categories()
    categories = SelectField('Category', choices=[(cat[0], 'Incomes'), (cat[1], 'Living costs'), (cat[2], 'Personal Expenses'), (cat[3], 'Investing')])
    subcategories = SelectField('Subcategory', choices=['salary', 'parents', 'grants', 'food', 'rent', 'household_costs', 'clothes', 'subscriptions', 'other', 'stocks', 'fonds', 'savings'])
    expense = DecimalField('Expense', places=2, validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(min=0, max=60)])
    
    submit = SubmitField('Save')
    delete = SubmitField('Delete')