"""
badge_utils.py: utility functions for badge printer input
"""
import codecs

def fsplit(line, N):
    """Parse a line from a CSV file and return the fields it contains
       ensuring that the whole line is consumed or raising an AssertionError exception."""
    pos = 0
    fields = []
    for _ in range(N):
        if line[pos] == '"':
            start = pos
            end = line.find('"', pos+1)
            while end+1<len(line) and line[end+1] == '"':
                pos = end+1
                end = line.find('"', pos+1)
            field = line[start+1:end].replace('""', '"')
            pos = end+2
        else:
            end = line.find(',', pos)
            field = line[pos:end]
            pos = end+1
        fields.append(field)
    if len(line) != pos:
        print("***", line)
        print("Pos:", pos, "Remaining:", line[pos:])
    assert pos == len(line) # sanity check
    return fields

def evb_reader(filename, fields, encoding):
    """Yields sucessive data sets from an Eventbrite delegate summary."""
    f = codecs.open(filename, "r", encoding)
    for line in f:
        cols=fsplit(line, 27)
        yield tuple(cols[n] for n in fields)

def csv_reader(filename, encoding):
    """Yields successive data sets from a CSV file."""
    f = codecs.open(filename, "Ur", encoding)
    for line in f:
        if line.startswith("#"):
            continue
        cols = line[:-1].split(",")
        yield tuple(cols+["manual"])

def blanks(N):
    """Yields blank tickets to allow blank labels to be printed."""
    for i in range(N):
        yield ("", "", "", "", "")
