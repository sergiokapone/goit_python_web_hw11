from datetime import datetime
from faker import Faker
from sqlalchemy.orm import Session

from src.database.models import Contact
from src.database.connect import SessionLocal
from src.schemas import ContactBase

fake = Faker()


def create_fake_contacts(num_contacts: int):
    db: Session = SessionLocal()

    for _ in range(num_contacts):
        fake_contact = ContactBase(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            phone_number=fake.phone_number(),
            birthday=fake.date_of_birth(minimum_age=18, maximum_age=90).strftime(
                "%d.%m.%Y"
            ),
            additional_data=fake.sentence() if fake.boolean() else None,
        )

        contact_data = fake_contact.dict()
        contact = Contact(
            first_name=contact_data["first_name"],
            last_name=contact_data["last_name"],
            email=contact_data["email"],
            phone_number=contact_data["phone_number"],
            birthday=datetime.strptime(contact_data["birthday"], "%d.%m.%Y").date(),
            additional_data=contact_data["additional_data"],
        )
        db.add(contact)

    db.commit()


if __name__ == "__main__":
    create_fake_contacts(num_contacts=30)
