from app.database.connection import SessionLocal
from app.database.services.track_service import TrackService


def test_track_service_creates_reads_lists_and_deletes_track():
    db = SessionLocal()

    try:
        service = TrackService(db)

        created_track = service.create_track(
            name="Track Service Integration Test",
            country="Test Country",
            length_km=5.900,
            number_of_corners=18,
        )

        assert created_track.track_id is not None

        fetched_track = service.get_track(created_track.track_id)

        assert fetched_track is not None
        assert fetched_track.name == "Track Service Integration Test"

        tracks = service.list_tracks()

        assert any(
            track.track_id == created_track.track_id
            for track in tracks
        )

        deleted = service.delete_track(created_track.track_id)

        assert deleted is True
        assert service.get_track(created_track.track_id) is None

    finally:
        db.rollback()
        db.close()