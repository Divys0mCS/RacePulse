from app.database.connection import SessionLocal
from app.database.models.team import TeamModel
from app.database.repositories.team_repository import TeamRepository


def test_team_repository_persists_team():
    db = SessionLocal()

    try:
        repository = TeamRepository(db)

        team = TeamModel(
            name="Integration Test Team",
            base_country="Test Country",
        )

        created_team = repository.create(team)
        db.commit()

        assert created_team.team_id is not None

        fetched_team = repository.get_by_id(created_team.team_id)

        assert fetched_team is not None
        assert fetched_team.team_id == created_team.team_id
        assert fetched_team.name == "Integration Test Team"
        assert fetched_team.base_country == "Test Country"

        teams = repository.list_all()

        assert any(
            existing.team_id == created_team.team_id
            for existing in teams
        )

        repository.delete(fetched_team)
        db.commit()

        assert repository.get_by_id(created_team.team_id) is None

    finally:
        db.close()