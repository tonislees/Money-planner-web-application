from rahaleht import create_app, db
from rahaleht.models import Expense

app = create_app()

with app.app_context():
    db.session.query(Expense).delete()
    db.session.commit()