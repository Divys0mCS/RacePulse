from app.database.connection import SessionLocal
from app.database.models.team import TeamModel


def test_team_can_be_inserted_and_read_back() -> None:
    session = SessionLocal()

    try:
        team = TeamModel(
            name="Red Bull Racing",
            base_country="Austria",
        )

        session.add(team)
        session.commit()
        session.refresh(team)

        assert team.team_id is not None

        saved_team = session.get(TeamModel, team.team_id)

        assert saved_team is not None
        assert saved_team.name == "Red Bull Racing"
        assert saved_team.base_country == "Austria"

        session.delete(saved_team)
        session.commit()

    finally:
        session.close()