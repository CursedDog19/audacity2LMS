"""
Written by Ethan Ingalls
Adapted from a script by John Storms
ethaningalls22@gmail.com
ver. 1.0

Use: Translates Audacity polyphonic labels into LOR effects and timings.
Directions:
- Enter all filenames without file extensions (.txt, .lms)
- First enter the name of a blank sequence file
- Then enter the name of the Audacity labels file
"""

import xml.etree.ElementTree as ET

def get_timings(labels):
    """Return a sorted list of timings without duplicates."""
    output = []
    for dt in labels:
        if dt[1] not in output:
            output.append(dt[1])
        if dt[2] not in output:
            output.append(dt[2])
    output.sort()
    return output

def centi(timing):
    """Converts decimal seconds to deciseconds."""
    timing = 100 * float(timing)
    # Adds .1 to the value, then chopps off extraneous digits. Seems to work.
    timing += .1
    return int(timing)

def write_timings(timings):
    """Adds timings to an existing lms tree."""
    existing_grids = len(list(root[1]))
    ET.SubElement(root[1], 'timingGrid', saveID="0", name="PyPoly", type="freeform")   
    for i in timings:
        ET.SubElement(root[1][existing_grids],'timing', centisecond=str(i))

def extract(polyfile):
    """Outputs a list of dictionaries containing tag data."""
    output = []
    # Read file.
    with open(polyfile) as f_obj:
        lines = f_obj.readlines()
    # Convert to centiseconds, format and sort dictionaries.
    for line in lines:
        dt = []
        vals = line.split()
        dt.append(int(float(vals[2])))
        dt.append(centi(vals[0]))
        dt.append(centi(vals[1]))
        output.append(dt)
    return output

def write_channels(ch_list):
    """Write all channels on a new track."""
    length = get_total_len()
    # Format channels and tracks.
    for i in root[2][0][0].iter('channel'):
        root[2][0][0].remove(i)
    for i in root[0].iter('channel'):
        root[0].remove(i)
    # Format track and channel entries.
    for i in range(128):
        ET.SubElement(root[0], 'channel', name=ch_list[i], color="202",
            centiseconds=length, savedIndex=str(i))
        ET.SubElement(root[2][0][0],'channel', savedIndex=str(i))
    
def write_effects(labels):
    """Write effects to their appropriate channels."""
    for effect in labels:
        ET.SubElement(root[0][effect[0]], 'effect', type="intensity",
            startCentisecond=str(effect[1]), endCentisecond=str(effect[2]),
            startIntensity="100", endIntensity="0")

def get_total_len():
    """Return the total length of the sequence in centiseconds."""
    track = root[2][0].attrib
    length = track['totalCentiseconds']
    return length


midi_list = ['C', 'C#-Db', 'D', 'D#-Eb', 'E', 'F', 'F#-Gb', 'G', 'G#-Ab', 'A', 'A#-Bb', 'B', 'C', 'C#-Db', 'D', 'D#-Eb', 'E', 'F', 'F#-Gb', 'G', 'G#-Ab', 'A', 'A#-Bb', 'B', 'C', 'C#-Db', 'D', 'D#-Eb', 'E', 'F', 'F#-Gb', 'Low_G', 'Low_G#-Ab', 'Low_A', 'Low_A#-Bb', 'Low_B', 'Low_C', 'Low_C#-Db', 'Low_D', 'Low_D#-Eb', 'Low_E', 'Low_F', 'Low_F#-Gb', 'Bass_G', 'Bass_G#-Ab', 'Bass_A', 'Bass_A#-Bb', 'Bass_B', 'Bass_C', 'Bass_C#-Db', 'Bass_D', 'Bass_D#-Eb', 'Bass_E', 'Bass_F', 'Bass_F#-Gb', 'Middle_G', 'Middle_G#-Ab', 'Middle_A', 'Middle_A#-Bb', 'Middle_B', 'Middle_C', 'Middle_C#-Db', 'Middle_D', 'Middle_D#-Eb', 'Middle_E', 'Middle_F', 'Treble_F#-Gb', 'Treble_G', 'Treble_G#-Ab', 'Treble_A', 'Treble_A#-Bb', 'Treble_B', 'Treble_C', 'Treble_C#-Db', 'Treble_D', 'Treble_D#-Eb', 'Treble_E', 'Treble_F', 'High_F#-Gb', 'High_G', 'High_G#-Ab', 'High_A', 'High_A#-Bb', 'High_B', 'High_C', 'High_C#-Db', 'High_D', 'High_D#-Eb', 'High_E', 'High_F', 'F#-Gb', 'G', 'G#-Ab', 'A', 'A#-Bb', 'B', 'C', 'C#-Db', 'D', 'D#-Eb', 'E', 'F', 'F#-Gb', 'G', 'G#-Ab', 'A', 'A#-Bb', 'B', 'C', 'C#-Db', 'D', 'D#-Eb', 'E', 'F', 'F#-Gb', 'G', 'G#-Ab', 'A', 'A#-Bb', 'B', 'C', 'C#-Db', 'D', 'D#-Eb', 'E', 'F', 'F#-Gb', 'G']
# User input.
existing = input("Existing LOR filename:  ")
audacity = input("Audacity filename:  ")

# Parse base XML file.
tree = ET.parse(str(existing)+".lms")
root = tree.getroot()
# Import labels from an Audacity polyphonic file.
labels = extract(str(audacity)+".txt")
print("\nFormatting timings...")
timings = get_timings(labels)
write_timings(timings)
print("Generating effects...")
write_channels(midi_list)
write_effects(labels)

# Save to new file.
tree.write(str(existing)+"_POLYPHONIC.lms")
print("Done!")








