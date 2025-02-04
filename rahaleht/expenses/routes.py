from flask import render_template, Blueprint, redirect, url_for
from rahaleht.expenses.utils import get_categories, sort_by_month
from rahaleht.expenses.forms import ExpenseForm, DateForm
from rahaleht.models import Expense
from rahaleht import db
from flask_login import current_user, login_required


expenses = Blueprint('expenses', __name__)


@expenses.route("/overview", methods=['POST', 'GET'])
@login_required
def overview():
    form = DateForm()
    cat, subcat = get_categories()

    return render_template('overview.html', form=form, categories=cat, subcategories=subcat)


@expenses.route("/new-expense", methods=['POST', 'GET'])
@login_required
def new_expense():
    cat, subcat = get_categories()
    form = ExpenseForm()
    if form.validate_on_submit():
        new_exp = Expense(category=form.categories.data, 
                          subcategory=form.subcategories.data, 
                          money=form.expense.data, 
                          description=form.description.data, 
                          owner=current_user)
        db.session.add(new_exp)
        db.session.commit()
        return redirect(url_for('expenses.overview'))
    return render_template('new_expense.html', form=form, categories=cat, subcategories=subcat)