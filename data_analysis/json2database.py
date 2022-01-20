from pathlib import Path
from datetime import datetime, timedelta
import json
import time
import re

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from tqdm import tqdm

DATA_PATH = Path(__file__).parent.parent / "data"
JSON_DATA_PATH = DATA_PATH / "DBDaten"
DATABASE_PATH = DATA_PATH / "bahn_database2.db"

Base = declarative_base()


class DataPoint(Base):
    __tablename__ = "data"

    id = sa.Column(sa.Integer, primary_key=True)
    city = sa.Column(sa.String)
    scraping_timestamp = sa.Column(sa.Integer)
    arrival_timestamp = sa.Column(sa.Integer)  # "21:38"
    train_type = sa.Column(sa.String)  # "Bus SEV"
    train_line = sa.Column(sa.String)
    destination = sa.Column(sa.String)  # "Berlin Friedrichstraße (S)",
    platform = sa.Column(sa.String)  # "Berlin Hbf (Washingtonplatz)",
    delay_delta = sa.Column(sa.Integer)
    reason = sa.Column(sa.String)
    # TODO use many to many relationship instead of json list
    enroutestops = sa.Column(sa.String)


def string2datetime(time_string, max_hour, scraping_time):
    the_time = datetime.strptime(time_string, "%H:%M")
    the_time = datetime(
        year=scraping_time.year,
        month=scraping_time.month,
        day=scraping_time.day,
        hour=the_time.hour,
        minute=the_time.minute,
    )

    if max_hour > 12 and the_time.hour < 2:
        the_time = the_time + timedelta(days=1)

    return the_time


if __name__ == "__main__":
    engine = sa.create_engine(f"sqlite:///{DATABASE_PATH}")
    Base.metadata.create_all(engine)
    Session = sa.orm.sessionmaker(bind=engine)
    session = Session()

    all_files = [f for city_dir in JSON_DATA_PATH.iterdir() for f in city_dir.iterdir()]

    start = time.perf_counter()
    for file in tqdm(all_files):
        split_index = len(file.stem) - 15
        city = file.stem[:split_index]
        scraping_time = datetime.strptime(file.stem[split_index:], "%Y%m%d-%H%M%S")

        with open(file, encoding="utf-8") as f:
            data = json.load(f)

        max_hour = 0

        for entry in data:
            arrival_time = string2datetime(
                entry["arrival_time"], max_hour, scraping_time
            )
            max_hour = max(arrival_time.hour, max_hour)
            arrival_timestamp = arrival_time.timestamp()

            if entry["delay"] is None:
                delay_delta = 0
            else:
                delay_time = string2datetime(entry["delay"], max_hour, scraping_time)
                delay_timestamp = delay_time.timestamp()
                delay_delta = delay_timestamp - arrival_timestamp

            # assert delay_delta >= 0

            entry_orm = DataPoint(
                city=city,
                scraping_timestamp=scraping_time.timestamp(),
                arrival_timestamp=arrival_timestamp,
                train_type=entry["ID"],
                train_line=re.sub("[0-9]+", "", entry["ID"].split()[0]).lower(),
                destination=entry["destination"],
                platform=entry["platform"].split("\n")[-1],
                delay_delta=delay_delta,
                reason=entry["latest"],
                # TODO seperate time and station
                enroutestops=json.dumps(
                    [v for s in entry["enroutestops"] for v in s.split(",")],
                    ensure_ascii=False,
                ),
            )

            session.add(entry_orm)

        # commit every 60 seconds
        current = time.perf_counter()
        if current - start > 60:
            start = current
            session.commit()

    session.commit()
