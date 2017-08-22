import unittest
import scale_builder


class TestScaleBuilder(unittest.TestCase):
    def setUp(self):
        pass

    def test_validate_user_input(self):
        """
        If user input is valid then a list of length 3 should be returned. If invalid False should be returned. The
        user input passed to the function validate_user_input is already lowercase so we will only use lowercase 
        input when testing valid fixtures.
        """
        # valid input. list of tuples of the form (input fixture, expected output)
        valid_fixtures = [
            ('c sharp lydian augmented', ['c', '+', 'lydian augmented']),
            ('c major', ['c', '', 'major']),
            ('f sharp locrian', ['f', '+', 'locrian']),
            ('b melodic minor', ['b', '', 'melodic minor']),
            ('f sharp mixolydian', ['f', '+', 'mixolydian']),
            ('g minor', ['g', '', 'harmonic minor']),
            ('e major', ['e', '', 'major']),
            ('e sharp minor', ['e', '+', 'harmonic minor']),
        ]

        # invalid user input
        invalid_fixtures = [
            'C# Minor',
            'B b Major',
            'C+ minor',
            'cmajor',
            'Bflatminor',
            'Fsharp minor',
            'scale c minor',
            'Aeolian on A',
            'a sharpsharp major',
            'b flatflat major',
            'd flatsharp major',
            'f sharpflat major',
            'a flat sharp minor',
            'a flat    sharp minor',
            'f sharp sharp major',
            '1',
            '-1',
            '\'c major\'',
            '\'12345\'',
            '\'1 2 3 4 5\''
            '%$£',
            '******',
        ]

        for fixture in valid_fixtures:
            self.assertEquals(scale_builder.validate_user_input(fixture[0]), fixture[1])

        for fixture in invalid_fixtures:
            self.assertFalse(scale_builder.validate_user_input(fixture))

    def test_modify_note(self):
        """
        The modify_note function is called from within the create_scale() function at which point the input has already
        been validated so we will only test valid fixtures here.
        
        modify_note() uses the functions raise_note() and lower_note() and as such are tested here. We will not 
        explicitly test these two methods.
        """
        # list of tuples of the form (input fixture, expected output)
        valid_fixtures = [
            # single semitone modifications
            ('a', '-', 'a-'),
            ('b', '+', 'b+'),
            ('a--', '+', 'a-'),
            ('f++', '-', 'f+'),
            ('c', '+', 'c+'),
            ('a+', '-', 'a'),
            ('b-', '+', 'b'),

            # multiple semitone modifications
            ('c', '++', 'c++'),
            ('b', '----', 'b----'),
            ('g--', '++', 'g'),
            ('g+', '---', 'g--'),
        ]

        for fixture in valid_fixtures:
            self.assertEqual(scale_builder.modify_note(fixture[0], fixture[1]), fixture[2])

    def test_create_scale(self):
        """
        The function create_scale() is only called when the data that the user has given has been validated in the
        function validate_user_input() which is tested above so no need to test invalid fixtures here.
        """
        # list of tuples of the form (input fixture, expected output)
        valid_fixtures = [
            (['c', '', 'major'], 'C, D, E, F, G, A, B, C'),
            (['b', '-', 'lydian augmented'], 'Bb, C, D, E, F#, G, A, Bb'),
            (['f', '', 'harmonic minor'], 'F, G, Ab, Bb, C, Db, E, F'),
            (['g', '', 'major'], 'G, A, B, C, D, E, F#, G'),
            (['a', '+', 'harmonic minor'], 'A#, B#, C#, D#, E#, F#, G##, A#')
        ]

        for fixture in valid_fixtures:
            self.assertEqual(scale_builder.create_scale(fixture[0]), fixture[1])

    def test_prep_scale_for_display(self):
        """
        the list passed into the function is a list of lowercase letters with potential modifiers '+' and '-'. The 
        output is a single string of uppercase letters with modifiers '#' and 'b' separated by commas. 
        
        The input to this function is given by the method create_scale() and will be valid so no need to test invalid
        fixtures
        """
        # list of tuples of the form (input fixture, expected output)
        valid_fixtures = [
            (['c', 'd', 'e', 'f', 'g', 'a', 'b', 'c'], 'C, D, E, F, G, A, B, C'),
            (['f', 'g', 'a-', 'b-', 'c', 'd-', 'e', 'f'], 'F, G, Ab, Bb, C, Db, E, F'),
            (['a', 'b', 'c', 'd', 'e', 'f', 'g', 'a'], 'A, B, C, D, E, F, G, A'),
            (['e-', 'f', 'g', 'a-', 'b-', 'c', 'd', 'e-'], 'Eb, F, G, Ab, Bb, C, D, Eb'),
            (['g+', 'a+', 'b+', 'c+', 'd+', 'e+', 'f++', 'g+'], 'G#, A#, B#, C#, D#, E#, F##, G#'),
        ]

        for fixture in valid_fixtures:
            self.assertEqual(scale_builder.prep_scale_for_display(fixture[0]), fixture[1])

    def test_get_user_friendly_result(self):
        """
        The function should takes a scale which has been processed by prep_scale_for_display() which has been tested 
        above so we will not test for invalid fixtures.
        """
        # list of tuples of the form (input fixture, expected output)
        valid_fixtures = [
            ('C, D, E, F, G, A, B, C', 'c major', 'C Major: C, D, E, F, G, A, B, C'),
            ('F, G, Ab, Bb, C, Db, E, F', 'f minor', 'F Harmonic Minor: F, G, Ab, Bb, C, Db, E, F'),
            ('A, B, C, D, E, F, G, A', 'a aeolian', 'A Aeolian: A, B, C, D, E, F, G, A'),
            ('Eb, F, Gb, Ab, Bb, Cb, D, Eb', 'e flat minor', 'Eb Harmonic Minor: Eb, F, Gb, Ab, Bb, Cb, D, Eb'),
            ('G#, A#, B#, C#, D#, E#, F##, G#', 'g sharp major', 'G# Major: G#, A#, B#, C#, D#, E#, F##, G#'),
        ]

        for fixture in valid_fixtures:
            self.assertEqual(scale_builder.get_user_friendly_result(fixture[0], fixture[1]), fixture[2])

if __name__ == '__main__':
    unittest.main()

