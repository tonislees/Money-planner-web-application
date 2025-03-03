from rahaleht import create_app, db
from rahaleht.models import Expense, Budget

app = create_app()

def empty_budget_db():
    with app.app_context():
        db.session.query(Budget).delete()
        db.session.commit()


def reset_db():
    with app.app_context():
        db.drop_all()
        db.create_all()


reset_db()