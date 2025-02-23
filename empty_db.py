from rahaleht import create_app, db
from rahaleht.models import Expense

app = create_app()

def empty_db():
    with app.app_context():
        db.session.query(Expense).delete()
        db.session.commit()


def reset_db():
    with app.app_context():
        db.drop_all()
        db.create_all()


reset_db()