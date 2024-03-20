
from app import db
from app import app

def create_tables():
    db.create_all()

if __name__ == '__main__':
    print('Hello Flask!')

    with app.app_context():
        create_tables()

    app.run(host='::', port=8080, debug=True)
    print('flask startup complete.')

