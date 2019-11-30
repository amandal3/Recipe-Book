import unittest
import TestRecipe
from TestRecipe import *

class TestStringMethods(unittest.TestCase):
    #print('-----------------------TESTING OPTION 1--------------------------')
    def test_Option1_01(self):
        placeholder = TestRecipe.optionOne('chicken','apple','re','https://www.allrecipes.com/recipe/237992/roasted-greek-chicken/')
        self.assertEqual(placeholder[0], 8)

    def test_Option1_02(self):
        placeholder = TestRecipe.optionOne('chicken','apple','re','https://www.allrecipes.com/recipe/237992/roasted-greek-chicken/')
        self.assertNotEqual(placeholder[1], '') #should just test that we get it

    def test_Option1_03(self):
        placeholder = TestRecipe.optionOne('chicken','apple','re','https://www.allrecipes.com/recipe/223042/chicken-parmesan/')
        self.assertNotEqual(placeholder[1], '') #should just test that we get it

    def test_Option1_04(self):
        placeholder = TestRecipe.optionOne('chicken','apple','re','https://www.allrecipes.com/recipe/223042/chicken-parmesan/')
        self.assertEqual(placeholder[2], 'Chicken Parmesan') #should just test that we get it

    def test_Option1_05(self):
        placeholder = TestRecipe.optionOne('chicken','apple','re','https://www.allrecipes.com/recipe/237992/roasted-greek-chicken/')
        self.assertEqual(placeholder[3], 'Roasted Greek Chicken')

    def test_Option1_06(self):
        placeholder = TestRecipe.optionOne('chicken','apple','re','https://www.allrecipes.com/recipe/223042/chicken-parmesan/')
        self.assertEqual(placeholder[3], 'Chicken Parmesan') #should just test that we get it
    # #print('-----------------------TESTING OPTION 2--------------------------')
    def test_Option2_01(self):
        placeholder = TestRecipe.optionTwo('pie','re','https://www.allrecipes.com/recipe/212491/killer-pumpkin-pie/')
        self.assertEqual(placeholder[0], 8)

    def test_Option2_02(self):
        placeholder = TestRecipe.optionTwo('pie','re','https://www.allrecipes.com/recipe/212491/killer-pumpkin-pie/')
        self.assertNotEqual(placeholder[1], '')

    def test_Option2_03(self):
        placeholder = TestRecipe.optionTwo('pie','re','https://www.allrecipes.com/recipe/22544/pecan-pie-v/')
        self.assertNotEqual(placeholder[1], '')

    def test_Option2_04(self):
        placeholder = TestRecipe.optionTwo('pie','re','https://www.allrecipes.com/recipe/212491/killer-pumpkin-pie/')
        self.assertEqual(placeholder[2], 'Butter Flaky Pie Crust')

    def test_Option2_05(self):
        placeholder = TestRecipe.optionTwo('pie','re','https://www.allrecipes.com/recipe/212491/killer-pumpkin-pie/')
        self.assertEqual(placeholder[3], 'Killer Pumpkin Pie')

    def test_Option2_06(self):
        placeholder = TestRecipe.optionTwo('pie','re','https://www.allrecipes.com/recipe/22544/pecan-pie-v/')
        self.assertEqual(placeholder[3], 'Pecan Pie V')
    # #print('-----------------------TESTING OPTION 3--------------------------')
    def test_Option3_01(self):
        placeholder = TestRecipe.optionThree('cereal','','','ra','https://www.allrecipes.com/recipe/228376/farro-perlato-cereal/')
        self.assertEqual(placeholder[0], 8)

    def test_Option3_02(self):
        placeholder = TestRecipe.optionThree('cereal','','','ra','https://www.allrecipes.com/recipe/228376/farro-perlato-cereal/')
        self.assertNotEqual(placeholder[1], '')

    def test_Option3_03(self):
        placeholder = TestRecipe.optionThree('cereal','','','ra','https://www.allrecipes.com/recipe/232084/homemade-granola-cereal/')
        self.assertNotEqual(placeholder[1], '')

    def test_Option3_04(self):
        placeholder = TestRecipe.optionThree('cereal','','','ra','https://www.allrecipes.com/recipe/232084/homemade-granola-cereal/')
        self.assertEqual(placeholder[2], 'Gluten-Free Hot Breakfast Cereal')

    def test_Option3_05(self):
        placeholder = TestRecipe.optionThree('cereal','','','ra','https://www.allrecipes.com/recipe/228376/farro-perlato-cereal/')
        self.assertEqual(placeholder[3], 'Farro Perlato Cereal')

    def test_Option3_06(self):
        placeholder = TestRecipe.optionThree('cereal','','','ra','https://www.allrecipes.com/recipe/232084/homemade-granola-cereal/')
        self.assertEqual(placeholder[3], 'Homemade Granola Cereal')
    #print('-----------------------TESTING OPTION 4--------------------------')
    def test_Option4_01(self):
        placeholder = TestRecipe.optionFour('pasta','','','p', 2)
        self.assertEqual(placeholder[0], 9)

    def test_Option4_02(self):
        placeholder = TestRecipe.optionFour('pasta','','','p', 2)
        self.assertEqual(placeholder[1], 20)

    def test_Option4_03(self):
        placeholder = TestRecipe.optionFour('pasta','','','p', 2)
        self.assertNotEqual(placeholder[2], '')

    def test_Option4_04(self):
        placeholder = TestRecipe.optionFour('pasta','','','p', 2)
        self.assertEqual(placeholder[3], 'Peppered Shrimp Alfredo')

    def test_Option4_05(self):
        placeholder = TestRecipe.optionFour('pasta','','','p', 2)
        self.assertEqual(placeholder[4], 'Chicken Noodle Soup')

    def test_Option4_06(self):
        placeholder = TestRecipe.optionFour('pasta','','','p', 5)
        self.assertEqual(placeholder[0], [])

    def test_Option4_07(self):
        placeholder = TestRecipe.optionFour('pasta','','','p', 5)
        self.assertEqual(placeholder[1], 20)
if __name__ == '__main__':
    unittest.main()
