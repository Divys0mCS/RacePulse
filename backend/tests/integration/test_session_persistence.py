from datetime import date

from app.database.connection import SessionLocal
from app.database.models.race import RaceModel
from app.database.models.session import SessionModel
from app.database.models.track import TrackModel


def test_session_can_be_inserted_and_read_back() -> None:
    session = SessionLocal()

    try:
        track = TrackModel(
            name="Spa-Francorchamps",
            country="Belgium",
            length_km=7.004,
            number_of_corners=19,
        )

        session.add(track)
        session.commit()
        session.refresh(track)

        race = RaceModel(
            name="Belgian Grand Prix",
            season=2026,
            round_number=13,
            track_id=track.track_id,
            race_date=date(2026, 7, 19),
        )

        session.add(race)
        session.commit()
        session.refresh(race)

        fp1 = SessionModel(
            race_id=race.race_id,
            session_type="FP1",
        )

        session.add(fp1)
        session.commit()
        session.refresh(fp1)

        assert fp1.session_id is not None

        saved_session = session.get(SessionModel, fp1.session_id)

        assert saved_session is not None
        assert saved_session.race_id == race.race_id
        assert saved_session.session_type == "FP1"

        assert saved_session.race is not None
        assert saved_session.race.name == "Belgian Grand Prix"

        saved_race = session.get(RaceModel, race.race_id)

        assert saved_race is not None
        assert len(saved_race.sessions) == 1
        assert saved_race.sessions[0].session_type == "FP1"

        session.delete(fp1)
        session.delete(race)
        session.delete(track)
        session.commit()

    finally:
        session.close()