import pprint


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


def get_column_data(row, index_dict):
    """Returns a dictionary with the column data from the row"""

    column_data = {}
    for column in RECOMMEND_SCORE_COLUMN_DICT:
        column_data[column] = row[index_dict[column]]
    return column_data


def weight_rec_score_data(rec_score_column_data):
    """Returns a dictionary with the cleaned data"""


    # Combine the number of certified beds and average number of residents per day
    num_beds = rec_score_column_data["Number of Certified Beds"]
    num_residents = rec_score_column_data["Average Number of Residents per Day"]

    # Make sure the data is a number
    num_beds = int(num_beds) if num_beds.isdigit() else -1
    num_residents = float(num_residents) if num_residents.isdigit() else -1

    # Calculate the number of beds available
    num_beds_available = int(num_beds) - float(num_residents)


    # Reduce variable names for readability
    overall_rating = rec_score_column_data["Overall Rating"]
    num_deficiencies = rec_score_column_data["Rating Cycle 1 Total Number of Health Deficiencies"]
    num_penalties = rec_score_column_data["Total Number of Penalties"]
    abuse = rec_score_column_data["Abuse Icon"]
    recent_health_inspection = rec_score_column_data["Most Recent Health Inspection More Than 2 Years Ago"]
    resident_family_council = rec_score_column_data["With a Resident and Family Council"]
    pt_hours_per_res = rec_score_column_data["Reported Physical Therapist Staffing Hours per Resident Per Day"]
    number_incidents = rec_score_column_data["Number of Facility Reported Incidents"]
    num_complaints = rec_score_column_data["Number of Substantiated Complaints"]



    # Weight data to be used in the recommendation score
    weighted_data = {
        "overall_rating": weight_overall_rating(overall_rating),
        "num_beds_available": weight_available_beds(num_beds_available),
        "num_deficiencies": weight_deficiencies(num_deficiencies),
        "num_penalties": weight_penalties(num_penalties),
        "abuse": weight_abuse(abuse),
        "recent_health_inspection": weight_inspection(recent_health_inspection),
        "resident_family_council": weight_council(resident_family_council),
        "pt_hours_per_res": weight_pt_per_res(pt_hours_per_res),
        "number_incidents": weight_incidents(number_incidents),
        "num_complaints": weight_complaints(num_complaints),
    }
    return weighted_data


# Important metric due to taking in many other metrics
def weight_overall_rating(overall_rating):
    """Returns the weighted overall rating"""

    overall_rating = int(overall_rating) if overall_rating.isdigit() else 0
    return overall_rating * 1.25


# Multiple factors to consider here
# Too many vacancies are likely not a good sign
# But also don't want to reccommend a facility that is too full
def weight_available_beds(num_available_beds):
    """Returns the weighted number of available beds"""

    if num_available_beds < 5 or num_available_beds > 50:
        return -1
    elif num_available_beds >= 5 and num_available_beds <= 50:
        return 1
    else:
        return 0


def weight_deficiencies(num_deficiencies):
    """Returns the weighted number of deficiencies"""

    num_deficiencies = int(num_deficiencies) if num_deficiencies.isdigit() else -1

    if num_deficiencies == 0:
        return 1
    elif num_deficiencies > 0 and num_deficiencies <= 5:
        return -0.25
    elif num_deficiencies > 5:
        return -1
    else:
        return 0


def weight_penalties(num_penalties):
    """Returns the weighted number of penalties"""

    num_penalties = int(num_penalties) if num_penalties.isdigit() else -1
    if num_penalties == 0:
        return 1
    elif num_penalties > 0 and num_penalties <= 5:
        return -0.25
    elif num_penalties > 5:
        return -1
    else:
        return 0


def weight_abuse(abuse):
    """Returns the weighted abuse value"""

    if abuse == "Y":
        return -1
    elif abuse == "N":
        return 1
    else:
        return 0


def weight_inspection(recent_health_inspection):
    """Returns the weighted recent health inspection value"""

    if recent_health_inspection == "Y":
        return 1
    elif recent_health_inspection == "N":
        return -1
    else:
        return 0


def weight_council(resident_family_council):
    """Returns the weighted resident family council value"""

    if resident_family_council == "Both":
        return 1
    elif resident_family_council == "Resident":
        return 0
    else:
        return 0


def weight_pt_per_res(pt_hours_per_res):
    """Returns the weighted physical therapist hours per resident value"""

    pt_hours_per_res = int(pt_hours_per_res) if pt_hours_per_res.isdigit() else -1
    if pt_hours_per_res > 0.09:
        return 1
    else:
        return 0
    


def weight_incidents(number_incidents):
    """Returns the weighted number of incidents"""

    number_incidents = int(number_incidents) if number_incidents.isdigit() else -1
    if number_incidents == 0:
        return 1
    elif number_incidents > 0 and number_incidents <= 5:
        return -0.25
    elif number_incidents > 5:
        return -1
    else:
        return 0


def weight_complaints(num_complaints):
    """Returns the weighted number of complaints"""

    num_complaints = int(num_complaints) if num_complaints.isdigit() else -1
    if num_complaints == 0:
        return 1
    elif num_complaints > 0 and num_complaints <= 5:
        return -0.25
    elif num_complaints > 5:
        return -1
    else:
        return 0

