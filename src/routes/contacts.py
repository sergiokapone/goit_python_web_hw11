from datetime import date, datetime, timedelta
from sqlalchemy import or_, select

from sqlalchemy.ext.asyncio import AsyncSession
from src.database.connect import get_session

from fastapi import APIRouter, Depends, HTTPException, Query

from src.schemas import ContactCreate
from src.database.models import Contact

router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.post("/")
async def create_contact(
    contact: ContactCreate, session: AsyncSession = Depends(get_session)
):
    async with session.begin():
        new_contact = Contact(
            first_name=contact.first_name,
            last_name=contact.last_name,
            email=contact.email,
            phone_number=contact.phone_number,
            birthday=datetime.strptime(contact.birthday, "%d.%m.%Y").date(),
            additional_data=contact.additional_data,
        )
        session.add(new_contact)
        await session.flush()  # Сохраняем изменения в базе данных
        await session.refresh(new_contact)
        return new_contact


# Отримати всі контакти
@router.get("/")
async def get_all_contacts(session: AsyncSession = Depends(get_session)):
    async with session.begin():
        result = await session.execute(select(Contact))
        contacts = result.all()
    return contacts


@router.get("/{contact_id}")
async def get_contact(contact_id: int, session: AsyncSession = Depends(get_session)):
    contact = await session.execute(select(Contact).filter(Contact.id == contact_id))
    result = contact.scalar_one_or_none()
    if result is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return result


# Зміна контакту
@router.put("/{contact_id}")
async def update_contact(
    contact_id: int,
    contact: ContactCreate,
    session: AsyncSession = Depends(get_session),
):
    async with session.begin():
        existing_contact = await session.get(Contact, contact_id)
        if not existing_contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        existing_contact.first_name = contact.first_name
        existing_contact.last_name = contact.last_name
        existing_contact.email = contact.email
        existing_contact.phone_number = contact.phone_number
        existing_contact.birthday = datetime.strptime(
            contact.birthday, "%d.%m.%Y"
        ).date()
        existing_contact.additional_data = contact.additional_data

    await session.commit()
    await session.refresh(existing_contact)
    return existing_contact


# Видалення контакту
@router.delete("/{contact_id}")
async def delete_contact(contact_id: int, session: AsyncSession = Depends(get_session)):
    contact = await session.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    await session.delete(contact)
    await session.commit()
    return {"message": "Contact deleted", "contact": contact}


# Пошук контакту
@router.get("/search/")
async def search_contacts(
    query: str = Query(...), session: AsyncSession = Depends(get_session)
):
    contacts = (
        (
            await session.execute(
                select(Contact).filter(
                    or_(
                        Contact.first_name.ilike(f"%{query}%"),
                        Contact.last_name.ilike(f"%{query}%"),
                        Contact.email.ilike(f"%{query}%"),
                        Contact.phone_number.ilike(f"%{query}%"),
                    )
                )
            )
        )
        .scalars()
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
    end_date: date = date.today() + timedelta(days=7),
    start_date: date = date.today(),
    session: AsyncSession = Depends(get_session),
):
    async with session.begin():
        result = await session.execute(select(Contact).order_by(Contact.birthday))
        contacts = result.scalars().all()

    upcoming_birthdays = [
        contact
        for contact in contacts
        if is_upcoming_birthday(contact.birthday, start_date, end_date)
    ]

    return upcoming_birthdays
