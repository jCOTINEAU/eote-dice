#!/usr/bin/env python3

import collections
import operator
from typing import Mapping, Tuple

class QuadDistribution:
    def __init__(self, distribution: Mapping[Tuple[int, int, int, int], int] = None):
        if distribution is None:
            distribution = {(0, 0, 0, 0): 1}
        self._distribution = distribution

    def _total(self) -> int:
        return sum(self._distribution.values())

    def mean(self) -> Tuple[float, float, float, float]:
        val_sum = [0, 0, 0, 0]
        for value, frequency in self._distribution.items():
            for i in range(0, 4):
                val_sum[i] = val_sum[i] + value[i] * frequency
        for i in range(0, 4):
            val_sum[i] /= self._total()
        return tuple(val_sum)

    def standard_deviation(self) -> Tuple[float, float, float, float]:
        mean = self.mean()
        val_sum = [0, 0, 0, 0]
        for value, frequency in self._distribution.items():
            for i in range(0, 4):
                val_sum[i] = val_sum[i] + (value[i] - mean[i]) ** 2 * frequency
        for i in range(0, 4):
            val_sum[i] = (val_sum[i] / self._total()) ** 0.5
        return tuple(val_sum)

    def median(self) -> Tuple[int, int, int, int]:
        val_median = [0, 0, 0, 0]
        _total = self._total()
        _half_total = _total // 2

        for i in range (0, 4):
            sorted_values = sorted(self._distribution.items(), key=lambda item: item[0][i])
            cumulative_frequency = 0
            for index, (item, frequency) in enumerate(sorted_values):
                cumulative_frequency += frequency
                if cumulative_frequency > _half_total:
                    # We have passed the median point, take the current value as the median
                    val_median[i] = item[i]
                    break
                elif cumulative_frequency == _half_total and _total % 2 == 0:
                    # Special case for even total: need to average two elements
                    next_item = sorted_values[index + 1]
                    val_median[i] = (item[i] + next_item[0][i]) / 2
                    break
        return tuple(val_median)

    def probability_above(self,
                          cutoff: Tuple[int, int, int, int] = (None, None, None, None)) -> float:
        hits = 0
        for (value, frequency) in self._distribution.items():
            for i, cut in enumerate(cutoff):
                if cut is not None and value[i] < cut:
                    # This does make the cut.
                    break
            # Executed when the loop terminates through exhaustion (not a break).
            else:
                hits += frequency
        return hits / self._total()

    def probability(self,
                          cutoff: Tuple[int, int, int, int] = (None, None, None, None)) -> float:
        hits = 0
        for (value, frequency) in self._distribution.items():
            for i, cut in enumerate(cutoff):
                if cut is not None and value[i] != cut:
                    # This does make the cut.
                    break
            # Executed when the loop terminates through exhaustion (not a break).
            else:
                hits += frequency
        return hits / self._total()

    def probability_with_operator(self,
            cutoff_with_operator: Tuple[Tuple[int,operator],Tuple[int,operator],Tuple[int,operator],Tuple[int,operator]]=(None,None,None,None))  -> float:
        hits = 0
        for (value, frequency) in self._distribution.items():
            for i, cut in enumerate(cutoff_with_operator):
                if cut is not None and not cut[1](value[i],cut[0]):
                    # This does make the cut.
                    break
            # Executed when the loop terminates through exhaustion (not a break).
            else:
                hits += frequency
        return hits / self._total()

    def add(self, that: 'QuadDistribution') -> 'QuadDistribution':
        elements = collections.defaultdict(int)
        for value_i, frequency_i in self._distribution.items():
            for value_j, frequency_j in that._distribution.items():
                value = [0, 0, 0, 0]
                for i in range(0, 4):
                    value[i] = value_i[i] + value_j[i]
                frequency = frequency_i * frequency_j
                elements[tuple(value)] += frequency

        return QuadDistribution(elements)
