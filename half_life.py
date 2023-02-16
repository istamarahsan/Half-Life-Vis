from typing import Protocol


class HalfLifeCalculator:
    def half_lives(self, time_elapsed: float, half_life: float) -> float:
        return time_elapsed/half_life

    def n_remaining(self, initial_amount: float, half_life: float, time_elapsed: float) -> float:
        return initial_amount * ((1/2)**(time_elapsed/half_life))
