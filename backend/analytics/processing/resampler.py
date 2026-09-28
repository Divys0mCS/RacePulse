import math


class TelemetryResampler:
    """Resamples transformed telemetry onto a regular distance grid."""

    def resample(self, samples: list[dict], step_m: float) -> list[dict]:
        """Return telemetry samples on a regular distance grid."""

        if step_m <= 0:
            raise ValueError("step_m must be greater than zero")

        if not samples:
            return []

        ordered = sorted(samples, key=lambda sample: sample["distance_m"])

        distances = [sample["distance_m"] for sample in ordered]

        if len(ordered) == 1:
            return [dict(ordered[0])]

        result_distances = [
            distances[0] + i * step_m
            for i in range(
                math.floor((distances[-1] - distances[0]) / step_m) + 1
            )
        ]

        if not math.isclose(result_distances[-1], distances[-1]):
            result_distances.append(distances[-1])

        continuous_keys = (
            "distance_pct",
            "speed_kph",
            "throttle_pct",
            "brake_pct",
        )

        discrete_keys = ("gear", "rpm")

        result = []

        for target_distance in result_distances:
            if target_distance <= distances[0]:
                lower = upper = ordered[0]
            elif target_distance >= distances[-1]:
                lower = upper = ordered[-1]
            else:
                upper_index = next(
                    i
                    for i, distance in enumerate(distances)
                    if distance >= target_distance
                )

                lower = ordered[upper_index - 1]
                upper = ordered[upper_index]

            if lower["distance_m"] == upper["distance_m"]:
                ratio = 0.0
            else:
                ratio = (
                    target_distance - lower["distance_m"]
                ) / (
                    upper["distance_m"] - lower["distance_m"]
                )

            point = {
                "distance_m": target_distance,
            }

            for key in continuous_keys:
                point[key] = round(
                    lower[key] + ratio * (upper[key] - lower[key]),
                    6,
                )

            nearest = (
                lower
                if abs(target_distance - lower["distance_m"])
                <= abs(target_distance - upper["distance_m"])
                else upper
            )

            for key in discrete_keys:
                point[key] = nearest[key]

            result.append(point)

        return result