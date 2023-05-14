import unittest
import simd_age
import os
import csv

os.path.abspath(os.getcwd())

class TestSIMD_Data(unittest.TestCase):
    """
    A class to unittest the SIMD_Data data class in simd_age.py
    """

    def test_regions(self) -> None:
        """
        A method to test whether the regions() function returns all the regions from the dataset
        """
        simd_data = simd_age.SIMD_Data("SIMD_2020v2csv.csv") # Instantiating the object
        if simd_data.load(): # If loading in the data is successful then open the dataset so that it can be compared
       
            # Comparing a list of random regions as strings with the regions got from the regions() function
            name_of_regions = [
            'Carnoustie and District', 'Tain and Easter Ross', 'North East', 
            'Clackmannanshire North', 'Strathmartine', 'An Taobh Siar agus Nis', 'Monifieth and Sidlaw', 
            'Cardonald', '"Houston', 'Stirling West', 'Perth City North', 'Maryfield'
            ]

            # Seeing whether the list contains the above defined random regions
            for region in name_of_regions:
                self.assertIn(region, simd_data.regions())

    def test_lowest_simd(self) -> None:
        """
        A method to test whether lowest_simd() returns the correct region
        """
        simd_data = simd_age.SIMD_Data("SIMD_2020v2csv.csv") # Instantiating the object
        if simd_data.load(): # If loading in the data is successful then open the dataset so that it can be compared
            min_value_region = simd_data.lowest_simd() # Getting th minimum value region (in this case "Canal")
            min_value_rank = simd_data.data_dict[min_value_region] # Getting the value associated with the lowest simd region

            #Comparing the minimum value region to other regions
            self.assertEqual(min_value_region, "Canal")
            self.assertNotEqual(min_value_region, "Strathmartine")
            self.assertNotEqual(min_value_region, "Aboyne")
            self.assertNotEqual(min_value_region, "Perth City North")

            # Comparing the minimum rank to all other ranks by looping through dictionary values
            for rank in simd_data.data_dict.values():
                self.assertLessEqual(min_value_rank, rank)
        
if __name__ == "__main__":
    unittest.main()