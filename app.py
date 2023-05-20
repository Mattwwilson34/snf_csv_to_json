import argparse

parser = argparse.ArgumentParser()

# add arguments
parser.add_argument(
    "state",
    help="Case insensitive US tate abbreviation to filter facilities by. This is a required argument.",
)
parser.add_argument(
    "num_facilities",
    nargs="?",
    default=20,
    type=int,
    help="The maximium number of facilities to be returned | Default: 20",
)
parser.add_argument(
    "min_overall_rating",
    nargs="?",
    choices=range(1, 6),
    default=1,
    type=int,
    metavar="min_overall_rating",
    help="The minimum quality rating required for each returned facility | Default: 1 | Accepted Range: {1,2,3,4,5}"
)
parser.add_argument(
    "num_beds",
    nargs="?",
    default=0,
    type=int,
    help="The minimum number of beds required for each returned facility | Default: 0",
)
parser.add_argument(
    "max_num_deficiencies",
    nargs="?",
    default=float("inf"),
    type=float,
    help="The maximum number of deficiencies allowed for each returned facility | Default: infinity",
)

parser.add_argument(
    "max_number_penalties",
    nargs="?",
    default=float("inf"),
    type=float,
    help="The maximum number of penalties allowed for each returned facility | Default: infinity",
)

# parse the arguments
args = parser.parse_args()

# Assign the arguments to constant variables
STATE = args.state
NUM_FACILITIES = args.num_facilities
MIN_OVERALL_RATING = args.min_overall_rating
NUM_BEDS = args.num_beds
MAX_NUM_DEFICIENCIES = args.max_num_deficiencies
MAX_NUM_PENALTIES = args.max_number_penalties
