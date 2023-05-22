#!/usr/bin/env python

import csv
import codecs
import pprint
import json
from arg_parse import parse_arguments
from rec_score_analytic import get_column_data, weight_rec_score_data

# Parse command line arguments
args = parse_arguments()

# File to output the results to
OUTPUT_FILE = "output.json"

# Assign the arguments to constant variables
# See cell_meets_filter_condition func for conditional logic
FILE = args.file
STATE = args.state.upper()
NUM_FACILITIES = args.num_facilities
MIN_OVERALL_RATING = args.min_rating
MIN_NUM_BEDS = args.num_beds
MAX_NUM_DEFICIENCIES = args.max_deficiencies
MAX_NUM_PENALTIES = args.max_penalties

# List of columns to filter dataset by
# Must match the CSV file headers and the command line arguments except for FILE
FILTER_COLUMNS = [
    "Provider State",
    "Overall Rating",
    "Number of Certified Beds",
    "Rating Cycle 1 Total Number of Health Deficiencies",
    "Total Number of Penalties",
]

# List of columns to include in the output
# Must match the CSV file headers
# If adding or removing columns, update the OUTPUT_COLUMN_NAMES dictionary
OUTPUT_COLUMNS = [
    "Provider Name",
    "Provider Address",
    "Provider City",
    "Provider State",
    "Provider Zip Code",
    "Number of Certified Beds",
    "Average Number of Residents per Day",
    "Overall Rating",
    "Rating Cycle 1 Total Number of Health Deficiencies",
    "Total Number of Penalties",
]

RECOMMEND_SCORE_COLUMN_DICT = [
    "Overall Rating",
    "Number of Certified Beds",
    "Average Number of Residents per Day",
    "Rating Cycle 1 Total Number of Health Deficiencies",
    "Total Number of Penalties",
    "Abuse Icon",
    "Most Recent Health Inspection More Than 2 Years Ago",
    "With a Resident and Family Council",
    "Reported Physical Therapist Staffing Hours per Resident Per Day",
    "Number of Facility Reported Incidents",
    "Number of Substantiated Complaints",
]

# Dictionary used to format the output
# Output will be a list of dictionaries
# Each dictionary will represent a facility
# Each key in this dictionary will represent a key in the output dictionary
# Each value array will represent the column cell values in the CSV 
# For arrays with more than one value they will be concatenated with a comma and space
OUTPUT_COLUMN_NAMES = {
    "name": ["Provider Name"],
    "address": [
        "Provider Address",
        "Provider City",
        "Provider State",
        "Provider Zip Code",
    ],
    "num_beds": ["Number of Certified Beds"],
    "residents_per_day:": ["Average Number of Residents per Day"],
    "overall_rating": ["Overall Rating"],
    "num_deficiencies": ["Rating Cycle 1 Total Number of Health Deficiencies"],
    "num_penalties": ["Total Number of Penalties"],
}

EMPTY_ROWS = 0


def format_output_dictionaries(row, output_dict):
    """Formats the output dictionaries to match the expected output format"""

    output = {}
    for key, value in OUTPUT_COLUMN_NAMES.items():
        output[key] = ""
        for index, column in enumerate(value):
            if index == 0 or index == len(value) - 1:
                output[key] += f"{row[output_dict[column]]}"
            else:
                output[key] += f"{row[output_dict[column]]}, "
    return output


def get_index_dict_from_columns(columns):
    """Returns a dictionary with column headers as the keys and initial values of None"""

    index_dict = {}
    for column in columns:
        index_dict[column] = None
    return index_dict


def set_index_dict_from_headers(index_dict, headers, columns):
    """Sets the index of each column in the index_dict to the index of the column in the headers"""

    for column in columns:
        for header in headers:
            if column == header:
                index_dict[column] = headers.index(header)
    return index_dict


def validate_index_dict_update(index_dict, columns):
    """Validates that the index_dict was updated with the index of each column"""

    if None in index_dict.values():
        raise Exception(
            f"Error: Invalid CSV file. The columns in the CSV file do not match those expected.\n"
            f"Please ensure that the CSV file contains the following columns: {columns}"
        )


def get_valid_number(value, default):
    """Returns the value if it is a valid number, otherwise returns the default value"""

    return int(value) if value.isdigit() else default


def get_cell_val_dict(row, column_list, filter_dict):
    """Returns a dictionary with the column names as the keys and the cell values as the values"""

    cell_val_dict = {}
    for column in column_list:
        if column == "Provider State":
            cell_val_dict[column] = row[filter_dict[column]]
        elif column == "Overall Rating":
            cell_val_dict[column] = get_valid_number(row[filter_dict[column]], 1)
        else:
            cell_val_dict[column] = get_valid_number(row[filter_dict[column]], 0)
    return cell_val_dict


def cell_meets_filter_condition(key, cell_value):
    """Returns True if the cell value meets the filter condition, otherwise returns False"""

    if key == "Provider State":
        return cell_value == STATE
    elif key == "Overall Rating":
        return cell_value >= MIN_OVERALL_RATING
    elif key == "Number of Certified Beds":
        return cell_value >= MIN_NUM_BEDS
    elif key == "Rating Cycle 1 Total Number of Health Deficiencies":
        return cell_value <= MAX_NUM_DEFICIENCIES
    elif key == "Total Number of Penalties":
        return cell_value <= MAX_NUM_PENALTIES
    else:
        return False


def get_recommendation_score(csv_file_headers, row):
    score_index_dict = get_index_dict_from_columns(RECOMMEND_SCORE_COLUMN_DICT)
    score_index_dict = set_index_dict_from_headers(score_index_dict, csv_file_headers, RECOMMEND_SCORE_COLUMN_DICT)
    rec_score_col_data = get_column_data(row, score_index_dict)
    weighted_data = weight_rec_score_data(rec_score_col_data)
    weighted_sum = sum(weighted_data.values())
    return weighted_sum / 5


# Dictionary to store the index of each column to filter by
filter_dict = get_index_dict_from_columns(FILTER_COLUMNS)

# Dictionary to store index of each column to include in the output
output_dict = get_index_dict_from_columns(OUTPUT_COLUMNS)

# Begin CSV parsing
with codecs.open(FILE, "r", encoding="latin1") as csv_file:
    reader = csv.reader(csv_file, delimiter=",")
    csv_file_headers = next(reader)


    # Update the filter_dict with the index of each column to filter by
    filter_dict = set_index_dict_from_headers(
        filter_dict, csv_file_headers, FILTER_COLUMNS
    )

    # Throw error if any of the filter_columns were not found in the CSV
    validate_index_dict_update(filter_dict, FILTER_COLUMNS)

    # Update the output_dict with the index of each column to include in the output
    output_dict = set_index_dict_from_headers(
        output_dict, csv_file_headers, OUTPUT_COLUMNS
    )

    # Throw error if any of the output_columns were not found in the CSV
    validate_index_dict_update(output_dict, OUTPUT_COLUMNS)

    filtered_csv_data = []

    # Iterate through each row in the CSV file and filter the data
    for index, row in enumerate(reader):
        # Skip empty rows
        if len(row) == 0:
            EMPTY_ROWS += 1
            continue

        # Get cell values from the row for dictionary comparison
        cell_val_dict = get_cell_val_dict(row, FILTER_COLUMNS, filter_dict)

        valid_facility = True

        # Validate all filter conditions are met
        for key, value in cell_val_dict.items():
            if not cell_meets_filter_condition(key, value):
                valid_facility = False
                break

        if valid_facility:
            # Calculate the recommendation score
            score = get_recommendation_score(csv_file_headers, row)

            # Format the output dictionarie
            output = format_output_dictionaries(row, output_dict)

            # Add the recommendation score to the output dictionary
            output["Recommendation Score"] = score

            filtered_csv_data.append(output)

# Write the filtered data to a JSON file
with open(OUTPUT_FILE, "w") as json_file:
    json.dump(filtered_csv_data, json_file)


pprint.pprint(len(filtered_csv_data))
# pprint.pprint(filtered_csv_data[0])
print(f"Empty Rows: {EMPTY_ROWS}")
