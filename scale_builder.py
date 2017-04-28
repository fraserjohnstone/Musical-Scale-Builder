"""
This application allows the user to type in a musical scale and be shown all of the notes involved.

Throughout the code the following definitions are used:

  - mode:      An arrangement of tones and semi-tones. Major and Minor are 2 commonly used modes, but there are many 
               others. A mode is more commonly but not always correctly referred to as a scale.
  - root:      The tonic (first degree) of a scale.
  - modifier:  Musical sharp or flat symbol. For example F# (read as 'F sharp') has the root F and modifier sharp.
               in code sharps and flats will be represented by '+', and '-' respectively.
  
In short this program works by altering the standard Major mode (also called Ionian mode). Any mode can be represented 
as a modification of the Major that shares the same root note. For example the Aeolian mode with the root note A can 
be represented as degrees 1, 2, flat 3, 4, 5, flat 6, flat 7, and 8 of A Major.

In the definitions module we have a dictionary of major scales (one for each root), and a dictionary of mode definitions
(including the degrees of the major scale included, and any modifier). We use these together to build the ussers mode.
  
For usage instructions and more detailed information please see the README file..
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
          - 'F Major'                     (shows: F, G, A, Bb, C, D, E, F)
          - 'C Sharp Melodic Minor'       (shows: C#, D#, E, F#, G#, A#, B#, C#, B, A, G#, F#, E, D#, C#)
          
        Type 'Show Modes' to see a complete list of available modes.
        
        To exit the application enter '-1'
        
---------------------------------------------------------------------------------------------
    """
    print(msg)


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
        37.Phrygian          38.Prometheus        39.Tritone           40.Wholetone

---------------------------------------------------------------------------------------------
    """
    print(msg)


def validate_user_input(user_input):
    """    
    Checks that the user has entered a valid scale. The input should be for the form 'root-note mode-type'.
    
    in the above format, root-note must take the form:
      
      - The letter a-g followed by a space and the words 'flat' or 'sharp'. this is not case sensitive
          
    If the input validates then we extract the root, any possible modifier, and mode as three separate variables. 
    
    If the user only enters 'minor' as the mode, this is ambiguous and it is presumed they want the harmonic minor. We 
    will change this after the mode has been extracted.
    
    The validation consists of the following checks:
    
      1. Does the input begin with a valid musical note (letters a-g) followed by a space?
      2. Is there a modifier ('flat' or 'sharp')
      3. Is there a mode and is it valid?
      
    If either step 1, or step 3 above does not evaluate to True then return False and exit the function.
    
    :param user_input: 
      
    :return False if user input does not validate.
    
    or
    
    :return root:      string. The root of the scale the user would like to see
    :return modifier:  string. May be '', 'sharp, or 'flat'
    :return mode:      string. Valid musical mode as defined in definitions.mode_types
    """
    # convert the user input to all lower case
    user_input = str.lower(user_input)

    # if the input is valid we will return the root, modifier and mode so create holders fo these
    root = ''
    mode = ''
    modifier = ''

    # define pattern to search for a single letter followed by a space at the beginning of the user input
    if not re.match('([a-g])\\s', user_input[:2]):
        # user input is invalid so return False
        return False

    # input is valid so extract the root
    root = user_input[0]

    # check for a modifier and extract this. We can extract the mode here as well.
    if re.match('sharp', user_input[2:]):
        modifier = '+'
        mode = re.sub('sharp', '', user_input[2:])
    elif re.match('flat', user_input[2:]):
        modifier = '-'
        mode = re.sub('flat', '', user_input[2:])
    else:
        mode = user_input[2:]

    # remove any unwanted whitespace from the mode
    mode = mode.strip()

    # check the 'mode' for just 'minor' and change to 'harmonic minor' if need be
    if 'minor' in mode and 'harmonic' not in mode and 'melodic' not in mode and 'natural' not in mode:
        mode = 'harmonic minor'

    # check if what we are left with is a valid mode
    if mode not in definitions.mode_definitions.keys():
        # this is not a valid mode so return False
        return False

    # we have the root, modifier and mode so return these as a list
    return [root, modifier, mode]


def create_scale(scale_elements, scale_name):
    """
    This function is only called if the user has entered a valid scale. We will create the scale through the following 
    algorithm:
    
      1. Find the major scale that shares the root that the user has entered.
      2. Create a new scale using the degrees defined in 'definitions.mode_definitions'.
      3. Apply any modifiers to the scale again using 'definitions.mode_definitions'.
      4. prepare the scale for display to the user.
    
    :param scale_elements: list of strings with length 3. [root, modifier, mode] (modifier may be empty string)
    :param scale_name:     string. The user input - should be scale name but may be None if the input is not valid.
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
        # the degree is one less than the user entered as we are using it as the position in a list
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

    # display the prepared scale to the user
    display_result_to_user(prepared_scale, scale_name)


def modify_note(note, modifier):
    """
    This function attempts to modify a note if need be. If the modifier is None then we simply return the note that was
    passed in. If the modifier passed in is not None, we first need to find out if the note passed in has an existing
    modifier, then act accordingly.
    
    :param note:     string. The musical note we wish to modify
    :param modifier: string. Either '++', '+', '-', '--', or None
    :return: string: The modified note
    """
    # if the modifier is None then simply return the note that was passed in.
    if modifier is None:
        return note

    # the modifier is not None so find out if we need to raise or lower the note
    new_note = ''
    if '+' in modifier:
        new_note = raise_note(note)
    elif '-' in modifier:
        new_note = lower_note(note)

    return new_note


def raise_note(note):
    """
    Raises the note passed in by one semitone.

    :param note:     The note to be raised
    :return: string: A note 1 semitone higher than the one passed in
    """
    # if the note involves '-' then all we need to do is trim the last character from the string
    if '-' in note:
        raised_note = note[:-1]

    # if the note does not involve '-' then all we need to do is append '+' to the end of the string
    else:
        as_list = list(note)
        as_list.append('+')
        raised_note = ''.join(as_list)

    return raised_note


def lower_note(note):
    """
    Lowers the note passed in by one semitone.

    :param note:     string: The note to be lowered
    :return: string: A note 1 semitone lower than the one passed in
    """
    # if the note involves '+' then all we need to do is trim the last character from the string
    if '+' in note:
        lowered_note = note[:-1]

    # if the note does not involve '+' then all we need to do is append '-' to the end of the string
    else:
        as_list = list(note)
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
    :return string: the scale formatted as a single string of uppercase letters as notes with modifiers, separated by 
                    commas, for example C major would return as 'B, C#, D#, E, F#, G#, A#, B'
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


def display_result_to_user(result, scale_name):
    """
    :param result:     string. Either the scale that the user wants to see or if there has been a problem, a message to 
                       the user detailing the issue.
    :param scale_name: string. The user input - should be scale name but may be None if the input is not valid.
    """
    # check if the scale name has been passed in
    if scale_name is not None:
        # replace the words sharp or flat with symbols
        if ' sharp' in scale_name:
            scale_name = re.sub(' sharp', '#', scale_name)
        elif ' flat' in scale_name:
            scale_name = re.sub(' flat', 'b', scale_name)

        # if the scale type is simply minor we will be showing the harmonic minor so change this in the user input
        if 'minor' in scale_name and 'harmonic' not in scale_name and 'melodic' not in scale_name and 'natural' not in scale_name:
            scale_name = re.sub('minor', 'harmonic minor', scale_name)

        # display the scale to the user
        print('{}: {}'.format(scale_name.title(), result))
    else:
        print(result)


def print_divider():
    print()
    print('---------------------------------------------------------------------------------------------')
    print()


def main():
    """
    Requests user input repeatedly until the user decides to exit the application by entering -1.
    
    The user input is validated and if it is valid a the scale is created and displayed to the user.
    """
    # clear the screen
    os.system('cls')

    # initially show instructions
    show_instructions()

    # create a variable to hold the user input
    user_input = ""

    # prompt the user to enter a scale
    while user_input != '-1':
        user_input = input('Enter a scale: ')
        if user_input != '-1':
            # clear the screen, validate, and then process the user input
            os.system('cls')

            # show the instructions again
            show_instructions()

            # validate the user input and try to get a list of the root, modifier (can be '') and mode
            scale_elements = validate_user_input(user_input)

            # if the user has entered a valid option then process
            if user_input == 'show modes':
                show_possible_modes()
            elif scale_elements:
                create_scale(scale_elements, user_input)
            else:
                display_result_to_user('Please enter a valid scale such as \'C Sharp Harmonic Minor\'', None)

            # print a divider for aesthetics
            print_divider()


if __name__ == '__main__':
    main()
