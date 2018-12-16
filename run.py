"""Initialize your app by declaring it"""
import os
from app import create_app
from app.db_con import Database


app = create_app(os.getenv("FLASK_CONFIG") or "default")
with app.app_context():
        db = Database()
        db.init_db(app)
        db.create_app_tables()
if __name__ == "__main__":
    app.run()