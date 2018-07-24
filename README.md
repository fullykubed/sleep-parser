# Installation

All of the logic is contained within ``Parser.py``. It can either be downloaded directly from https://github.com/jclangst/sleep-parser
or cloned via ``git clone https://github.com/jclangst/sleep-parser.git`` if you are familiar with git.

It has a single dependency, `numpy` that can be installed by running:

`pip install numpy`

or

`python -m pip install numpy` (if the above does not work)

# Running

Execute the file from a bash shell (terminal) as such:

``python Parser.py [args]``

Running with `-h` or `--help` will show you the supported arguments and their functionality.

As an example, if you wanted to extract the data ranging from
`2018-03-29 20:23:29` to `2018-03-29 20:30:09` from `input.csv` to `output.csv`,
you would run the following:

``python Parser.py 1522369409 1522369809 test.csv -o output.csv``

For additional syntax and functionality, see the help command.

# Input and Output Format

### Input
The input file is expected to have the following parameters:

(1) The data is contained in a csv file in a single column;

(2) The first row contains the unix timestamp indicating the start of the data;

(3) The second row contains the sampling frequency in Hz;

(4) All subsequent rows contain the sampled data with the third row being the datum sampled
at the timestamp from row one.

### Output

The output file will have the following format:

(1) The data will be contained in a csv file in a single column;

(2) The first row contains the unix timestamp indicating the **start of the *extracted* data**;

(3) The second row contains the sampling frequency in Hz;

(4) All subsequent rows contain the sampled data with the third row being the datum sampled
at the timestamp from row one.
