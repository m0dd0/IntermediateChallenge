from pathlib import Path
from datetime import datetime, timedelta
import json

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from tqdm import tqdm

DATA_PATH = Path(__file__).parent.parent / "data"
JSON_DATA_PATH = DATA_PATH / "DBDaten"
DATABASE_PATH = DATA_PATH / "bahn_database.db"

Base = declarative_base()


class DataPoint(Base):
    __tablename__ = "data"

    id = sa.Column(sa.Integer, primary_key=True)
    city = sa.Column(sa.String)
    scraping_timestamp = sa.Column(sa.Integer)
    arrival_timestamp = sa.Column(sa.Integer)  # "21:38"
    train_type = sa.Column(sa.String)  # "Bus SEV"
    destination = sa.Column(sa.String)  # "Berlin Friedrichstraße (S)",
    platform = sa.Column(sa.String)  # "Berlin Hbf (Washingtonplatz)",
    delay_delta = sa.Column(sa.Integer)
    reason = sa.Column(sa.String)
    # TODO use may to many relationship instead of json list
    enroutestops = sa.Column(sa.String)


if __name__ == "__main__":
    engine = sa.create_engine(f"sqlite:///{DATABASE_PATH}")
    Base.metadata.create_all(engine)
    Session = sa.orm.sessionmaker(bind=engine)
    session = Session()

    all_files = [f for city_dir in JSON_DATA_PATH.iterdir() for f in city_dir.iterdir()]

    for file in tqdm(all_files):
        split_index = len(file.stem) - 15
        city = file.stem[:split_index]
        scraping_time = datetime.strptime(file.stem[split_index:], "%Y%m%d-%H%M%S")

        with open(file) as f:
            data = json.load(f)

        max_hour = 0

        for entry in data:
            arrival_time = datetime.strptime(entry["arrival_time"], "%H:%M")
            arrival_time = datetime(
                year=scraping_time.year,
                month=scraping_time.month,
                day=scraping_time.day,
                hour=arrival_time.hour,
                minute=arrival_time.minute,
            )

            max_hour = max(arrival_time.hour, max_hour)
            if max_hour > 12 and arrival_time.hour < 2:
                arrival_time = arrival_time + timedelta(days=1)

            arrival_timestamp = arrival_time.timestamp()

            if entry["delay"] is None:
                delay_delta = 0
            else:
                delay_time = datetime.strptime(entry["delay"], "%H:%M")
                delay_time = datetime(
                    year=scraping_time.year,
                    month=scraping_time.month,
                    day=scraping_time.day,
                    hour=delay_time.hour,
                    minute=delay_time.minute,
                )
                delay_timestamp = delay_time.timestamp()
                delay_delta = delay_timestamp - arrival_timestamp

            entry_orm = DataPoint(
                city=city,
                scraping_timestamp=scraping_time.timestamp(),
                arrival_timestamp=arrival_timestamp,
                train_type=entry["ID"],
                destination=entry["destination"],
                platform=entry["platform"],
                delay_delta=delay_delta,
                reason=entry["latest"],
                enroutestops=json.dumps(
                    [v for s in entry["enroutestops"] for v in s.split(",")]
                ),
            )

            session.add(entry_orm)
        session.commit()
