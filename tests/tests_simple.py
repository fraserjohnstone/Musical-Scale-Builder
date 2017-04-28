import unittest
import scale_builder


class TestSB(unittest.TestCase):
    def setUp(self):
        pass

    def test_validate_user_input(self):
        """
        If user input is valid then a list of length 3 should be returned. If invalid False should be returned 
        """
        valid_input = [
            'c sharp lydian augmented',
            'C Major',
            'F Sharp Locrian',
            'B Melodic Minor',
            'f sharp mixolydian',
            'g minor',
            'e Major',
            'E mAjor'
        ]

        invalid_input = [
            'C# Minor',
            'B b Major',
            'C+ minor',
            'cmajor',
            'Bflatminor',
            'Fsharp minor',
            'scale c minor',
            'Aeolian on A'
        ]

        for case in valid_input:
            self.assertTrue(scale_builder.validate_user_input(case))

        for case in invalid_input:
            self.assertFalse(scale_builder.validate_user_input(case))

    def test_raise_note(self):
        """
        The note entered should be one higher than the one returned 
        """
        valid_input_output = [
            ('a----', 'a---'),
            ('a---', 'a--'),
            ('a--', 'a-'),
            ('a-', 'a'),
            ('a', 'a+'),
            ('a+', 'a++'),
            ('a++', 'a+++'),
            ('a+++', 'a++++')
        ]

        invalid_input_output = [
            ('a----', 'a--'),
            ('a---', 'a-'),
            ('a--', 'a'),
            ('a-', 'a+'),
            ('a', 'a-'),
            ('a+', 'a+'),
            ('a++', 'a-+'),
            ('a+++', 'a--')
        ]

        for case in valid_input_output:
            self.assertEqual(scale_builder.raise_note(case[0]), case[1])

        for case in invalid_input_output:
            self.assertNotEqual(scale_builder.raise_note(case[0]), case[1])

    def test_lower_note(self):
        """
        The note entered should be one lower than the one returned 
        """
        valid_input_output = [
            ('a++++', 'a+++'),
            ('a+++', 'a++'),
            ('a++', 'a+'),
            ('a+', 'a'),
            ('a', 'a-'),
            ('a-', 'a--'),
            ('a--', 'a---'),
            ('a---', 'a----')
        ]

        invalid_input_output = [
            ('a++++', 'a++'),
            ('a+++', 'a+'),
            ('a++', 'a'),
            ('a+', 'a-'),
            ('a', 'a+'),
            ('a-', 'a-'),
            ('a--', 'a+-'),
            ('a---', 'a++')
        ]

        for case in valid_input_output:
            self.assertEqual(scale_builder.lower_note(case[0]), case[1])

        for case in invalid_input_output:
            self.assertNotEqual(scale_builder.lower_note(case[0]), case[1])


if __name__ == '__main__':
    unittest.main()

