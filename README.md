# Python Program Readme

This is a Python program that filters data from a CSV file based on specified conditions and outputs the filtered results in JSON format. The program takes command line arguments to customize the filtering criteria and output file location.

## Prerequisites

- Python 3.10
- The following Python modules:
  - csv
  - codecs
  - pprint
  - json
  - arg_parse
  - rec_score_analytic

## Usage

1. Ensure you have the necessary Python dependencies installed.
2. Save the CSV file that you want to filter in the same directory as the Python program.
3. Open a terminal or command prompt and navigate to the directory where the Python program is saved.
4. Run the program using the following command:

```shell
python app.py --input_file input.csv --state PA --output_file output.json --num_facilities 20 --min_rating 5 --num_beds 0 --max_deficiencies 50 --max_penalties 50
```

5. The only required command line arguments are `--input_file` and `--state`.
6. All other argumnets are optional and have predefined default which are outlined below.
7. The program will filter the CSV data based on the specified conditions and output the results in the JSON file provided via `--output_file` or the default `output.json` in the same directory as the program.

## Command Line Arguments

The program accepts the following command line arguments:

_Help:_

- `-h` or `--help` Will bring up a detailed usage prompt.

_Required:_

- `--file`: Specifies the input CSV file name.
- `--state`: Filters by the provider state (e.g., "NY" for New York).

_Optional:_

- `--output_file`: Specifies the output JSON file name.
- `--num_facilities`: Limits the number of facilities to include in the output.
- `--min_rating`: Filters by the minimum overall rating of facilities.
- `--num_beds`: Filters by the minimum number of certified beds.
- `--max_deficiencies`: Filters by the maximum number of health deficiencies.
- `--max_penalties`: Filters by the maximum number of penalties.

## Output

The program generates an output file in JSON format named `output.json`, unless a different name is specified via command line arguments, that contains the filtered data from the input CSV file. The output file will include the following columns:

- Name of Facility
- Address of Facility
- Number of Certified Beds
- Average Number of Residents per Day
- Overall Rating
- Total Number of Health Deficiencies
- Total Number of Penalties
- Recommendation Score

Each facility's data is represented as a dictionary in the output JSON file.

## Recommendation Score Analytic

A feature of this program is that it generates a reccomendation score for each facility. The reccomendation score is calculated using multiple data points from each facility.

The data points chosen for the recommedation analytic were:

- Overall Rating
- Number of Certified Beds
- Average Number of Residents per Day"
- Rating Cycle 1 Total Number of Health Deficiencies"
- Total Number of Penalties"
- Abuse Icon"
- Most Recent Health Inspection More Than 2 Years Ago"
- With a Resident and Family Council"
- Reported Physical Therapist Staffing Hours per Resident Per Day"
- Number of Facility Reported Incidents"
- Number of Substantiated Complaints"

### Overall Rating:

      The CMS (Centers for Medicare & Medicaid Services) nursing home metric overall rating is a measure used to assess the quality of care provided by nursing homes in the United States. The rating is based on individual metrics including health inspections, staffing, and quality measures.

This rating is recognizes within the clinical community for being good, but not great which gives the rating value, but we must make sure not to overweight is.

#### weighting:

`n = overall rating in range of {1,2,3,4,5}`

- n = 1
  - weight of 0.25
- n = 2
  - weight of 0.50
- n = 3
  - weight of 0.75
- n = 4
  - weight of 1.00
- n = 5
  - weight of 1.25

### Number of Beds

The number of beds metric is calculated by taking the difference of
`Number of Certified Beds` and `Average Number of Residents per Day`. This metric is important because it tells use how many beds are currently available for potential residents. There are mutiple factors that are considered in the weighting of this value.

#### weighting:

`n = num of available beds`

- Too few beds (n < 5):
  - If there are not enough beds for incoming residents then a negative weight is given to lower its reccomendation score.
- Too many beds (n > 50):
  - If there are too many open beds, this could suggest that the facility is not desirable thus a negative weight is given for this metric.
- Sweet spot (5 > n < 50):
  - any facilities that fall between our too few and too many catagories will have a positive weight applied to their score.

### Rating Cycle 1 Total Number of Health Deficiencies

      This metric is a specific measure used by CMS to assess the quality of care provided by nursing homes in the United States. It is one of the components that contributes to the health inspection rating of a nursing home.

The total number of health deficiencies is an important metric because it provides an indication of the nursing home's compliance with regulatory standards. The lower the number of deficiencies found during the inspection, the better the nursing home's performance in meeting those standards.

It is unclear based on my research if this score is included in the `overall_rating` metric discussed earlier and if so how much weight it is given, but by including it in our reccomedation analytic I am making sure that it is accounted for in our reccomendation.

#### weighting:

`n = num_health_deficiencies`

- n = 0
  - A weight of 1 is applied
- 0 < n < 5
  - A weight of 0.25 is applied
- n > 5
  - A weight of -1 is applied

### Total Number of Penalties

      This metric provides an indication of the nursing home's regulatory compliance history. A higher number of penalties suggests a higher frequency of deficiencies or violations identified in the past. This metric serves as a signal to potential residents and their families about the nursing home's track record and its commitment to meeting quality standards.

#### weighting:

`n = num_penalties_deficiencies`

- n = 0
  - A weight of 1 is applied
- 0 < n < 5
  - A weight of 0.25 is applied
- n > 5
  - A weight of -1 is applied

### Abuse Icon

      The abuse icon is applied when a nursing home has been cited for abuse, neglect, or exploitation during a standard survey conducted by the state or federal survey agencies. The citations can be related to various forms of mistreatment, such as physical abuse, verbal abuse, sexual abuse, emotional abuse, or neglectful care that results in harm to a resident.

Given the serverity of a present abuse Icon I chose to weight the presence of one heavier than other metrics to ensure these facilities very unlikely to be recommended. The values for this metric in the dataset are `Y` for yes or present icon and `N` for no or icon is not present.

Given the infrequency of this icon being present in the dataset I chose to not weight the abscence of the icon.

#### weighting:

`n = Y or N`

- n = Y
  - A weight of -3
- n = N
  - A weight of 0

### Most Recent Health Inspection More Than 2 Years Ago

      The "recent health inspection within the past 2 years" metric serves as an indicator of how up-to-date the nursing home's inspection information is. It signifies whether the facility has been evaluated relatively recently, giving potential residents and their families a sense of the nursing home's regulatory compliance and the timeliness of information available.

The values for this metric in the dataset are `Y` for yes and `N` for no.

#### weighting:

`n = Y or N`

- n = Y
  - A weight of 1
- n = N
  - A weight of -1

### With a resident family council

      The nursing home Resident Family Council metric refers to an assessment or measurement related to the presence and functioning of a Resident Family Council within a nursing home. A Resident Family Council is a formalized group or organization comprised of family members and friends of residents living in a nursing home. Its purpose is to provide support, advocacy, and a platform for communication between the facility's administration and residents' families.

The Resident Family Council metric aims to ensure that families have a voice and are actively engaged in the care and well-being of their loved ones residing in nursing homes. It underscores the importance of collaboration and communication between the facility and residents' families to create a supportive and person-centered care environment thus I chose to include this metric in the score analytic.

The values for this metric in the dataset are `Both` meaning the both residents and family councils are involved `Resident` for only resident and not family councils are involved

#### weighting:

`n = Both or Resident`

- n = Both
  - A weight of 1
- n = N
  - A weight of 0

### Reported PT Staffing Hours per Resident Per Day

      Physical therapy is a crucial aspect of care in nursing homes, particularly for individuals who require rehabilitation or have mobility issues. Physical therapists help residents improve their strength, balance, mobility, and overall functional abilities through targeted exercises and therapies.

Higher reported physical therapist staffing hours per resident per day indicate that nursing homes have more dedicated resources for providing physical therapy services. It suggests that residents have greater access to physical therapy and are likely to receive more personalized and frequent sessions to address their specific needs.

To determine the reported physical therapist staffing hours per resident per day, nursing homes track and report the number of hours their physical therapists spend providing care specifically to residents on a daily basis. This data is then averaged to provide an average number of hours per resident per day.

I given the infrequency of facilities reaching the 0.09 marker I chose to not penalize them for being lower, but reward them for being higher.

#### weighting:

`n = avg(PT hours of care per pt per day)

- n > 0.09
  - A weight of 1
- n < 0.09
  - A weight of 0

### Number of Facility Reported Incidents

    This metric refers to the count of incidents or adverse events that have occurred within a nursing home and have been reported by the facility itself. It is a measure used to assess the occurrence and frequency of incidents or adverse events that may impact resident health, safety, or well-being.

Analyzing the number of facility reported incidents provides an indication of the overall safety and risk management practices within the nursing home. A higher number of reported incidents may suggest a greater need for interventions, staff training, or policy revisions to prevent future occurrences and ensure resident safety.

#### weighting:

`n = number of reported incidents

- `n = 0`
  - A weight of 1
- `0 > n < 5`
  - A weight of -0.25
- `n > 5`
  - A weight of -1

### Number of Substantiated Complaints

    This metric refers to the count of complaints lodged against a nursing home that have been investigated and determined to be valid or substantiated. It is a measure used to assess the occurrence and validity of complaints made by residents, their families, or other individuals regarding the care, services, or conditions within the nursing home.

The number of substantiated complaints provides an indication of the nursing home's responsiveness to resident concerns, the effectiveness of its complaint resolution processes, and potential areas of improvement. A higher number of substantiated complaints may suggest recurring issues or deficiencies within the facility that require attention and corrective action.

#### weighting:

`n = number of substantiated complaints

- `n = 0`
  - A weight of 1
- `0 > n < 5`
  - A weight of -0.25
- `n > 5`
  - A weight of -1

## Additional Notes

- The program expects the input CSV file to have headers that match the specified column names.
- Empty rows in the CSV file will be skipped during the filtering process and tracked in the program's output.
- The program uses external Python modules such as `arg_parse` and `rec_score_analytic`. Make sure these modules are installed or available in the Python environment where you run the program.

Please ensure that your system meets the requirements and follow the usage instructions to run the program successfully.
