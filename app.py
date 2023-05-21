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

# List of column names to use in the output
OUTPUT_COLUMN_NAMES = [
    "name",
    "address",
    "num_beds" "residents_per_day",
    "overall_rating",
    "num_deficiencies",
    "num_penalties",
]


def format_address(row, output_dict):
    """Formats the output address into a single string"""
    address = row[output_dict["Provider Address"]]
    city = row[output_dict["Provider City"]]
    state = row[output_dict["Provider State"]]
    zip_code = row[output_dict["Provider Zip Code"]]
    return f"{address}, {city}, {state} {zip_code}"


def format_output_dictionaries(row, output_dict):
    """Formats the output dictionaries to match the expected output format"""
    return {
        "name": row[output_dict["Provider Name"]],
        "address": format_address(row, output_dict),
        "num_beds": row[output_dict["Number of Certified Beds"]],
        "residents_per_day": row[output_dict["Average Number of Residents per Day"]],
        "overall_rating": row[output_dict["Overall Rating"]],
        "num_deficiencies": row[output_dict["Rating Cycle 1 Total Number of Health Deficiencies"]],
        "num_penalties": row[output_dict["Total Number of Penalties"]],
    }


def get_index_dict_from_columns(columns):
    """Returns a dictionary with column headers as the keys and initial values of None"""
    index_dict = {}
    for column in columns:
        index_dict[column] = None
    return index_dict


# Dictionary to store the index of each column to filter by
filter_dict = get_index_dict_from_columns(FILTER_COLUMNS)

# Dictionary to store index of each column to include in the output
output_dict = get_index_dict_from_columns(OUTPUT_COLUMNS)

# Begin CSV parsing
with codecs.open(FILE, "r", encoding="latin1") as csv_file:
    reader = csv.reader(csv_file, delimiter=",")
    csv_file_headers = next(reader)

    # Find and store the index of each column to filter by
    for filter_column in FILTER_COLUMNS:
        for header in csv_file_headers:
            if filter_column == header:
                filter_dict[filter_column] = csv_file_headers.index(header)

    # Check if all filter_columns were found in the CSV indicating that the file is valid
    if None in filter_dict.values():
        print(
            """Error: Invalid CSV file. The coumns in the CSV file do not match those expected.
              Please ensure that the CSV file contains the following columns:
              Provider State, Overall Rating, Number of Certified Beds, 
              Rating Cycle 1 Total Number of Health Deficiencies, Total Number of Penalties"""
        )
        sys.exit(1)

    # Find and store the index of each column to include in the output
    for output_column in OUTPUT_COLUMNS:
        for header in csv_file_headers:
            if output_column == header:
                output_dict[output_column] = csv_file_headers.index(header)

    # Check if all output_columns were found in the CSV indicating that the file is valid
    if None in output_dict.values():
        print(
            """Error: Invalid CSV file. The coumns in the CSV file do not match those expected.
            Please ensure that the CSV file contains the following columns:
            Provider Name, Provider Address, Provider City, Provider State, 
            Provider Zip Code, Number of Certified Beds, Average Number of Residents Per Day,
            Overall Rating, Rating Cycle 1 Total Number of Health Deficiencies, Total Number of Penalties"""
        )
        sys.exit(2)

    # Create a list to store rows of csv data
    filtered_csv_data = []

    # Iterate through each row in the CSV file and filter the data
    for index, row in enumerate(reader):
        # skip empty rows
        if len(row) == 0:
            continue

        # extract header indexs from the filter_dict
        state_header_index = filter_dict["Provider State"]
        overall_rating_header_index = filter_dict["Overall Rating"]
        num_beds_header_index = filter_dict["Number of Certified Beds"]
        num_deficiencies_header_index = filter_dict[
            "Rating Cycle 1 Total Number of Health Deficiencies"
        ]
        num_penalties_header_index = filter_dict["Total Number of Penalties"]

        # extract data to compare to command line arguments
        state = row[state_header_index]

        """convert csv string values to integers or floats if posisble otherwise set to default values
        TODO: consider proper values to set if string is not parsable this will effect weighting of the data
        """
        overall_rating = (
            int(row[overall_rating_header_index])
            if row[overall_rating_header_index].isdigit()
            else 1
        )
        num_beds = (
            int(row[num_beds_header_index])
            if row[num_beds_header_index].isdigit()
            else 0
        )
        num_deficiencies = (
            float(row[num_deficiencies_header_index])
            if row[num_deficiencies_header_index].isdigit()
            else 0
        )
        num_penalties = (
            float(row[num_penalties_header_index])
            if row[num_penalties_header_index].isdigit()
            else 0
        )

        # filter the data
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
