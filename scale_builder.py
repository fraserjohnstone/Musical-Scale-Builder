"""
This application allows the user to type in a musical scale and be shown all of the notes involved.

The user input is converted to lowercase as soon as is read so all of the strings we deal with until we display the
scale to the user are lowercase.

Throughout the code the following definitions are used:

  - mode:      An arrangement of tones and semi-tones. Major and Minor are 2 commonly used modes, but there are many 
               others. A mode is more commonly but not always correctly referred to as a scale.
  - root:      The tonic (first degree) of a scale.
  - modifier:  Musical sharp or flat symbol. For example F# (read as 'F sharp') has the root F and modifier sharp.
               in code sharps and flats will be represented by '+', and '-' respectively.
  
In short this algorithm works by altering the standard Major mode (also called Ionian mode). Any mode can be represented 
as a modification of the Major that shares the same root note. For example the Aeolian mode with the root note A can 
be represented as degrees 1, 2, flat 3, 4, 5, flat 6, flat 7, and 8 of the A Major.

In the definitions module we have a dictionary of major scales (one for each root), and a dictionary of mode definitions
(including the degrees of the major scale included, and any modifier). We use these together to build the desired mode.
  
For usage instructions please see the README file.
"""
import os
import re

import definitions


def show_instructions():
    """
    Displays a short message to the user letting them know how to use the application.
    """
    msg = """Instructions:

        Simply type in the scale you would like in the form 'root-note mode-type'. For example:
        
          - 'C Major'                     (shows: C, D, E, F, G, A, B, C)
          - 'F Sharp Harmonic Minor'      (shows: F#, G#, A, B, C#, D, E#, F#)
          - 'G Lydian'                    (shows: G, A, B, C#, D, E, F#, G) 
          - 'B Flat Major'                (shows: Bb, C, D, Eb, F, G, A, Bb)
          - 'C Sharp Melodic Minor'       (shows: C#, D#, E, F#, G#, A#, B#, C#, B, A, G#, F#, E, D#, C#)
          
        Type 'Show Modes' to see a complete list of available modes.
        
        To exit the application enter '-1'"""
    print(msg)
    print_divider()


def show_possible_modes():
    """
    Displays a message to the user showing all of the possible modes that are here to choose from.
    """
    # clear the screen first
    os.system('cls')
    msg = """Possible Modes:

        1.Acoustic           2.Aeolian            3.Algerian           4.Altered
        5.Augmented          6.Bebop dominant     7.Blues              8.Chromatic
        9.Dorian             10.Double Harmonic   11.Enigmatic         12.Flamenco
        13.Gypsy             14.Half Diminished   15.Harmonic Major    16.Harmonic Minor
        17.Hungarian         18.Insen             19.Ionian            20.Istrian
        21.Iwato             22.Locrian           23.Lydian Augmented  24.Lydian
        25.Major             26.Major Bebop       27.Major Locrian     28.Major Pentatonic
        29.Melodic Minor     30.Minor Pentatonic  31.Mixolydian        32.Melodic Minor
        33.Neapolitan Major  34.Neapolitan Minor  35.Persian           36.Phrygian Dominant
        37.Phrygian          38.Prometheus        39.Tritone           40.Wholetone"""

    print(msg)
    print_divider()


def validate_user_input(user_input):
    """    
    Checks that the user has entered a valid scale. The input should be of the form 'root-note mode-type'.
    
    In the above format, root-note must take the form:
      
      - one single letter, a-g, followed by a space and optionally the word 'flat' or 'sharp'. This is not case sensitive.
          
    If the input validates then we extract the root, any possible modifier, and mode as three separate variables. 
    
    If the user only enters 'minor' as the mode, this is ambiguous and it is presumed they want the harmonic minor. We 
    will change this after the mode has been extracted.
    
    Validation consists of the following checks:
    
      1. Does the input begin with a valid musical note (letters a-g) followed by a space?
      2. Is there a single modifier (the word 'flat' or 'sharp')
      3. Is there a mode and is it valid?
      
    If either step 1, or step 3 above does not evaluate to True then return False and exit the function.
    
    :param user_input: This has already been converted to lowercase
      
    :return False if user input does not validate.
    
    or
    
    :return root:      string. The root of the scale the user would like to see
    :return modifier:  string. May be '', '+', or '-'
    :return mode:      string. Valid musical mode as defined in definitions.mode_types
    """
    # if the input is valid we will return the root, modifier and mode so create holders fo these
    root = ''
    mode = ''
    modifier = ''

    # initially replace multiple white spaces with single space
    user_input = ' '.join(user_input.split())

    # define pattern to search for a single letter followed by a space at the beginning of the user input
    if not re.match('([a-g])\\s', user_input[:2]):
        # user input is invalid so return False
        return False

    # input has a valid root so extract it.
    root = user_input[0]

    # check for only a single modifier. if there are multiple in any combination then validation fails so return False.
    if user_input.count('sharp') > 1 or \
            user_input.count('flat') > 1 or \
            user_input.count('sharp flat') > 0 or \
            user_input.count('flat sharp') > 0:
        return False

    # check for a modifier and extract it. We will extract the mode here as well.
    if re.match('sharp', user_input[2:]):
        modifier = '+'
        mode = re.sub('sharp', '', user_input[2:])
    elif re.match('flat', user_input[2:]):
        modifier = '-'
        mode = re.sub('flat', '', user_input[2:])
    else:
        mode = user_input[2:]

    # remove any unwanted whitespace from the mode.
    mode = mode.strip()

    # check the 'mode' for just 'minor' and change to 'harmonic minor' if need be.
    if 'minor' in mode and 'harmonic' not in mode and 'melodic' not in mode and 'natural' not in mode:
        mode = 'harmonic minor'

    # check if what we are left with is a valid mode
    if mode not in definitions.mode_definitions.keys():
        # this is not a valid mode so return False
        return False

    # we have a valid root, modifier and mode so return these as a list
    return [root, modifier, mode]


def create_scale(scale_elements):
    """
    This function is only called if the user has entered a valid scale. We will create the scale through the following 
    algorithm:
    
      1. Find the major scale that shares the root that the user has entered.
      2. Create a new scale upon this root using the degrees of the major scale as defined in 
         'definitions.mode_definitions'.
      3. Apply any modifiers to our newly build scale, again using 'definitions.mode_definitions'.
      4. prepare the scale for display to the user.
    
    :param scale_elements: list of strings with length 3. [root, modifier, mode] (modifier may be an empty string)
    :return string: The scale that we want to display
    """
    # get the root with modifier
    full_root = ''.join(scale_elements[:2])

    # get the mode definition
    mode_definition = definitions.mode_definitions.get(scale_elements[2])

    # get the major scale that shares the root with the scale we are looking for
    major_scale = definitions.majors.get(full_root)

    # create an empty list for our scale
    scale = []

    # get the degrees of the major scale we need to use and populate our empty scale list with these notes
    for degree_and_modifier in mode_definition:
        # extract just the degree (digit) and modifier ('+' or '-') from this degree
        # the degree needs to be one less than the user entered as we are using it as the position in a list
        degree = int(degree_and_modifier[0]) - 1

        # modifier may not exist so initialise with None and attempt to change this
        modifier = None
        if len(degree_and_modifier) > 1:
            modifier = degree_and_modifier[1:]

        # get the correct note from the major scale and if there is a modifier, modify it
        note = modify_note(major_scale[degree], modifier)

        # add the note to our scale
        scale.append(note)

    # add the root to the end of the scale. This is not strictly essential for the scale to be
    # correctly defined is but expected by musicians
    scale.append(scale[0])

    # prepare the scale for display
    prepared_scale = prep_scale_for_display(scale)

    # return the scale as a string
    return prepared_scale


def modify_note(note, modifier):
    """
    This function attempts to modify a note if needed. If the modifier is None then we simply return the note that was
    passed in. If the modifier passed in is not None, we first need to find out if the note passed in has an existing
    modifier, then act accordingly.
    
    :param note:     string. The musical note we wish to modify
    :param modifier: string. Either '++', '+', '-', '--', or None
    :return: string: The modified note
    """
    # if the modifier is None then simply return the note that was passed in.
    if modifier is None:
        return note

    # the modifier is not None so find out if we need to raise or lower the note.
    new_note = ''
    if '+' in modifier:
        new_note = raise_note(note, len(modifier))
    elif '-' in modifier:
        new_note = lower_note(note, len(modifier))

    return new_note


def raise_note(note, num_semitones):
    """
    Raises the note passed in by the number of semitones in num_semitones.

    :param note:          string: The note to be raised
    :param num_semitones: The number of times the note passed in is to be lowered
    :return: string:      A note one or more semitones higher than the one passed in
    """
    # start with the note passed in
    raised_note = note
    for i in range(num_semitones):
        # if the note involves '-' then all we need to do is trim the last character from the string
        if '-' in raised_note:
            raised_note = raised_note[:-1]

        # if the note does not involve '-' then all we need to do is append '+' to the end of the string
        else:
            as_list = list(raised_note)
            as_list.append('+')
            raised_note = ''.join(as_list)

    return raised_note


def lower_note(note, num_semitones):
    """
    Lowers the note passed in by the number of semitones in num_semitones.

    :param note:          string: The note to be lowered
    :param num_semitones: The number of times the note passed in is to be lowered
    :return: string:      A note one or more semitones lower than the one passed in
    """
    # start with the note passed in
    lowered_note = note
    for i in range(num_semitones):
        # if the note involves '+' then all we need to do is trim the last character from the string
        if '+' in lowered_note:
            lowered_note = lowered_note[:-1]

        # if the note does not involve '+' then all we need to do is append '-' to the end of the string
        else:
            as_list = list(lowered_note)
            as_list.append('-')
            lowered_note = ''.join(as_list)

    return lowered_note


def prep_scale_for_display(scale):
    """
    This function creates a single string from a list of strings. The list will be a scale formatted as lowercase
    letters as notes with modifiers '-', and '+'. The returned string will be in the format or uppercase letters as 
    notes with the modifiers '#', and 'b' for sharp and flat respectively.
    
    :param scale:   list. The scale the user would like to see as a list of strings (one for each note potentially with
                    modifiers). 
    :return string: The scale formatted as a single string of uppercase letters as notes with modifiers, separated by 
                    commas, for example B major would return as 'B, C#, D#, E, F#, G#, A#, B'
    """
    # create a new list holder for the prepared scale
    new_scale = []

    for note in scale:
        # change the note to uppercase
        new_note = note.upper()

        # find and replace any modifiers with the appropriate musical symbols
        if '-' in new_note:
            new_note = re.sub('-', 'b', new_note)
        elif '+' in note:
            new_note = re.sub('\+', '#', new_note)

        new_scale.append('{}, '.format(new_note))

    # pass back the scale as a single string omitting the last 2 characters which will be ', '
    return ''.join(new_scale)[:-2]


def get_user_friendly_result(scale, scale_name):
    """
    :param scale:      string. Either the scale that the user wants to see or if there has been a problem, a message to 
                       the user detailing the issue.
    :param scale_name: string. The user input - should be scale name but may be None if the input is not valid.
    """
    # replace the words sharp or flat with symbols
    if ' sharp' in scale_name:
        scale_name = re.sub(' sharp', '#', scale_name)
    elif ' flat' in scale_name:
        scale_name = re.sub(' flat', 'b', scale_name)

    # if the scale type is simply minor we will be showing the harmonic minor so change this in the user input
    if 'minor' in scale_name and 'harmonic' not in scale_name and \
                    'melodic' not in scale_name and \
                    'natural' not in scale_name:
        scale_name = re.sub('minor', 'harmonic minor', scale_name)

    # return the full string in the format 'scale name: scale'
    return '{}: {}'.format(scale_name.title(), scale)


def print_divider():
    print()
    print('---------------------------------------------------------------------------------------------')
    print()


def get_user_input():
    """
    Repeatedly asks the user for input and acts accordingly. 
    """
    # create a variable to hold the user input
    user_input = ""

    # prompt the user to enter a scale
    while user_input != '-1':
        # get user input as all lower case
        user_input = str.lower(input('Enter a scale: ').lower())
        if user_input != '-1':
            # clear the screen, validate, and then process the user input
            os.system('cls')

            # show the instructions again
            show_instructions()

            # validate the user input and try to get a list of the root, modifier (can be '') and mode
            scale_elements = validate_user_input(user_input)

            # if the user has entered a valid option then process and display it, if not then let them know
            if user_input == 'show modes':
                show_possible_modes()
            elif scale_elements:
                scale = create_scale(scale_elements)
                print(get_user_friendly_result(scale, user_input))
            else:
                print('Please enter a valid scale such as \'C Sharp Harmonic Minor\', or \'F Major\'')

            # print a divider for aesthetic purposes
            print_divider()


def main():
    """
    Requests user input repeatedly until the user decides to exit the application by entering '-1'.
    
    The user input is validated and if it is valid a the scale is created and displayed to the user.
    """
    # clear the screen
    os.system('cls')

    # initially show instructions
    show_instructions()

    # get the user input
    get_user_input()


if __name__ == '__main__':
    main()
