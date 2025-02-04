from rahaleht import db
from flask_restful import Resource
from rahaleht.models import Expense
from flask import jsonify, request

# class Tere(Resource):
#     def get(self):

#         # yearly = yearly == 
#         # user_data = {'data': []}
#         # query = db.session.query(Expense).filter_by(user_id=user_id)

#         # if yearly:
#         #     query = query.filter(db.extract('year', Expense.date) == year)
#         # else:
#         #     query = query.filter(db.extract('year', Expense.date) == year).filter(db.extract('month', Expense.date) == month)
        
#         # for expense in query.all():
#         #     user_data['data'].append({
#         #         'category': expense.category,
#         #         'subcategory': expense.subcategory,
#         #         'money': expense.money,
#         #         'description': expense.description,
#         #         'date': expense.date.strftime('%Y-%m-%d %H:%M:%S')/<yearly>/<month>/<year>
#         #     })
        
#         return {'data': 'tere'}

# api.add_resource(Tere, '/api')

class Tere(Resource):
    def get(self):
        return {'data': 'tere'}