import csv
import codecs
import pprint
from arg_parse import parse_arguments

# Parse command line arguments
args = parse_arguments()

# Assign the arguments to constant variables
FILE = args.file
STATE = args.state.upper()
NUM_FACILITIES = args.num_facilities
MIN_OVERALL_RATING = args.min_overall_rating
MIN_NUM_BEDS = args.num_beds
MAX_NUM_DEFICIENCIES = args.max_num_deficiencies
MAX_NUM_PENALTIES = args.max_number_penalties

# List of columns to filter dataset by
FILTER_COLUMNS = [
    "Provider State",
    "Overall Rating",
    "Number of Certified Beds",
    "Rating Cycle 1 Total Number of Health Deficiencies",
    "Total Number of Penalties",
]

# List of columns to include in the output
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

# Dictionary used to format the output
# Output will be a list of dictionaries
# Each dictionary will represent a facility
# Each key in this dictionary will represent a key in the output dictionary
# Each value array will represent the columns in the CSV file that will be concatenated into a single string
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

        # Get cell values from the row for command line args comparison
        state = row[filter_dict["Provider State"]]
        overall_rating = get_valid_number(row[filter_dict["Overall Rating"]], 1)
        num_beds = get_valid_number(row[filter_dict["Number of Certified Beds"]], 0)
        num_deficiencies = get_valid_number(
            row[filter_dict["Rating Cycle 1 Total Number of Health Deficiencies"]], 0
        )
        num_penalties = get_valid_number(
            row[filter_dict["Total Number of Penalties"]], 0
        )

        # Validate that the row meets the filter criteria
        if (
            state == STATE
            and overall_rating >= MIN_OVERALL_RATING
            and num_beds >= MIN_NUM_BEDS
            and num_deficiencies <= MAX_NUM_DEFICIENCIES
            and num_penalties <= MAX_NUM_PENALTIES
        ):
            # format the filtered data into a dictionary with expected output format
            filtered_csv_data.append(format_output_dictionaries(row, output_dict))

pprint.pprint(len(filtered_csv_data))
pprint.pprint(filtered_csv_data[0])
print(f"Empty Rows: {EMPTY_ROWS}")
