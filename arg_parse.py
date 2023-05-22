#!/usr/bin/env python

import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Filter nursing home facilities by state and other criteria.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Add arguments
    # Required arguments
    parser.add_argument(
        "--input_file",
        required=True,
        help="A required argument specifying the path to the file containing the nursing home data.",
    )

    parser.add_argument(
        "--state",
        required=True,
        help="A required case insensitive argument specifying the state to filter facilities by.",
    )

    # Optional arguments
    parser.add_argument(
        "--output_file",
        default="output.json",
        help="An optional argument specifying the path to the file to output the results to.\n"
        "Default: output.json",
    )

    parser.add_argument(
        "--num_facilities",
        default=20,
        type=int,
        help="An optional argument specifying the number of facilities to return\n"
        "Default: 20",
    )

    parser.add_argument(
        "--min_rating",
        choices=range(1, 6),
        default=1,
        type=int,
        help="The minimum quality rating required for each returned facility.\n"
        "Default: 1\n"
        "Range: {1,2,3,4,5}",
    )

    parser.add_argument(
        "--num_beds",
        default=0,
        type=int,
        help="The minimum number of beds required for each returned facility.\n"
        "Default: 0",
    )

    parser.add_argument(
        "--max_deficiencies",
        default=float("inf"),
        type=float,
        help="The maximum number of deficiencies allowed for each returned facility.\n"
        "Default: infinity",
    )

    parser.add_argument(
        "--max_penalties",
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
