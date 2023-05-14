import unittest
import simd_age
import os
import csv

os.path.abspath(os.getcwd())

class TesCensusData(unittest.TestCase):
    """
    A class to unittest the CensusData data class in simd_age.py
    """

    def test_regions(self) -> None:
        """
        A method to test whether the regions() function returns all the regions from the dataset
        """
        census_data = simd_age.CensusData("DC1117SC . csv") # Instantiating the object
        if census_data.load(): # If loading in the data is successful then open the dataset so that it can be compared
            with open("DC1117SC.csv", "r", newline="", encoding="iso-8859-1") as f:

                # After reading in the desired columns the program skips the first 4 lines (headers)
                data = csv.DictReader(f, fieldnames = ("Region", "Range"), delimiter=",", quotechar='"') 
                for i in range(5): 
                    next(data)

                # Creating a list of dictionaries using the dictreader object
                input_dicts = []
                for row in data:
                    input_dicts.append(row)
                    
                # Extracting the unique values from the dictionary and then casting them onto a list
                regions = list(set([data["Region"] for data in input_dicts]))  

        self.assertListEqual(census_data.regions(), regions) # Comparing the two acquired lists

        # Checking whether a list of random regions from the dataset is contained in the output of the regions() method
        name_of_regions = [
        'Hawick and Hermitage', 'Bridge of Don', 'Greater Pollok', 
        'Strathmartine', 'Nairn', 'Thurso', 'Fountainbridge / Craiglockhart', 
        'Jedburgh and District', 'George St / Harbour', 'Paisley South', 'Kilsyth'
        ]
        for region in name_of_regions:
            self.assertIn(region, census_data.regions())

    def test_total_population(self) -> None:
        """
        A method to test whether total_population() returns the correct number of people
        """
        census_data = simd_age.CensusData("DC1117SC . csv")
        if census_data.load():
            # Test whether the total population of a given region filtered for all ages including and below
            # the input integer returns the correct population statistic
            self.assertEqual(census_data.total_population("Paisley South", 56), 13544)
            self.assertEqual(census_data.total_population("Steï¿½rnabhagh a Deas ", 20), 749)
            self.assertEqual(census_data.total_population("Stirling East", 40), 7052)

        
if __name__ == "__main__":
    unittest.main()