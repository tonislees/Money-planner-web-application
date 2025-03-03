from rahaleht import db
from flask_restful import Resource
from rahaleht.models import Budget


class BudgetData(Resource):
    def get(self, user_id, month, year):

        budget_data = {'data': []}
        budget = Budget.query.filter_by(user_id=user_id, year=year, month=month).first()
        
        if budget:
            budget_data['data'].append({
                'incomes': budget.salary + budget.tuition + budget.other_incomes,
                'living_costs': budget.rent + budget.utilities + budget.groceries + budget.transport + budget.other_living_costs,
                'personal_expenses': budget.clothing + budget.entertainment + budget.other_personal_expenses,
                'investing': budget.stocks + budget.fonds + budget.bonds + budget.savings + budget.other_investments,
                'salary': budget.salary,
                'tuition': budget.tuition,
                'other_incomes': budget.other_incomes,
                'rent': budget.rent,
                'utilities': budget.utilities,
                'groceries': budget.groceries,
                'transport': budget.transport,
                'other_living_costs': budget.other_living_costs,
                'clothing': budget.clothing,
                'entertainment': budget.entertainment,
                'other_personal_expenses': budget.other_personal_expenses,
                'stocks': budget.stocks,
                'fonds': budget.fonds,
                'bonds': budget.bonds,
                'savings': budget.savings,
                'other_investments': budget.other_investments,
                'is_default': budget.default,
                'name': budget.name,
                'id': budget.id
            })
        
        return budget_data