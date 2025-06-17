from fastapi import FastAPI
from pydantic import BaseModel
import os
from datetime import date
from typing import Literal

app = FastAPI()

class BankAccount(BaseModel):
    id: int
    type: Literal["business", "personal"]
    person_name:str
    person_address: str

def write_account_to_file(account: "BankAccount"):
        with open("accounts_data.txt", "a") as file:
            file.write(f"{account.id}, {account.type}, {account.person_name}, {account.person_address}\n")

def read_accounts_from_file():
    accounts = []
    with open("accounts_data.txt", "r") as file:
            for line in file:
                id, type, person_name, person_address = line.strip().split(", ")
                accounts.append(BankAccount(id=int(id), type=type, person_name=person_name, person_address=person_address))
    
    return accounts

def delete_account_from_file(account_id_to_delete: int):
    accounts = read_accounts_from_file()
    accounts = [account for account in accounts if account.id != account_id_to_delete]
    
    with open("accounts_data.txt", "w") as file:
        for account in accounts:
            file.write(f"{account.id}, {account.type}, {account.person_name}, {account.person_address}\n")



if not os.path.exists("accounts_data.txt"):
     open("accounts_data.txt", "w").close()


accounts:list[BankAccount] = read_accounts_from_file()

bank_accounts:list[BankAccount] = []

@app.post("/bank-accounts/")
def create_bank_account(account: BankAccount):
    bank_accounts.append(account)
    write_account_to_file(account)
    return {"message": "Bank account created successfully"}

@app.get("/bank-accounts/")
def get_bank_accounts():
    return bank_accounts

@app.get("/bank-accounts/{account_id}")
def get_account(account_id: int):
    for account in bank_accounts:
        if account.id == account_id:
            return account
    return {"message": "Such Bank account not found"}


@app.delete("/bank-accounts/{account_id}")
def delete_bank_account(account_id: int):
    bank_accounts[:] = [account for account in bank_accounts if account.id != account_id]
    return {"message": "Bank account deleted successfully"}


class PaymentResource(BaseModel):
    id: int
    from_account_id: int
    to_account_id: int
    amount: float
    payment_date: date


def write_payment_to_file(payment: PaymentResource):
        with open("payments_data.txt", "a") as file:
            file.write(f"{payment.id}, {payment.from_account_id}, {payment.to_account_id}, {payment.amount}, {payment.payment_date}\n")

def read_payments_from_file():
    payments = []
    with open("payments_data.txt", "r") as file:
            for line in file:
                id, type, person_name, person_address = line.strip().split(", ")
                payments.append(PaymentResource(id=int(id), type=type, person_name=person_name, person_address=person_address))
    
    return payments

def delete_payments_from_file(payment_id_to_delete: int):
    payments = read_payments_from_file()
    payments = [payment for payment in payments if payment.id != payment_id_to_delete]
    
    with open("payments_data.txt", "w") as file:
        for payment in payments:
            file.write(f"{payment.id}, {payment.from_account_id}, {payment.to_account_id}, {payment.amount}, {payment.payment_date}\n")


if not os.path.exists("payments_data.txt"):
     open("payments_data.txt", "w").close()


payment_recources:list[PaymentResource] = []

@app.post("/payment-recources/")
def create_payment_resource(payment: PaymentResource):
    payment_recources.append(payment)
    write_payment_to_file(payment)
    return {"message": "Payment resource created successfully"}
   

@app.get("/payment-recources/")
def get_payment_resources():
    return payment_recources

@app.get("/payment-recources/{recourse_id}")
def get_payment_resource(recourse_id: int):
    """Retrieve a payment resource by its ID."""
    for recourse in payment_recources:
        if recourse.id == recourse_id:
            return recourse
    return {"message": "Payment resource not found"}


@app.delete("/payment-recources/{recourse_id}")
def delete_payment_resource(recourse_id: int):
    """Delete a payment resource by its ID."""
    payment_recources[:] = [recourse for recourse in payment_recources if recourse.id != recourse_id]
    delete_payments_from_file(recourse_id)
    return {"message": "Payment resource deleted successfully"}