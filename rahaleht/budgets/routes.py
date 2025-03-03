from flask import render_template, Blueprint, redirect, url_for, flash, request
from rahaleht.expenses.utils import get_categories
from rahaleht.budgets.forms import BudgetForm, EditBudgetForm
from rahaleht.expenses.forms import DateForm
from rahaleht.models import Budget
from rahaleht import db
from flask_login import current_user, login_required
from rahaleht.main.utils import get_lang
from datetime import datetime, timezone, timedelta

budgets = Blueprint('budgets', __name__)


@budgets.route("/budgets", methods=['POST', 'GET'])
@login_required
def budgets_overview():
    form = DateForm(current_user.language)
    return render_template('budgets.html', 
                           get_lang=get_lang, 
                           lang=current_user.language,
                           form=form, current_user=current_user)


@budgets.route("/new-budget/<year>/<month>", methods=['POST', 'GET'])
@login_required
def new_budget(year, month):
    form = BudgetForm(current_user.language)
    form.process(request.form)
    cat, subcat = get_categories()
    if request.method == 'GET':
        form.year.data = year
        form.month.data = int(month)
    if form.validate_on_submit():
        incomes = [form.salary.data, form.tuition.data, form.other_incomes.data]
        expenses = [form.rent.data, form.utilities.data, form.groceries.data, form.transport.data, 
                    form.other_living_costs.data, form.clothing.data, form.entertainment.data, 
                    form.other_personal_expenses.data, form.stocks.data, form.bonds.data, form.fonds.data, 
                    form.savings.data, form.other_investments.data]
        if form.default.data == 1:
            previous_default = Budget.query.filter_by(default=1).first()
            if previous_default:
                previous_default.default = 0
                db.session.commit()
        if sum(float(i or 0) for i in incomes) != sum(float(e or 0) for e in expenses):
            flash(get_lang(current_user.language, "errors", "budget_balance"), 'danger')
            return render_template('new_budget.html', get_lang=get_lang, form=form, 
                           lang=current_user.language, categories=cat, subcategories=subcat)
        elif sum(float(i or 0) for i in incomes) == 0:
            flash(get_lang(current_user.language, "errors", "budget_zero"), 'danger')
            return render_template('new_budget.html', get_lang=get_lang, form=form, 
                           lang=current_user.language, categories=cat, subcategories=subcat)
        else:
            budget = Budget(name=form.name.data, 
                            user_id=current_user.id,
                            month=form.month.data,
                            year=form.year.data, 
                            default=form.default.data, 
                            salary=form.salary.data, 
                            tuition=form.tuition.data, 
                            other_incomes=form.other_incomes.data, 
                            rent=form.rent.data, 
                            utilities=form.utilities.data, 
                            groceries=form.groceries.data, 
                            transport=form.transport.data, 
                            other_living_costs=form.other_living_costs.data, 
                            clothing=form.clothing.data, 
                            entertainment=form.entertainment.data, 
                            other_personal_expenses=form.other_personal_expenses.data, 
                            stocks=form.stocks.data, 
                            bonds=form.bonds.data, 
                            fonds=form.fonds.data, 
                            savings=form.savings.data, 
                            other_investments=form.other_investments.data)
            db.session.add(budget)
            db.session.commit()
            flash(get_lang(current_user.language, "budgets", "budget_created"), 'success')
            return redirect(url_for('budgets.budgets_overview'))
    return render_template('new_budget.html', get_lang=get_lang, form=form, 
                           lang=current_user.language, categories=cat, subcategories=subcat)

@budgets.route("/edit-budget/<budget_id>", methods=['POST', 'GET'])
@login_required
def edit_budget(budget_id):
    cat, subcat = get_categories()
    budget = Budget.query.filter_by(id=budget_id, user_id=current_user.id).first()
    form = EditBudgetForm(current_user.language)
    form.process(request.form)
    cat, subcat = get_categories()
    if request.method == 'GET':
        form.name.data = budget.name
        form.year.data = budget.year
        form.month.data = budget.month
        form.default.data = budget.default
        form.salary.data = budget.salary
        form.tuition.data = budget.tuition
        form.other_incomes.data = budget.other_incomes
        form.rent.data = budget.rent
        form.utilities.data = budget.utilities
        form.groceries.data = budget.groceries
        form.transport.data = budget.transport
        form.other_living_costs.data = budget.other_living_costs
        form.clothing.data = budget.clothing
        form.entertainment.data = budget.entertainment
        form.other_personal_expenses.data = budget.other_personal_expenses
        form.stocks.data = budget.stocks
        form.fonds.data = budget.fonds
        form.bonds.data = budget.bonds
        form.savings.data = budget.savings
        form.other_investments.data = budget.other_investments
    if form.delete.data:
        print("siin")
        db.session.delete(budget)
        db.session.commit()
        flash(get_lang(current_user.language, "budget", "budget_deleted"))
        return redirect(url_for('budgets.budgets_overview')) 
    elif form.validate_on_submit():
        incomes = [form.salary.data, form.tuition.data, form.other_incomes.data]
        expenses = [form.rent.data, form.utilities.data, form.groceries.data, form.transport.data, 
                    form.other_living_costs.data, form.clothing.data, form.entertainment.data, 
                    form.other_personal_expenses.data, form.stocks.data, form.bonds.data, form.fonds.data, 
                    form.savings.data, form.other_investments.data]
        if form.default.data == 1:
            previous_default = Budget.query.filter_by(default=1).first()
            if previous_default:
                previous_default.default = 0
                db.session.commit()
        if sum(float(i or 0) for i in incomes) != sum(float(e or 0) for e in expenses):
            flash(get_lang(current_user.language, "errors", "budget_balance"), 'danger')
            return render_template('new_budget.html', get_lang=get_lang, form=form, 
                           lang=current_user.language, categories=cat, subcategories=subcat)
        elif sum(float(i or 0) for i in incomes) == 0:
            flash(get_lang(current_user.language, "errors", "budget_zero"), 'danger')
            return render_template('new_budget.html', get_lang=get_lang, form=form, 
                           lang=current_user.language, categories=cat, subcategories=subcat)
        else:
            budget.name = form.name.data
            budget.default = form.default.data
            budget.salary = form.salary.data
            budget.tuition = form.tuition.data
            budget.other_incomes = form.other_incomes.data
            budget.rent = form.rent.data
            budget.utilities = form.utilities.data
            budget.groceries = form.groceries.data
            budget.transport = form.transport.data
            budget.other_living_costs = form.other_living_costs.data
            budget.clothing = form.clothing.data
            budget.entertainment = form.entertainment.data
            budget.other_personal_expenses = form.other_personal_expenses.data
            budget.stocks = form.stocks.data
            budget.bonds = form.bonds.data
            budget.fonds = form.fonds.data
            budget.savings = form.savings.data
            budget.other_investments = form.other_investments.data
            db.session.commit()
            flash(get_lang(current_user.language, "budgets", "budget_updated"), 'success')
            return redirect(url_for('budgets.budgets_overview'))

    return render_template('edit_budget.html', get_lang=get_lang, form=form, 
                           lang=current_user.language, categories=cat, subcategories=subcat)