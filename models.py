from config import db

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    first_name=db.Column(db.String(80),unique=False,nullable=False)
    last_name=db.Column(db.String(80),unique=False,nullable=False)
    username=db.Column(db.String(80),unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    password=db.Column(db.String(80),unique=False,nullable=False)

    def to_json(self):
        return{
            "id":self.id,
            "firstName":self.first_name,
            "lastName":self.last_name,
            "userName":self.username,
            "email":self.email,
            "password":self.password,
        }


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False) 
    amount = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(255), nullable=True)
    date = db.Column(db.Date, nullable=False)
    payment_method = db.Column(db.Integer, nullable=False)
    is_recurring = db.Column(db.Boolean, nullable=False)
    category = db.Column(db.String(255), nullable=False)
    frequency = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=True)

    def to_json(self):
        return {
            "id": self.id,
            "username":self.username,
            "amount": self.amount,
            "location": self.location,
            "date": self.date.strftime('%d-%m-%Y') if self.date else None,
            "payment_method": self.payment_method,
            "is_recurring": self.is_recurring,
            "category": self.category,
            "frequency": self.frequency,
            "description": self.description
        }
    
class UserSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    def to_json(self):
        return {
            "id": self.id,
            "username":self.username,
        }