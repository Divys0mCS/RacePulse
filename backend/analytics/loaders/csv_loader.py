"""Loads race data from a flat CSV into the Track/Race/Session/Team/Driver/Lap object graph.

Expected CSV schema (one row per lap):

    season, round_number, race_name, track_name, track_country,
    track_length_km, track_corners, race_date, session_type,
    team_name, team_base_country, driver_number, driver_name,
    driver_nationality, lap_number, lap_time_seconds,
    sector_1_time_seconds, sector_2_time_seconds, sector_3_time_seconds

Real telemetry exports repeat the track/race/session/team/driver fields on
every single lap row (a "denormalized" layout) rather than splitting them
into separate linked files. This loader turns that flat layout back into
properly linked objects.

The session_type column must match a SessionType member NAME exactly
(case-insensitive): FP1, FP2, FP3, SPRINT_QUALIFYING, SPRINT, QUALIFYING,
RACE. This is the enum member's name, not its display value - write
"sprint_qualifying" in the CSV, not "Sprint Qualifying".
"""

import csv
from datetime import datetime
from pathlib import Path

from app.models.driver import Driver
from app.models.lap import Lap
from app.models.race import Race
from app.models.session import Session, SessionType
from app.models.team import Team
from app.models.track import Track


REQUIRED_COLUMNS = {
    "season",
    "round_number",
    "race_name",
    "track_name",
    "track_country",
    "track_length_km",
    "track_corners",
    "race_date",
    "session_type",
    "team_name",
    "team_base_country",
    "driver_number",
    "driver_name",
    "driver_nationality",
    "lap_number",
    "lap_time_seconds",
    "sector_1_time_seconds",
    "sector_2_time_seconds",
    "sector_3_time_seconds",
}


class CSVLoader:
    """Loads a flat laps CSV into fully-linked model objects.

    One CSVLoader instance should be used per file (or per related batch of
    files) so that identical tracks/races/sessions/teams/drivers across rows
    are deduplicated into single shared objects instead of being recreated
    per row.
    """

    def __init__(self) -> None:
        self._tracks: dict[str, Track] = {}
        self._races: dict[tuple[str, int], Race] = {}
        self._sessions: dict[tuple[str, int, str], Session] = {}
        self._teams: dict[str, Team] = {}
        self._drivers: dict[str, Driver] = {}
        self._next_lap_id = 1

    def load(self, csv_path: str | Path) -> list[Lap]:
        """Read the CSV at csv_path and return one Lap per row, fully linked."""
        csv_path = Path(csv_path)

        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")

        laps: list[Lap] = []

        with csv_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self._validate_header(reader.fieldnames, csv_path)

            for row_number, row in enumerate(reader, start=2):
                try:
                    laps.append(self._row_to_lap(row))
                except (KeyError, ValueError) as e:
                    raise ValueError(
                        f"Row {row_number} in {csv_path.name} is malformed: {e}"
                    ) from e

        return laps

    def _validate_header(self, fieldnames, csv_path: Path) -> None:
        missing = REQUIRED_COLUMNS - set(fieldnames or [])

        if missing:
            raise ValueError(
                f"{csv_path.name} is missing required column(s): {sorted(missing)}"
            )

    def _row_to_lap(self, row: dict) -> Lap:
        track = self._get_or_create_track(row)
        race = self._get_or_create_race(row, track)
        session = self._get_or_create_session(row, race)
        team = self._get_or_create_team(row)
        driver = self._get_or_create_driver(row, team)

        lap = Lap(
            lap_id=self._next_lap_id,
            session=session,
            driver=driver,
            lap_number=int(row["lap_number"]),
            lap_time_seconds=float(row["lap_time_seconds"]),
            sector_times=(
                float(row["sector_1_time_seconds"]),
                float(row["sector_2_time_seconds"]),
                float(row["sector_3_time_seconds"]),
            ),
        )

        self._next_lap_id += 1

        session.add_lap(lap)

        return lap

    def _get_or_create_track(self, row: dict) -> Track:
        key = row["track_name"]

        if key not in self._tracks:
            self._tracks[key] = Track(
                track_id=len(self._tracks) + 1,
                name=row["track_name"],
                country=row["track_country"],
                length_km=float(row["track_length_km"]),
                number_of_corners=int(row["track_corners"]),
            )

        return self._tracks[key]

    def _get_or_create_race(self, row: dict, track: Track) -> Race:
        key = (row["race_name"], int(row["season"]))

        if key not in self._races:
            self._races[key] = Race(
                race_id=len(self._races) + 1,
                name=row["race_name"],
                season=int(row["season"]),
                round_number=int(row["round_number"]),
                track=track,
                race_date=datetime.strptime(
                    row["race_date"], "%Y-%m-%d"
                ).date(),
            )

        return self._races[key]

    def _get_or_create_session(self, row: dict, race: Race) -> Session:
        raw_type = row["session_type"].strip().upper()
        key = (race.name, race.season, raw_type)

        if key not in self._sessions:
            try:
                session_type = SessionType[raw_type]
            except KeyError:
                valid = ", ".join(member.name for member in SessionType)

                raise ValueError(
                    f"Unrecognized session_type {row['session_type']!r}. "
                    f"Must be one of (case-insensitive): {valid}"
                )

            self._sessions[key] = Session(
                session_id=len(self._sessions) + 1,
                race=race,
                session_type=session_type,
            )

        return self._sessions[key]

    def _get_or_create_team(self, row: dict) -> Team:
        key = row["team_name"]

        if key not in self._teams:
            self._teams[key] = Team(
                team_id=len(self._teams) + 1,
                name=row["team_name"],
                base_country=row["team_base_country"],
            )

        return self._teams[key]

    def _get_or_create_driver(self, row: dict, team: Team) -> Driver:
        key = row["driver_number"]

        if key not in self._drivers:
            self._drivers[key] = Driver(
                driver_id=len(self._drivers) + 1,
                name=row["driver_name"],
                number=int(row["driver_number"]),
                nationality=row["driver_nationality"],
                team=team,
            )

        return self._drivers[key]