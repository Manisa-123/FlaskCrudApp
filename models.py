from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask
from manager import TodoManager
from importlib import import_module

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    objects = TodoManager()

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)


    def __repr__(self):
        return '<Task %r>' % self.id

    @property
    def Model(
            self
    ):
        """
            This property lazy loads the Model this manager is maintaining, preventing circular referencing.
        """
        if not hasattr(self, '_Model'):
            _module, _class = self.model.rsplit('.', 1)
            _module = import_module(_module)
            self._Model = getattr(_module, _class)
        return self._Model


    def create(
            self,
            **kwargs
    ):
        instance = self.Model(**kwargs)
        instance.save()
        return instance