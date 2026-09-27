"""End-to-end demo: load a laps CSV, then run PaceAnalyzer per driver.

This is the first place the full pipeline actually connects:
CSVLoader -> list[Lap] -> PaceAnalyzer -> printed report.
Telemetry is loaded and attached the same way, via TelemetryLoader.
"""

import sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from analytics.loaders.csv_loader import CSVLoader
from analytics.loaders.telemetry_loader import TelemetryLoader
from analytics.analysis.pace_analysis import PaceAnalyzer


def group_laps_by_driver(laps):
    """Group by driver_id (a plain int) rather than the Driver object itself,
    so this works regardless of whether Driver defines __eq__/__hash__."""
    laps_by_id = defaultdict(list)
    driver_by_id = {}
    for lap in laps:
        laps_by_id[lap.driver.driver_id].append(lap)
        driver_by_id[lap.driver.driver_id] = lap.driver
    return laps_by_id, driver_by_id


def main(csv_path: str, telemetry_csv_path: str | None = None) -> None:
    laps = CSVLoader().load(csv_path)
    print(f"Loaded {len(laps)} laps from {csv_path}\n")

    # Telemetry is optional: only attempt it if a file was actually given,
    # since not every laps CSV will have matching telemetry available yet.
    telemetry_by_lap_id = {}
    if telemetry_csv_path:
        telemetry_list = TelemetryLoader(laps).load(telemetry_csv_path)
        telemetry_by_lap_id = {t.lap.lap_id: t for t in telemetry_list}
        print(f"Loaded telemetry for {len(telemetry_list)} lap(s) from {telemetry_csv_path}\n")

    analyzer = PaceAnalyzer()
    laps_by_id, driver_by_id = group_laps_by_driver(laps)

    for driver_id, driver_laps in laps_by_id.items():
        driver = driver_by_id[driver_id]
        result = analyzer.analyze(driver_laps)
        fastest = result["fastest_lap"]
        print(f"{driver.name} ({driver.team.name})")
        print(f"  Laps analyzed:   {result['laps_analyzed']}")
        print(f"  Average lap:     {result['average_lap_time_seconds']:.3f}s")
        print(f"  Fastest lap:     #{fastest.lap_number} in {fastest.lap_time_seconds:.3f}s")

        for lap in sorted(driver_laps, key=lambda l: l.lap_number):
            telemetry = telemetry_by_lap_id.get(lap.lap_id)
            if telemetry is None:
                continue  # no telemetry loaded for this particular lap - skip it, don't fail
            max_speed = telemetry.max_speed_kph()
            avg_throttle = telemetry.average_throttle_pct()
            print(
                f"    Lap #{lap.lap_number} telemetry: "
                f"max speed {max_speed:.1f} kph, avg throttle {avg_throttle:.1f}%"
            )
        print()

    overall = analyzer.analyze(laps)
    fastest_overall = overall["fastest_lap"]
    print("Overall session")
    print(
        f"  Fastest lap:     {fastest_overall.driver.name}, "
        f"#{fastest_overall.lap_number} in {fastest_overall.lap_time_seconds:.3f}s"
    )


if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "data/sample/sample_laps.csv"
    telemetry_csv_path = sys.argv[2] if len(sys.argv) > 2 else "data/sample/sample_telemetry.csv"
    main(csv_path, telemetry_csv_path)