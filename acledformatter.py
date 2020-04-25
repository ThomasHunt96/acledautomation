import pandas as pd
import warnings
import sys
import calendar as cal
from datetime import datetime


def month_convert(month):
    name_to_number = {name: number for number, name in enumerate(cal.month_name) if number}  # dict month : month_num
    month_num = name_to_number.get(month)  # month number in int form
    return month_num


def date_format(in_date):  # converting date from textbased to dd-mm-yyyy format
    split_date = in_date.split()
    month_num = month_convert(split_date[1])
    out_date = split_date[0] + "-" + str(month_num) + "-" + split_date[2]
    return out_date


def between_date(d1, d2):  # Gets difference between two dates in string format "dd-mm-yy"
    d1list = d1.split("-")
    d2list = d2.split("-")
    date1 = datetime(int(d1list[2]), int(d1list[1]), int(d1list[0]))
    date2 = datetime(int(d2list[2]), int(d2list[1]), int(d2list[0]))

    return abs((date1 - date2).days) + 1  # Maybe add +1


def date_verify(date):
    date_format = "%d-%m-%Y"
    try:
        date_obj = datetime.strptime(date, date_format)
        return True

    except ValueError:
        print("Incorrect data format please input dd-mm-yyyy")
        return False


def drop_rows(inputdata, columnname, dropparameter):
    removedrows = inputdata.index[inputdata[columnname] == dropparameter].tolist()
    outputdata = inputdata.drop(removedrows)
    return outputdata


def get_admin2_list(df):
    uniqueadmin2 = df.admin2.unique()
    return uniqueadmin2


def get_all_occurences(df, value):
    occurences = df.loc[df['admin2'] == value]
    return occurences


def get_first_occurrence(df):
    adminlist = get_admin2_list(df)
    newdf = pd.DataFrame(columns=df.columns)

    for admin in adminlist:
        tempdf = get_all_occurences(df, admin)
        tempdf.sort_values('conflict_date', ascending=True)
        newdf = newdf.append(tempdf.tail(1))
    print(newdf)
    return newdf


def get_highest_fatalities(df):
    adminlist = get_admin2_list(df)
    newdf = pd.DataFrame(columns=df.columns)

    for admin in adminlist:
        tempdf = get_all_occurences(df, admin)
        tempdf.sort_values('fatalities', ascending=True)
        newdf = newdf.append(tempdf.tail(1))

    print(newdf)
    return newdf


def validate_acled(df):
    valid = False
    valid_labels = ["event_date", "country", "admin1", "admin2",
                    "location", "latitude", "longitude", "fatalities"]
    df_labels = df.columns

    for label in valid_labels:
        if label not in df_labels:
            valid = False
            break
        else:
            valid = True
    return valid


def validate_file(path):
    try:
        df = pd.read_csv(path)
        if validate_acled(df):
            return True
        else:
            return False
    except:
        print("Invalid path! Please use a valid ACLED .csv file")
        return False


def choose_file():
    valid_path = False
    while not valid_path:
        path = input("Please input path to an ACLED .csv file...\n")
        valid_path = validate_file(path)
    return path


def main():
    warnings.filterwarnings('ignore')

    path = choose_file()

    tempdf = pd.read_csv(path)
    df = tempdf[["event_date", "country", "admin1", "admin2",
                 "location", "latitude", "longitude", "fatalities"]]

    # user input start date, format dd-mm-yyyy
    is_date_verified = False
    while not is_date_verified:
        start_date = input("Please input valid start date (dd-mm-yyyy)...\n")
        is_date_verified = date_verify(start_date)
    print("Correct start date, calculating conflict dates...\n")

    # event_date is given in incorrect format, so formatting to dd-mm-yyyy required
    event_dates = df["event_date"].tolist()
    formatted_event_dates = [date_format(date) for date in event_dates]
    conflict_dates = [between_date(d,start_date) for d in formatted_event_dates]

    # replacing event_date
    df.loc[:, "event_date"] = conflict_dates
    df.rename(columns={'event_date': 'conflict_date'}, inplace=True)

    df = drop_rows(df, 'fatalities', 0)

    valid_input = False
    valid_inputs = [1, 2]
    print("Filter data by: 1. First Occurence  2. Highest Fatalities,\n")
    while not valid_input:
        userInput = int(input())
        if userInput not in valid_inputs:
            print("Filter data by: 1. First Occurence, 2. Highest Fatalities,\n")
        else:
            valid_input = True
    if userInput == 1:
        df = get_first_occurrence(df)
    elif userInput == 2:
        df = get_highest_fatalities(df)

    # Exporting CSV to locations.csv
    output_df = df[['location', 'admin1', 'country', 'latitude', 'longitude', 'conflict_date']]
    output_df.rename(columns={'location': 'name', 'admin1': 'reigon'}, inplace=True)
    output_df["location_type"] = "conflict"
    output_df["population"] = "null"

    output_path = input("Enter output filename...\n") + ".csv"
    output_df.to_csv(output_path, index=False)


process_new_file = True


def another_file():
    user_input = input("Do you want to process another file? (y/n)\n")
    valid_inputs = ['y', 'n']
    while user_input not in valid_inputs:
        user_input = input("Do you want to process another file? (y/n)\n")
    if user_input is 'y':
        return True
    else:
        sys.exit()
        return False

while process_new_file is True:
    main()
    process_new_file = another_file()
