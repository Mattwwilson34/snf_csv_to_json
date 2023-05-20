import argparse
import csv
import codecs
import sys

parser = argparse.ArgumentParser(
    description="Filter nursing home facilities by state and other criteria.",
    formatter_class=argparse.RawTextHelpFormatter,
)

# Add arguments
parser.add_argument(
    "file",
    help="A required argument specifying the path to the file containing the nursing home data.",
)

parser.add_argument(
    "state",
    help="A required case insensitive argument specifying the state to filter facilities by.",
)
parser.add_argument(
    "num_facilities",
    nargs="?",
    default=20,
    type=int,
    help="An optional argument specifying the number of facilities to return\n"
    "Default: 20",
)
parser.add_argument(
    "min_overall_rating",
    nargs="?",
    choices=range(1, 6),
    default=1,
    type=int,
    metavar="min_overall_rating",
    help="The minimum quality rating required for each returned facility.\n"
    "Default: 1\n"
    "Range: {1,2,3,4,5}",
)
parser.add_argument(
    "num_beds",
    nargs="?",
    default=0,
    type=int,
    help="The minimum number of beds required for each returned facility.\n"
    "Default: 0",
)
parser.add_argument(
    "max_num_deficiencies",
    nargs="?",
    default=float("inf"),
    type=float,
    help="The maximum number of deficiencies allowed for each returned facility.\n"
    "Default: infinity",
)

parser.add_argument(
    "max_number_penalties",
    nargs="?",
    default=float("inf"),
    type=float,
    help="The maximum number of penalties allowed for each returned facility.\n"
    "Default: infinity\n",
)

# Parse arguments
args = parser.parse_args()

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

# Dictionary to store the index of each column to filter by
filter_dict = {}
for column in FILTER_COLUMNS:
    filter_dict[column] = None


# Begin CSV parsing
with codecs.open(FILE, "r", encoding="latin1") as csv_file:
    reader = csv.reader(csv_file, delimiter=",")
    csv_file_headers = next(reader)

    # Find the index of each column to filter by
    for filter_column in FILTER_COLUMNS:
        for header in csv_file_headers:
            if filter_column == header:
                # store the index in the filter map
                filter_dict[filter_column] = csv_file_headers.index(header)

    # Check if all filter_columns were found in the CSV indicating that the file is valid
    if None in filter_dict.values():
        print(
            """Error: Invalid CSV file. The coumns in the CSV file do not match those expected.
              Please ensure that the CSV file contains the following columns:
              Provider State, Overall Rating, Number of Certified Beds, Rating Cycle 1 Total Number of Health Deficiencies, Total Number of Penalties"""
        )
        sys.exit(1)

    # Create a list to store rows of csv data
    filtered_csv_data = []
    # Add the headers to the list
    filtered_csv_data.append(csv_file_headers)

    # Iterate through each row in the CSV file and filter the data
    for index, row in enumerate(reader):
        # skip empty rows
        if len(row) == 0:
            continue

        # extract index header indexs from the filter_dict
        state_header_index = filter_dict["Provider State"]
        overall_rating_header_index = filter_dict["Overall Rating"]
        num_beds_header_index = filter_dict["Number of Certified Beds"]
        num_deficiencies_header_index = filter_dict[
            "Rating Cycle 1 Total Number of Health Deficiencies"
        ]
        num_penalties_header_index = filter_dict["Total Number of Penalties"]

        # extract data to compare to command line arguments
        state = row[state_header_index]

        # convert to csv string values to int if posisble else set to 0
        # TODO: consider proper values to set if string is not parsable this will effect weighting of the data
        overall_rating = int(row[overall_rating_header_index]) if row[overall_rating_header_index].isdigit() else 0
        num_beds = int(row[num_beds_header_index]) if row[num_beds_header_index].isdigit() else 0
        num_deficiencies = int(row[num_deficiencies_header_index]) if row[num_deficiencies_header_index].isdigit() else 0
        num_penalties = int(row[num_penalties_header_index]) if row[num_penalties_header_index].isdigit() else 0

        # filter the data
        if (
            state == STATE
            and overall_rating >= MIN_OVERALL_RATING
            and num_beds >= MIN_NUM_BEDS
            and num_deficiencies <= MAX_NUM_DEFICIENCIES
            and num_penalties <= MAX_NUM_PENALTIES
        ):
            filtered_csv_data.append(row)


print(len(filtered_csv_data))
print(filter_dict)
