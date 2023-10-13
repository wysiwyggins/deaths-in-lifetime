# Deaths Analysis in GEDCOM Files

This script analyzes **GEDCOM** (Genealogical Data Communication) files to extract information about individuals and, more specifically, details about their deaths. The tool offers two main search options:

Search by a person's name: The user can enter the full name of an individual and retrieve their birth and death dates.
Search by date range: The user can input a date range, and the script will retrieve all the individuals from the GEDCOM file who died within that range.

## Features

User-friendly file browser selection for GEDCOM file input.
Handling of multiple date formats, including unconventional ones.
Outputs the name and death date of individuals based on user criteria.
Error handling for invalid date formats, ensuring that years that look valid are extracted and considered.

## Prerequisites

Python (preferably version 3.7 or higher).
`tkinter` library for the file browser (usually comes with standard Python installations).

## How to Run

1. Ensure that you have Python and `tkinter` installed.
2. avigate to the directory containing the deaths_analysis.py script.
3. Run the script using the following command:

```python deaths_analysis.py```

3. Use the file browser to select your GEDCOM file.
4. Follow the on-screen instructions to select your search criteria (either by person's name or date range).

## Known Limitations

- The script primarily focuses on extracting and analyzing the `NAME`, `BIRT`, and `DEAT` tags from the GEDCOM file.
- The tool assumes the GEDCOM file is correctly structured and may not handle corrupt or non-standard files gracefully.

## Contributing

This script is provided as an educational example for working with the sometimes hairy GEDCOM format. GEDCOM is typically produced and exported from big Genealogy websites like Ancestry.com, and is often very dirty. Some open source cleaning tools are available, such as [Gramps](https://gramps-project.org). Fork as desired.

## License

GEDCOM is a contentious technology, developed by the Church of Latter Day Saints in the 1980's and the format of the material-of-value in the recent purchase of Ancestry.com by the world's largest private equity firm Blackstone, this software is provided under the [Anti-Capitalist Software License](https://anticapitalist.software) to prohibit its use for any number of unsavory ventures.
