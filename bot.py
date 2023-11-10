# SPDX-License-Identifier: BSD-3-Clause

# flake8: noqa F401

import numpy as np

from vendeeglobe import (
    Checkpoint,
    Heading,
    Instructions,
    Location,
    MapProxy,
    Vector,
    WeatherForecast,
    config,
)
from vendeeglobe.utils import distance_on_surface

CREATOR = "Bjørn Hurtigsejl"


class Bot:
    """
    This is the ship-controlling bot that will be instantiated for the competition.
    """

    def __init__(self):
        self.team = CREATOR  # Mandatory attribute
        self.avatar = "../../solution/hard-ship.png"  # Optional attribute
        self.course = [
            Checkpoint(
                latitude=config.start.latitude,
                longitude=config.start.longitude - 1,
                radius=5,
            ),
            Checkpoint(57.987, -49.846, radius=50),
            Checkpoint(57.987, -49.846, radius=50),
            Checkpoint(73.95, -66.51, radius=50),
            Checkpoint(74.19, -87.97, radius=50),
            Checkpoint(74.27, -103.58, radius=30),
            Checkpoint(73.80, -112.58, radius=30),
            Checkpoint(75.52, -123.23, radius=30),
            Checkpoint(75.02, -125.23, radius=30),
            Checkpoint(70.64, -129.22, radius=30),
            Checkpoint(70.29, -137.00, radius=30),
            Checkpoint(70.96, -147.39, radius=40),
            Checkpoint(71.60, -158.24, radius=30),
            Checkpoint(68.26, -169.57, radius=30),
            Checkpoint(65.691, -168.350, radius=50),
            Checkpoint(63.180, -168.108, radius=50),
            Checkpoint(52.8895, -169.3980, radius=30),
            Checkpoint(11.80, -183.94, radius=50),  # checkpoint 1
            Checkpoint(13.29, 166.15, radius=30),
            Checkpoint(6.50, 133.946, radius=30),
            Checkpoint(4.597, 125.554, radius=50),
            Checkpoint(1.498, 119.796, radius=30),
            Checkpoint(-8.574, 115.791, radius=30),
            Checkpoint(-9.291, 115.528, radius=30),
            Checkpoint(-6.0, 80.67, radius=50),  # checkpoint 2
            Checkpoint(11.352, 52.241, radius=50),
            Checkpoint(12.695, 51.187, radius=50),
            Checkpoint(12.288, 43.681, radius=30),
            Checkpoint(13.540, 42.633, radius=30),
            Checkpoint(27.526, 34.111, radius=50),
            Checkpoint(28.484, 33.157, radius=30),
            Checkpoint(29.7812, 32.5019, radius=20),
            Checkpoint(32.401, 32.357, radius=50),
            Checkpoint(36.400, 14.585, radius=50),
            Checkpoint(37.824, 9.900, radius=50),
            Checkpoint(37.738, 2.172, radius=50),
            Checkpoint(36.161, -2.016, radius=50),
            Checkpoint(35.9961, -5.4028, radius=30),
            Checkpoint(35.9316, -6.0423, radius=30),
            Checkpoint(36.837, -10.173, radius=40),
            Checkpoint(44.005, -10.016, radius=40),
            Checkpoint(
                latitude=config.start.latitude,
                longitude=config.start.longitude,
                radius=5,
            ),
        ]

    def run(
        self,
        t: float,
        dt: float,
        longitude: float,
        latitude: float,
        heading: float,
        speed: float,
        vector: np.ndarray,
        forecast: WeatherForecast,
        world_map: MapProxy,
    ):
        """
        This is the method that will be called at every time step to get the
        instructions for the ship.

        Parameters
        ----------
        t:
            The current time in hours.
        dt:
            The time step in hours.
        longitude:
            The current longitude of the ship.
        latitude:
            The current latitude of the ship.
        heading:
            The current heading of the ship.
        speed:
            The current speed of the ship.
        vector:
            The current heading of the ship, expressed as a vector.
        forecast:
            The weather forecast for the next 5 days.
        world_map:
            The map of the world: 1 for sea, 0 for land.
        """
        instructions = Instructions()
        for ch in self.course:
            dist = distance_on_surface(
                longitude1=longitude,
                latitude1=latitude,
                longitude2=ch.longitude,
                latitude2=ch.latitude,
            )
            jump = dt * np.linalg.norm(speed)
            if dist < 2.0 * ch.radius + jump:
                instructions.sail = min(ch.radius / jump, 1)
            else:
                instructions.sail = 1.0
            if dist < ch.radius:
                ch.reached = True
            if not ch.reached:
                instructions.location = Location(
                    longitude=ch.longitude, latitude=ch.latitude
                )
                break

        return instructions
