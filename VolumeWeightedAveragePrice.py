import numpy as np
import pandas as pd
from dataclasses import dataclass

@dataclass
class VWAPRecord:
	value: float
	conf_i: int
	conf_timestamp: pd.Timestamp

class VolumeWeightedAveragePrice:
	def __init__(self, anchor_type: str):
		self._achr = anchor_type
		self._cumulative_typical_price = 0
		self._cumulative_volume = 0
		self.curr_vwap = np.nan
		self.vwap = []

	def update(self, i: int, time_index: pd.DatetimeIndex, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray, volume: np.ndarray):
		if i < 8:
			return

		if i % 24 - 8 == 0:
			self._cumulative_typical_price = 0
			self._cumulative_volume = 0

		self._cumulative_typical_price += np.mean([high[i],low[i],close[i]]) * volume[i]
		self._cumulative_volume += volume[i]

		self.curr_vwap = self._cumulative_typical_price / self._cumulative_volume
		self.vwap.append(VWAPRecord(value=self.curr_vwap, conf_i=i, conf_timestamp=time_index[i]))
