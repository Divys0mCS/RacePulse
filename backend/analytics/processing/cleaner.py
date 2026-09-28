from app.models.telemetry import TelemetrySample


class TelemetryCleaner:
    """Cleans telemetry samples before downstream processing."""

    def clean(self, samples: list[TelemetrySample]) -> list[TelemetrySample]:
        """Return telemetry samples sorted by distance with exact duplicates removed."""

        ordered_samples = sorted(samples, key=lambda sample: sample.distance_m)

        cleaned_samples = []
        seen_samples = set()

        for sample in ordered_samples:
            if sample in seen_samples:
                continue

            seen_samples.add(sample)
            cleaned_samples.append(sample)

        return cleaned_samples