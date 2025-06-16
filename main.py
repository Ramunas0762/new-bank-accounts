from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Account(BaseModel):
    id: int
    type: str
    person_name:str
    person_address: str

def write_account_to_file(account: "Account"):
        with open("account.txt", "a") as file:
            file.write(f"{account.id}, {account.type}, {account.person_name}, {account.person_address}\n")

def read_accounts_from_file():
    accounts = []
    with open("account.txt", "r") as file:
            for line in file:
                id, type, person_name, person_address = line.strip().split(", ")
                accounts.append(Account(id=int(id), type=type, person_name=person_name, person_address=person_address))
    
    return accounts

def delete_account_from_file(account_id_to_delete: int):
    accounts = read_accounts_from_file()
    accounts = [account for account in accounts if account.id != account_id_to_delete]
    
    with open("account.txt", "w") as file:
        for account in accounts:
            file.write(f"{account.id}, {account.type}, {account.person_name}, {account.person_address}\n")


import os
if not os.path.exists("account.txt"):
     open("account.txt", "w").close()


accounts:list[Account] = read_accounts_from_file()

@app.post("/accounts/")
def create_account(account: Account):
    accounts.append(account)
    write_account_to_file(account)
    return {"message": "Account created successfully"}

@app.get("/accounts/")
def get_accounts():
    return accounts

@app.get("/accounts/{account_id}")
def get_account(account_id: int):
    for account in accounts:
        if account.id == account_id:
            return account
    return {"message": "Account not found"}


@app.delete("/accounts/{account_id}")
def delete_account(account_id: int):
    accounts[:] = [account for account in accounts if account.id != account_id]
    delete_account_from_file(account_id)
    return {"message": "Account deleted successfully"}