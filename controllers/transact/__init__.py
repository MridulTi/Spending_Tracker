from flask import Blueprint,jsonify,request,session,redirect
from models import Transaction
from config import db
from utils.RenderResponse import RenderResponse
from constants.https_status_codes import *
from utils.ApiError import ApiError
from utils.ApiResponse import ApiResponse
from datetime import datetime
from sqlalchemy import text

transact=Blueprint("transact",__name__,url_prefix="/api/v1/transact")

@transact.route("/",methods=['GET'])
def transact_get_all():
    all_transaction=Transaction.query.all()
    if not all_transaction:
        return ApiError("Transactions not made",HTTP_400_BAD_REQUEST)
    return jsonify([{
        "id":transaction.id,
        "amount":transaction.amount,
        "location":transaction.location,
        "date":transaction.date,
        "payment_method":transaction.payment_method,
        "is_recurring":transaction.is_recurring,
        "category":transaction.category,
        "frequency":transaction.frequency,
        "description":transaction.description
        } for transaction in all_transaction]), 200

@transact.route("/all",methods=['DELETE'])
def delete_all():
    Transaction.query.delete()
    db.session.commit()
    return ApiResponse("Deleted all",HTTP_200_OK,"")

@transact.route("/create-transaction",methods=['POST'])
def create_transaction():
    data=request.json

    new_transaction=Transaction(
        amount=data['amount'],
        location=data['location'],
        date= datetime.strptime(data['date'], '%Y-%m-%d').date(),
        payment_method=data['payment_method'],
        is_recurring=data['is_recurring'],
        category=data['category'],
        frequency=data['frequency'],
        description=data['description']
    )
    if not new_transaction:
        return ApiError("Transaction not created!")
    
    db.session.add(new_transaction)
    db.session.commit()
    return ApiResponse("Transaction Created!",HTTP_200_OK,new_transaction.to_json())


@transact.route("/num_transaction",methods=['GET'])
def num_transactions():
    total_amount_spent=db.session.query(db.func.sum(Transaction.amount)).scalar() or 0
    average_transaction_amount= db.session.query(db.func.avg(Transaction.amount)).scalar() or 0
    highest_transaction_amount=db.session.query(db.func.max(Transaction.amount)).scalar() or 0
    total_transactions_per_category=db.session.query(
        Transaction.category,
        db.func.count().label('num_transactions')
    ).group_by(Transaction.category).all()

    data = {
        "total_amount_spent": total_amount_spent,
        "average_amount": average_transaction_amount,
        "highest_amount": highest_transaction_amount,
        "num_transactions_per_category": [
            {"category": row.category, "num_transactions": row.num_transactions}
            for row in total_transactions_per_category
        ]
    }

    return ApiResponse("Num transactions Calculated",HTTP_200_OK,data)