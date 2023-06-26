from fastapi import Depends, FastAPI
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.database.connect import get_db


from src.routes import contacts

app = FastAPI()

app.include_router(contacts.router)

# Кореневий маршрут
@app.get("/", tags=["Root"])
def root():
    return {"message": "Hello World"}


@app.get("/api/healthchecker", tags=["Root"])
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        print(result)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database is not configured correctly",
            )
        return {"message": "You successfully connect to database!"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error connecting to the database",
        )
