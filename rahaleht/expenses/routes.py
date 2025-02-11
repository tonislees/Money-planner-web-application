from flask import render_template, Blueprint, redirect, url_for, flash, request
from rahaleht.expenses.utils import get_categories, sort_by_month
from rahaleht.expenses.forms import ExpenseForm, DateForm, EditExpenseForm
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


@expenses.route("/edit-category/category/yearly/year/month", methods=['POST', 'GET'])
@login_required
def edit_cat():
    cat, subcat = get_categories()
    category = request.args.get('category')
    yearly = request.args.get('yearly')
    year = request.args.get('year')
    month = request.args.get('month')
    return render_template('edit_cat.html', category=category,
                            yearly=yearly, year=year, month=month,  
                            categories=cat, subcategories=subcat)


@expenses.route("/edit-expense/<expense_id>", methods=['POST', 'GET'])
@login_required
def edit_expense(expense_id):
    cat, subcat = get_categories()
    form = EditExpenseForm()
    current_expense = Expense.query.get_or_404(expense_id)
    next_url = request.args.get('next')

    if form.validate_on_submit():
        if form.submit.data:
            if (form.categories.data != current_expense.category or \
               form.subcategories.data != current_expense.subcategory or \
               form.expense.data != current_expense.money or \
               form.description.data != current_expense.description):
                flash('Expense updated successfully!', 'success')
            current_expense.category = form.categories.data
            current_expense.subcategory = form.subcategories.data
            current_expense.money = form.expense.data
            current_expense.description = form.description.data
            db.session.commit()
            return redirect(next_url or url_for('expenses.overview'))
        elif form.delete.data:
            db.session.delete(current_expense)
            db.session.commit()
            flash('Expense deleted successfully!', 'success')
            return redirect(next_url or url_for('expenses.overview'))
    elif request.method == 'GET':
        form.categories.data = current_expense.category
        form.subcategories.data = current_expense.subcategory
        form.expense.data = current_expense.money
        form.description.data = current_expense.description

    return render_template('edit_expense.html', form=form, categories=cat, subcategories=subcat)