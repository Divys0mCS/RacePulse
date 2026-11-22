from app.database.connection import SessionLocal
from app.database.services.team_service import TeamService


def test_team_service_creates_reads_lists_and_deletes_team():
    db = SessionLocal()
    
    try:
        service = TeamService(db)

        created_team = service.create_team(
            name="Team Service Integration Test",
            base_country="Test Country",
        )

        assert created_team.team_id is not None

        fetched_team = service.get_team(created_team.team_id)

        assert fetched_team is not None
        assert fetched_team.name == "Team Service Integration Test"
        assert fetched_team.base_country == "Test Country"

        # Use limit=200 to ensure we capture the newly created team
        teams = service.list_teams(limit=200)

        assert any(
            team.team_id == created_team.team_id
            for team in teams
        )

        assert service.delete_team(created_team.team_id) is True
        assert service.get_team(created_team.team_id) is None

    finally:
        db.rollback()
        db.close()