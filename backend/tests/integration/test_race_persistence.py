from datetime import date

from app.database.connection import SessionLocal
from app.database.models.race import RaceModel
from app.database.models.track import TrackModel


def test_race_can_be_inserted_and_read_back() -> None:
    session = SessionLocal()

    try:
        track = TrackModel(
            name="Silverstone",
            country="United Kingdom",
            length_km=5.891,
            number_of_corners=18,
        )

        session.add(track)
        session.commit()
        session.refresh(track)

        race = RaceModel(
            name="British Grand Prix",
            season=2026,
            round_number=12,
            track_id=track.track_id,
            race_date=date(2026, 7, 5),
        )

        session.add(race)
        session.commit()
        session.refresh(race)

        assert race.race_id is not None

        saved_race = session.get(RaceModel, race.race_id)

        assert saved_race is not None
        assert saved_race.name == "British Grand Prix"
        assert saved_race.season == 2026
        assert saved_race.round_number == 12
        assert saved_race.track_id == track.track_id
        assert saved_race.race_date == date(2026, 7, 5)

        assert saved_race.track is not None
        assert saved_race.track.name == "Silverstone"

        saved_track = session.get(TrackModel, track.track_id)

        assert saved_track is not None
        assert len(saved_track.races) == 1
        assert saved_track.races[0].race_id == race.race_id

        session.delete(race)
        session.delete(track)
        session.commit()

    finally:
        session.close()