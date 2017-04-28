# Musical Scale Builder

For author details please read the included AUTHORS file. 

For licence details please read the included LICENCE file.

If you would like to contact me regarding this application or to submit a bug, please do so by emailing me
at fraserjohnstone12345@hotmail.com.

## The Application

This application provides musicians with an easy way to find out which musical notes are included in a scale.

The purpose of this README file is to aide the use of this program and is not intended to aide developers or explain the code.
The code is extensively commented for that purpose and offers very clear explanations at each step in the process.

More often than not, composers use notes from the common Major and Minor keys, for example, C Major, F# Harmonic Minor, 
G Major, and so on. 

Both Major and Minor are simply arrangements of musical tones and semitones (a semi-tone in western music being the closest distance from one 
note to its neighbour, and a tone being 2 semitones). An arrangement of intervals such as this in music is referred to as a mode. 
Throughout the application the word 'mode' is used to refer to an arrangement of intervals, and the word 'scale' is used to refer to
a mode with a specific root note.

In Western music, modes come in a huge number of forms, from which Major and Minor are just two. The modes available in this application are listed below, but
this list is by no means comprehensive. There are undoubtedly many many more, but this application supports all of the common modes
likely to be encountered and then some.

Supported modes:

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

Each of the modes above can be created by altering degrees of the Major mode with the same tonic which is the general idea behind 
the algorithm used here.

## Usage

This application was developed to run on Windows with Python 3 installed.

To start the program simply run the file 'scale_builder.py'. If Python has been 
added to your PATH then you can simply run the 'start.bat' file included. 

To display a scale, all you need to do is type it into the command prompt in the format 'root-note mode-type'. For Example:
        
    - 'C Major'                     (shows: C, D, E, F, G, A, B, C)
    - 'F Sharp Harmonic Minor'      (shows: F#, G#, A, B, C#, D, E#, F#)
    - 'G Lydian'                    (shows: G, A, B, C#, D, E, F#, G) 
    - 'F Major'                     (shows: F, G, A, Bb, C, D, E, F)
    - 'C Sharp Melodic Minor'       (shows: C#, D#, E, F#, G#, A#, B#, C#, B, A, G#, F#, E, D#, C#)
    
The text that you input is not case sensitive, so 'c sharp major' is just as valid as 'C Sharp Major'. It does however need
to involve spaces between the letter, any sharp or flat, and the mode.

If you would like to be shown a list of the available modes, just type 'Show Modes'. Again, this input is not case sensitive.

Due to the limitations of the windows command prompt, double sharps, etc are displayed by using multiple signs:

    Double Sharp: '##'
    Double Flat: 'bb'

## Further Development

If you would like to submit any further modes that have not been included in this application, please email me at 
fraserjohnstone12345@hotmail.com