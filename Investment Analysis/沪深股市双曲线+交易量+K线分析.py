import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # 使用TkAgg后端
import matplotlib.pyplot as plt
import tushare as ts

# 设置Tushare的token
ts.set_token('c96bfb91e26676f8127aa8e473c48af9403d091c971ed282baf4be68')

# 获取股票数据
def get_stock_data(code, start_date, end_date):
    pro = ts.pro_api()
    df = pro.daily(ts_code=code, start_date=start_date, end_date=end_date)
    if 'vol' not in df.columns:
        raise ValueError("The 'vol' column (trading volume) is missing in the retrieved data.")
    df = df[['trade_date', 'close', 'vol']]
    df.sort_values('trade_date', inplace=True)
    df['trade_date'] = pd.to_datetime(df['trade_date'])
    df.set_index('trade_date', inplace=True)
    return df

# 计算移动平均线
def calculate_ma(df, window):
    return df['close'].rolling(window=window).mean()

# 分析交易量和K线
def analyze_volume_and_kline(df):
    # 计算涨跌幅
    df['change'] = df['close'].pct_change()

    # 计算5日均线
    df['ma5'] = df['close'].rolling(window=5).mean()

    # 计算量比，即今日成交量与5日均量的比值
    df['volume_ratio'] = df['vol'] / df['vol'].rolling(window=5).mean()

    # 根据条件判断买入和卖出信号
    df['signal'] = np.where((df['change'] > 0) & (df['volume_ratio'] > 1), 1,
                            np.where((df['change'] < 0) & (df['volume_ratio'] > 1), -1, 0))

    return df

# 绘制股票双曲线图和交易信号
def plot_stock_chart(df, ma_short, ma_long):
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['close'], label='Close Price', color='blue')
    plt.plot(df.index, ma_short, label='Short MA', color='orange')
    plt.plot(df.index, ma_long, label='Long MA', color='red')
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Stock Price with Moving Averages')
    plt.grid()
    plt.show()

    # 绘制交易信号
    buy_signals = df[df['signal'] == 1]
    sell_signals = df[df['signal'] == -1]

    plt.scatter(buy_signals.index, df.loc[buy_signals.index, 'close'], marker='^', color='g', label='Buy Signal')
    plt.scatter(sell_signals.index, df.loc[sell_signals.index, 'close'], marker='v', color='r', label='Sell Signal')

    plt.legend()

def main():
    while True:
        stock_code = input("请输入股票代码（例如：000001.SZ），输入'e'退出：")
        if stock_code.lower() == 'e':
            print("程序已退出。")
            break

        start_date = input("请输入起始日期（例如：2020-01-01）：")
        end_date = input("请输入结束日期（例如：2021-12-31）：")
        short_window = int(input("请输入短期窗口大小："))
        long_window = int(input("请输入长期窗口大小："))

        df = get_stock_data(stock_code, start_date, end_date)
        if df.empty:
            print("获取数据失败，请检查输入的股票代码和日期范围。")
            continue

        short_ma = calculate_ma(df, short_window)
        long_ma = calculate_ma(df, long_window)

        df = analyze_volume_and_kline(df)

        plot_stock_chart(df, short_ma, long_ma)

if __name__ == "__main__":
    main()
