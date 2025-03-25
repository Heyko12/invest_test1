from freqtrade.strategy import IStrategy
import pandas as pd
import talib

class MACD(IStrategy):
    timeframe = "1d"
    minimal_roi = {"0": 0.1}
    stoploss = -0.1
    trailing_stop = False

    def populate_indicators(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        # Подставляем рекомендованные параметры по сглаживанию: MACD = EMA12 - EMA26; MACDSIGNAL = EMA(MACD)9
        dataframe['macd'], dataframe['macdsignal'], _ = talib.MACD(dataframe['close'], fastperiod=12, slowperiod=26, signalperiod=9)
        return dataframe

    def populate_entry_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        # Если MACD > MACDSIGNAL, играем на повышение, если меньше - иначе
        dataframe.loc[dataframe['macd'] > dataframe['macdsignal'], 'enter_long'] = 1
        dataframe.loc[dataframe['macd'] < dataframe['macdsignal'], 'enter_short'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        # В точности до наоборот относительно entry-правила
        dataframe.loc[dataframe['macd'] < dataframe['macdsignal'], 'exit_long'] = 1
        dataframe.loc[dataframe['macd'] > dataframe['macdsignal'], 'exit_short'] = 1
        return dataframe