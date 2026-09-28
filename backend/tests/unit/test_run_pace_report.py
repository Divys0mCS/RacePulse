from pathlib import Path

from scripts.run_pace_report import main


LAP_HEADER = (
    "season,round_number,race_name,track_name,track_country,track_length_km,"
    "track_corners,race_date,session_type,team_name,team_base_country,"
    "driver_number,driver_name,driver_nationality,lap_number,lap_time_seconds,"
    "sector_1_time_seconds,sector_2_time_seconds,sector_3_time_seconds\n"
)

LAP_ROWS = (
    "2024,10,British Grand Prix,Silverstone,United Kingdom,5.891,18,"
    "2024-07-07,race,Red Bull Racing,Austria,1,Max Verstappen,Dutch,"
    "1,90.0,28.0,30.0,32.0\n"
    "2024,10,British Grand Prix,Silverstone,United Kingdom,5.891,18,"
    "2024-07-07,race,Red Bull Racing,Austria,1,Max Verstappen,Dutch,"
    "2,87.5,27.5,29.8,30.2\n"
)

TELEMETRY_HEADER = (
    "driver_number,lap_number,distance_m,speed_kph,"
    "throttle_pct,brake_pct,gear,rpm\n"
)

TELEMETRY_ROWS = (
    "1,1,0,120,80,0,4,9000\n"
    "1,1,1000,250,100,0,7,11000\n"
    "1,2,0,130,85,0,4,9200\n"
    "1,2,1000,280,100,0,8,11800\n"
)


def test_run_pace_report_generates_all_visualizations(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    lap_csv = tmp_path / "laps.csv"
    telemetry_csv = tmp_path / "telemetry.csv"

    lap_csv.write_text(LAP_HEADER + LAP_ROWS)
    telemetry_csv.write_text(TELEMETRY_HEADER + TELEMETRY_ROWS)

    main(str(lap_csv), str(telemetry_csv))

    output_dir = Path("data/processed")

    assert (output_dir / "lap_chart_driver1.html").exists()
    assert (output_dir / "sector_chart_driver1.html").exists()
    assert (output_dir / "speed_trace_driver1_lap2.html").exists()