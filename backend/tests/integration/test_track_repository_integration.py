from app.database.connection import SessionLocal
from app.database.models.track import TrackModel
from app.database.repositories.track_repository import TrackRepository


def test_track_repository_persists_track():
    db = SessionLocal()
    
    try:
        repository = TrackRepository(db)

        track = TrackModel(
            name="Integration Test Track",
            country="Test Country",
            length_km=5.000,
            number_of_corners=10,
        )

        # CREATE
        created_track = repository.create(track)
        db.commit()

        assert created_track.track_id is not None

        # GET BY ID
        fetched_track = repository.get_by_id(created_track.track_id)

        assert fetched_track is not None
        assert fetched_track.track_id == created_track.track_id
        assert fetched_track.name == "Integration Test Track"
        assert fetched_track.country == "Test Country"
        assert fetched_track.length_km == 5.000
        assert fetched_track.number_of_corners == 10

        # LIST ALL
        # Use limit=500 to ensure we capture the newly created track
        # (database may have many tracks from previous test runs)
        tracks = list(repository.list_all(limit=500))

        assert any(
            existing.track_id == created_track.track_id
            for existing in tracks
        )

        # DELETE
        repository.delete(fetched_track)
        db.commit()

        assert repository.get_by_id(created_track.track_id) is None

    finally:
        db.close()