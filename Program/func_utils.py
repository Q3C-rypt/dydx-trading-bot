from datetime import datetime, timedelta

# Format number function
def format_number(curr_num, match_num): #Function to match desired number of decimales needed

    """
    Give current number an example of number with decimals desired
    Function will return the correctly formatted string
    """

    curr_num_string = f"{curr_num}"
    match_num_string = f"{match_num}"

    if "." in match_num_string:
        match_decimals = len(match_num_string.split(".")[1])
        curr_num_string = f"{curr_num:.{match_decimals}f}"
        curr_num_string = curr_num_string[:]
        return curr_num_string
    else:
        return f"{int(curr_num)}"
    

# Format time
def format_time(timestamp):
    return timestamp.replace(microsecond = 0).isoformat() # returns time in iso format, good format for dydx API


# Get ISO Times
def get_ISO_times():

    # Get time stamps
    date_start_0 = datetime.now()
    date_start_1 = date_start_0 - timedelta(hours = 100) #start time 100 hours before now time. This is cause function with dydx API lets you get a max of 100 hours of data. But we can keep stacking these, so we can keep going 100 hours back using this func.
    date_start_2 = date_start_1 - timedelta(hours = 100)
    date_start_3 = date_start_2 - timedelta(hours = 100)
    date_start_4 = date_start_3 - timedelta(hours = 100) # Good enough historical data to work with, about 16 days

    # Format datetimes 
    times_dict = {
        "range_1": {
            "from_iso": format_time(date_start_1), # not in right format for dydx API to read, it's in python time, so we use format_time function
            "to_iso": format_time(date_start_0),
        },
        "range_2": {
            "from_iso": format_time(date_start_2), 
            "to_iso": format_time(date_start_1),
        },
        "range_3": {
            "from_iso": format_time(date_start_3), 
            "to_iso": format_time(date_start_2),
        },
        "range_4": {
            "from_iso": format_time(date_start_4), 
            "to_iso": format_time(date_start_3),
        },
    }

    # Return result
    return times_dict
  