from rahaleht import db
from flask_restful import Resource
from rahaleht.models import Expense


class UserData(Resource):
    def get(self, user_id, yearly, month, year):

        yearly = yearly == 'true'
        user_data = {'data': []}
        query = db.session.query(Expense).filter_by(user_id=user_id)

        if yearly:
            newquery = query.filter(db.extract('year', Expense.date) == year)
        else:
            newquery = query.filter(db.extract('year', Expense.date) == year).filter(db.extract('month', Expense.date) == month)
        
        for expense in newquery.all():
            user_data['data'].append({
                'category': expense.category,
                'subcategory': expense.subcategory,
                'money': expense.money,
                'description': expense.description,
                'date': expense.date.strftime('%d.%m %H:%M'),
                'expense_id': expense.id
            })
        
        return user_data