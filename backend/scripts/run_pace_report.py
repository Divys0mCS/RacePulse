"""End-to-end demo: load a laps CSV, then run every analyzer per driver.

This is the place the full pipeline connects:
CSVLoader -> list[Lap] -> {Pace, Consistency, Sector}Analyzer -> printed report.
Telemetry is loaded and attached the same way, via TelemetryLoader, and the
fastest lap's speed trace (when telemetry exists for it) is saved as HTML.
"""

import sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from analytics.loaders.csv_loader import CSVLoader
from analytics.loaders.telemetry_loader import TelemetryLoader
from analytics.analysis.pace_analysis import PaceAnalyzer
from analytics.analysis.consistency_analysis import ConsistencyAnalyzer
from analytics.analysis.sector_analysis import SectorAnalyzer
from analytics.visualization.speed_trace import build_speed_trace


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

    telemetry_by_lap_id = {}
    if telemetry_csv_path:
        telemetry_list = TelemetryLoader(laps).load(telemetry_csv_path)
        telemetry_by_lap_id = {t.lap.lap_id: t for t in telemetry_list}
        print(f"Loaded telemetry for {len(telemetry_list)} lap(s) from {telemetry_csv_path}\n")

    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)

    pace_analyzer = PaceAnalyzer()
    consistency_analyzer = ConsistencyAnalyzer()
    sector_analyzer = SectorAnalyzer()
    laps_by_id, driver_by_id = group_laps_by_driver(laps)

    for driver_id, driver_laps in laps_by_id.items():
        driver = driver_by_id[driver_id]
        pace = pace_analyzer.analyze(driver_laps)
        consistency = consistency_analyzer.analyze(driver_laps)
        sectors = sector_analyzer.analyze(driver_laps)
        fastest = pace["fastest_lap"]

        print(f"{driver.name} ({driver.team.name})")
        print(f"  Laps analyzed:   {pace['laps_analyzed']}")
        print(f"  Average lap:     {pace['average_lap_time_seconds']:.3f}s")
        print(f"  Fastest lap:     #{fastest.lap_number} in {fastest.lap_time_seconds:.3f}s")
        if consistency["consistency_stdev_seconds"] is not None:
            print(f"  Consistency:     stdev {consistency['consistency_stdev_seconds']:.3f}s")
        print(
            f"  Best sectors:    "
            f"S1 {sectors['fastest_sector_1_seconds']:.3f}s / "
            f"S2 {sectors['fastest_sector_2_seconds']:.3f}s / "
            f"S3 {sectors['fastest_sector_3_seconds']:.3f}s"
        )

        for lap in sorted(driver_laps, key=lambda l: l.lap_number):
            telemetry = telemetry_by_lap_id.get(lap.lap_id)
            if telemetry is None:
                continue
            max_speed = telemetry.max_speed_kph()
            avg_throttle = telemetry.average_throttle_pct()
            print(
                f"    Lap #{lap.lap_number} telemetry: "
                f"max speed {max_speed:.1f} kph, avg throttle {avg_throttle:.1f}%"
            )

        fastest_telemetry = telemetry_by_lap_id.get(fastest.lap_id)
        if fastest_telemetry is not None:
            fig = build_speed_trace(fastest_telemetry)
            output_path = output_dir / f"speed_trace_driver{driver.number}_lap{fastest.lap_number}.html"
            fig.write_html(output_path)
            print(f"  Saved speed trace for fastest lap -> {output_path}")
        print()

    overall_pace = pace_analyzer.analyze(laps)
    overall_sectors = sector_analyzer.analyze(laps)
    fastest_overall = overall_pace["fastest_lap"]
    print("Overall session")
    print(
        f"  Fastest lap:     {fastest_overall.driver.name}, "
        f"#{fastest_overall.lap_number} in {fastest_overall.lap_time_seconds:.3f}s"
    )
    print(
        f"  Best sectors:    "
        f"S1 {overall_sectors['fastest_sector_1_seconds']:.3f}s / "
        f"S2 {overall_sectors['fastest_sector_2_seconds']:.3f}s / "
        f"S3 {overall_sectors['fastest_sector_3_seconds']:.3f}s"
    )


if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "data/sample/sample_laps.csv"
    telemetry_csv_path = sys.argv[2] if len(sys.argv) > 2 else "data/sample/sample_telemetry.csv"
    main(csv_path, telemetry_csv_path)