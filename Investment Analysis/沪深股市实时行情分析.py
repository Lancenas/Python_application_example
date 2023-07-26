import tushare as ts
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def get_daily_quotes(stock_code, start_date, end_date):
    ts.set_token('c96bfb91e26676f8127aa8e473c48af9403d091c971ed282baf4be68-1')
    pro = ts.pro_api()
    df = pro.daily(ts_code=stock_code, start_date=start_date, end_date=end_date)
    if not df.empty:
        return df
    else:
        return None


def plot_daily_data(df):
    if df is None:
        print("No data available.")
        return

    df['trade_date'] = pd.to_datetime(df['trade_date'])
    df.sort_values(by='trade_date', ascending=True, inplace=True)

    plt.figure(figsize=(12, 6))
    plt.plot(df['trade_date'], df['close'], label='Close', color='b')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Daily Stock Price for {}'.format(df['ts_code'][0]))
    plt.legend()
    plt.grid(True)

    # Save the plot to a file (optional)
    plt.savefig('daily_stock_price_plot.png')

    plt.show()


def save_to_excel(df):
    if df is None:
        print("No data available to save.")
        return

    # Save the DataFrame to an Excel file
    df.to_excel('daily_stock_data.xlsx', index=False)
    print("Daily stock data saved to 'daily_stock_data.xlsx'.")


if __name__ == "__main__":
    stock_code = input("Enter the stock code (e.g., '000001.SZ') or 'e' to exit: ")

    while stock_code.lower() != 'e':
        start_date = input("Enter the start date (YYYYMMDD): ")
        end_date = input("Enter the end date (YYYYMMDD): ")

        df = get_daily_quotes(stock_code, start_date, end_date)
        plot_daily_data(df)
        save_to_excel(df)

        stock_code = input("Enter another stock code or 'e' to exit: ")
