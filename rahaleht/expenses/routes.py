from flask import render_template, Blueprint, redirect, url_for, flash, request
from rahaleht.expenses.utils import get_categories, get_categories_names
from rahaleht.expenses.forms import ExpenseForm, DateForm, EditExpenseForm
from rahaleht.models import Expense, Budget
from rahaleht import db
from flask_login import current_user, login_required
from rahaleht.main.utils import get_lang
from datetime import datetime, timezone, timedelta


expenses = Blueprint('expenses', __name__)

@expenses.route("/")
@expenses.route("/overview", methods=['POST', 'GET'])
@login_required
def overview():
    form = DateForm(current_user.language)
    cat, subcat = get_categories()
    now = datetime.now(timezone.utc) + timedelta(hours=2)
    if current_user.last_login.month != now.month or current_user.last_login.year != now.year:
        default_budget = Budget.query.filter_by(default='1').first()
        if default_budget:
            new_budget = Budget(
                name=get_lang(current_user.language, "budget_names", str(now.month)),
                user_id=current_user.id,
                month=now.month,
                year=now.year,
                default=0,
                salary=default_budget.salary,
                tuition=default_budget.tuition,
                other_incomes=default_budget.other_incomes,
                rent=default_budget.rent,
                utilities=default_budget.utilities,
                groceries=default_budget.groceries,
                transport=default_budget.transport,
                other_living_costs=default_budget.other_living_costs,
                clothing=default_budget.clothing,
                entertainment=default_budget.entertainment,
                other_personal_expenses=default_budget.other_personal_expenses,
                stocks=default_budget.stocks,
                bonds=default_budget.bonds,
                fonds=default_budget.fonds,
                savings=default_budget.savings,
                other_investments=default_budget.other_investments
            )
            db.session.add(new_budget)
            db.session.commit()
    current_user.last_login = now
    db.session.commit()
    return render_template('overview.html', form=form, categories=cat, 
                           subcategories=subcat, get_lang=get_lang, lang=current_user.language)


@expenses.route("/new-expense", methods=['POST', 'GET'])
@login_required
def new_expense():
    cat, subcat = get_categories()
    subcat_names = get_categories_names(current_user.language)
    form = ExpenseForm(current_user.language)
    if form.validate_on_submit():
        if not form.description.data:
            form.description.data = get_lang(current_user.language, form.categories.data, form.subcategories.data)
        form_date = datetime(year=int(form.year.data), month=int(form.month.data), day=form.day.data.day, hour=form.time.data.hour, minute=form.time.data.minute)
        new_exp = Expense(category=form.categories.data, 
                          subcategory=form.subcategories.data, 
                          money=form.expense.data, 
                          date=form_date,
                          description=form.description.data, 
                          owner=current_user)
        db.session.add(new_exp)
        db.session.commit()
        return redirect(url_for('expenses.overview'))
    elif request.method == 'GET':
        time = datetime.now(timezone.utc) + timedelta(hours=2)
        form.time.data = time
        form.day.data = time
    return render_template('new_expense.html', form=form, categories=cat, subcategories=subcat,
                           subcategories_names=subcat_names, 
                           get_lang=get_lang, lang=current_user.language)


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
                            categories=cat, subcategories=subcat, 
                            get_lang=get_lang, lang=current_user.language)


@expenses.route("/edit-expense/<expense_id>", methods=['POST', 'GET'])
@login_required
def edit_expense(expense_id):
    cat, subcat = get_categories()
    subcat_names = get_categories_names(current_user.language)
    form = EditExpenseForm(current_user.language)
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
    if form.delete.data:
        db.session.delete(current_expense)
        db.session.commit()
        flash(get_lang(current_user.language, "edit_expense", "delete_succesful"), 'success')
        return redirect(next_url or url_for('expenses.overview'))
    elif request.method == 'GET':
        form.categories.data = current_expense.category
        form.subcategories.data = current_expense.subcategory
        form.expense.data = current_expense.money
        form.description.data = current_expense.description
        form.day.data = current_expense.date
        form.time.data = current_expense.date

    return render_template('edit_expense.html', form=form, categories=cat, subcategories=subcat,
                           subcategories_names=subcat_names, 
                           get_lang=get_lang, lang=current_user.language)