import tushare as ts
import pandas as pd

# Replace 'YOUR_TUSHARE_API_KEY' with your Tushare API key (optional)
# If you don't have an API key, you can still use the library but with limited access.
ts.set_token('c96bfb91e26676f8127aa8e473c48af9403d091c971ed282baf4be68-1')

# Initialize the Tushare pro API
pro = ts.pro_api()

def get_ipo_list(start_date, end_date):
    # Set the initial offset and limit values
    offset = 0
    limit = 50  # You can adjust this value based on your needs, but 50 is the maximum per request

    all_ipo_list = []

    while True:
        # Get IPO new stock listings for the current page
        current_page_data = pro.new_share(start_date=start_date, end_date=end_date, offset=offset, limit=limit)

        # If there is no data for the current page, break the loop
        if current_page_data.empty:
            break

        # Append the current page data to the overall IPO list
        all_ipo_list.append(current_page_data)

        # Increment the offset for the next page
        offset += limit

    # Concatenate all the data frames to get the final result
    all_ipo_list = pd.concat(all_ipo_list).reset_index(drop=True)

    return all_ipo_list

while True:
    # Interactive input for start_date and end_date
    start_date = input("Enter the start date (YYYYMMDD): ")
    end_date = input("Enter the end date (YYYYMMDD): ")

    # Get IPO new stock listings
    all_ipo_listings = get_ipo_list(start_date, end_date)

    # Display IPO new stock listings
    print(all_ipo_listings)

    # Ask if the user wants to continue or exit
    choice = input("Enter 'e' to exit or any other key to continue: ")
    if choice.lower() == 'e':
        break
