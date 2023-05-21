import argparse


def parse_arguments():
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

    # Validate arguments
    def validate_two_alpha_chars(value):
        """Validates that the state argument is a 2-character alphabetic input"""

        if len(value) != 2 or not value.isalpha():
            raise argparse.ArgumentTypeError(
                f"'{value}' is not a valid 2-character alphabetic input"
            )

        return value


    validate_two_alpha_chars(args.state)

    return args

