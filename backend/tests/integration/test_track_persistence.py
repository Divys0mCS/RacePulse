from app.database.connection import SessionLocal
from app.database.models.track import TrackModel


def test_track_can_be_inserted_and_read_back() -> None:
    with SessionLocal() as session:
        track = TrackModel(
            name="RacePulse Test Circuit",
            country="Testland",
            length_km=5.0,
            number_of_corners=12,
        )

        session.add(track)
        session.commit()

        assert track.track_id is not None

        saved_track = session.get(TrackModel, track.track_id)

        assert saved_track is not None
        assert saved_track.name == "RacePulse Test Circuit"
        assert saved_track.country == "Testland"
        assert saved_track.length_km == 5.0
        assert saved_track.number_of_corners == 12

        session.delete(saved_track)
        session.commit()