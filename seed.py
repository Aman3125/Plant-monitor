"""Put some fake sensor readings in the database so the dashboard has something to show.

Run it once with:  python seed.py
Later, the Raspberry Pi will send real readings through MQTT instead.
"""
import os
import random
from datetime import UTC, datetime, timedelta

from sqlalchemy import select

import models
from auth import hash_password
from database import Base, SessionLocal, engine

# Make the tables if they do not exist yet
Base.metadata.create_all(bind=engine)
# Same fake numbers every time the script runs
random.seed(1)

# Password for the test user. Set PLANT_PI_PASSWORD to choose your own.
PLANT_PI_PASSWORD = os.environ.get("PLANT_PI_PASSWORD", "plantpi-test-1")

with SessionLocal() as db:
    # Stop if there is already data, so readings are not added twice
    if db.execute(select(models.Reading)).first():
        print("The database already has readings. Delete readings.db to start again.")
        raise SystemExit

    # Make the plant_pi test user that owns all the fake readings
    user = db.execute(select(models.User).where(models.User.username == "plant_pi")).scalars().first()
    if not user:
        user = models.User(username="plant_pi", email="plantpi@example.com",
                           password_hash=hash_password(PLANT_PI_PASSWORD))
        db.add(user)
        db.commit()
        db.refresh(user)

    now = datetime.now(UTC)

    # 30 readings of each sensor, one every 10 minutes
    for i in range(30):
        when = now - timedelta(minutes=10 * (30 - i))
        db.add(models.Reading(sensor="temperature", content=round(random.uniform(18, 26), 1),
                              user_id=user.id, date_timestamp=when))
        db.add(models.Reading(sensor="humidity", content=round(random.uniform(45, 65), 1),
                              user_id=user.id, date_timestamp=when))
        db.add(models.Reading(sensor="light", content=round(random.uniform(40, 90), 1),
                              user_id=user.id, date_timestamp=when))

    # One hot reading as the latest, so the dashboard shows an alert
    db.add(models.Reading(sensor="temperature", content=32.5, user_id=user.id, date_timestamp=now))

    db.commit()
    print(f"Added a user (plant_pi, password: {PLANT_PI_PASSWORD}) and fake readings.")
