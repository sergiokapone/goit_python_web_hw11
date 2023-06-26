from datetime import datetime
from fastapi import APIRouter, HTTPException


from src.database.connect import SessionLocal
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
