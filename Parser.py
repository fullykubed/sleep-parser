import numpy as np
import argparse
from datetime import datetime
from pathlib import Path

if __name__ == "__main__":

    #Parser configuration
    parser = argparse.ArgumentParser()
    parser.add_argument("start", help="unix timestamp of the first recording to extract (e.g., 1522369409)", type=int)
    parser.add_argument("end", help="unix timestamp of the first recording to extract (e.g., 1522369409)", type=int)
    parser.add_argument("input_file", help="path to file to read raw data from (e.g., 'input.csv')")
    parser.add_argument("-o", "--output", help="path to save extracted data (e.g., 'output.csv')")
    parser.add_argument("-v", "--verbose", help="toggle to show intermediate information", action='store_true')
    parser.add_argument("-f", "--force", help="overwrite the output file if it exists", action='store_true')
    args = parser.parse_args()

    START_TIME = args.start
    END_TIME = args.end
    FILE_NAME = Path(args.input_file)
    OUT_FILE_NAME = Path(args.output) if args.output else FILE_NAME.parent.joinpath(FILE_NAME.name.split(".")[0] + "-out.csv")

    #Filename checks
    if(not FILE_NAME.is_file()):
        print("Error: '",FILE_NAME,"' does not exist!")
        exit(1)
    if(OUT_FILE_NAME.exists() and not args.force):
        print("Error: '", OUT_FILE_NAME, "' already exists! Use -f to override.")
        exit(1)

    #Read data from the input file
    raw = np.loadtxt(FILE_NAME)
    first_time = raw[0]
    frequency = raw[1]
    data = raw[2:]
    last_time = raw[0] + (len(data) * 1/frequency)

    #Data input checks
    if(START_TIME < first_time):
        print("Error: Beginning of selected range (", datetime.fromtimestamp(START_TIME), ") is before the start of the",
              " data (", datetime.fromtimestamp(first_time), ")!")
        exit(1)
    if(END_TIME > last_time):
        print("Error: End of selected range (", datetime.fromtimestamp(END_TIME), ") is before the start of the",
              " data (", datetime.fromtimestamp(last_time), ")!")
        exit(1)
    if(START_TIME >= END_TIME):
        print("Error: Beginning of selected range (", datetime.fromtimestamp(START_TIME), ") is the same or after the end of the",
              " selected range (", datetime.fromtimestamp(END_TIME), ")!")
        exit(1)


    #Print some summary information
    if(args.verbose):
        print("First Sample Collected At:",datetime.fromtimestamp(first_time))
        print("Last Sample Collected At:", datetime.fromtimestamp(last_time))
        print("Number of Samples:", len(data))
        print()

        print("Extracting Range\nFrom:", datetime.fromtimestamp(START_TIME))
        print("TO:", datetime.fromtimestamp(END_TIME))


    #Extract the interesting data
    times = np.arange(first_time, last_time, 1/frequency)
    times_in_range = np.all([times >= START_TIME, times < END_TIME], axis=0)
    extracted_data = data[times_in_range]

    #save data
    to_save = np.append([START_TIME, frequency], [extracted_data])
    np.savetxt(OUT_FILE_NAME, to_save, fmt="%3.6f")

    if(args.verbose):
        print("\nDone! Extracted to:", OUT_FILE_NAME)