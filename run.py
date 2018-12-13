"""Initialize your app by declaring it"""
import os
from app import create_app
from app.db_con import Database

db=Database('main')
app = create_app(os.getenv("FLASK_CONFIG") or "default")
db.create_app_tables()
if __name__ == "__main__":
    app.run()