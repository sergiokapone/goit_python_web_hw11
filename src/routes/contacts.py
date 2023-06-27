from datetime import datetime, date, timedelta

from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException, Query

from src.database.connect import SessionLocal, get_db
from src.schemas import ContactCreate
from src.database.models import Contact

router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.post("/")
def create_contact(contact: ContactCreate):
    db = SessionLocal()
    new_contact = Contact(
        first_name=contact.first_name,
        last_name=contact.last_name,
        email=contact.email,
        phone_number=contact.phone_number,
        birthday=datetime.strptime(contact.birthday, "%d.%m.%Y").date(),
        additional_data=contact.additional_data,
    )
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


# Отримання списку всіх контактів
@router.get("/")
def get_all_contacts():
    db = SessionLocal()
    contacts = db.query(Contact).all()
    return contacts


# Отримання одного контакту за ідентифікатором
@router.get("/{contact_id}")
def get_contact(contact_id: int):
    db = SessionLocal()
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


# Оновлення існуючого контакту
@router.put("/{contact_id}")
def update_contact(contact_id: int, contact: ContactCreate):
    db = SessionLocal()
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db_contact.first_name = contact.first_name
    db_contact.last_name = contact.last_name
    db_contact.email = contact.email
    db_contact.phone_number = contact.phone_number
    db_contact.birthday = contact.birthday
    db_contact.additional_data = contact.additional_data
    db.commit()
    db.refresh(db_contact)
    return db_contact


# Видалення контакту
@router.delete("/{contact_id}")
def delete_contact(contact_id: int):
    db = SessionLocal()
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return {"message": "Contact deleted"}


# Пошук контакту
@router.get("/search/")
async def search_contacts(query: str = Query(...), db: Session = Depends(get_db)):
    contacts = (
        db.query(Contact)
        .filter(
            Contact.first_name.ilike(f"%{query}%")
            | Contact.last_name.ilike(f"%{query}%")
            | Contact.email.ilike(f"%{query}%")
        )
        .all()
    )
    return contacts


def is_upcoming_birthday(birthday: date, start_date: date, end_date: date) -> bool:
    birthday_this_year = start_date.replace(
        year=start_date.year, month=birthday.month, day=birthday.day
    )

    if start_date <= birthday_this_year <= end_date:
        return True

    birthday_next_year = birthday_this_year.replace(year=start_date.year + 1)

    if start_date <= birthday_next_year <= end_date:
        return True

    return False


@router.get("/birthdays/")
async def get_upcoming_birthdays(
    start_date: date = date.today(), end_date: date = date.today() + timedelta(days=7)
):
    db = SessionLocal()
    contacts = db.query(Contact).all()

    upcoming_birthdays = [
        contact
        for contact in contacts
        if is_upcoming_birthday(contact.birthday, start_date, end_date)
    ]

    return upcoming_birthdays
