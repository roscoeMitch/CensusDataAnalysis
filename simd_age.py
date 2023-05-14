import csv
import os

os.path.abspath(os.getcwd())

class CensusData:
    """
    Creating a class to store the census data in a dictionary format and perform functions
    """
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.data_dict = {} # Dictionary to hold the census data
    
    def __repr__(self) -> str:
        """
        Returns class data members within a string along with their names 
        """
        return f"filename:{self.filename}" + "\n" + f"data_dict:{self.data_dict}"

    def load(self) -> bool:
        """
        Method to load in the census data to the above defined dictionary
        """
        exists = os.path.isfile("DC1117SC.csv")
        if not exists: # If file does not exist returns False
            return False

        # Otherwise open the dataset and load it into a dictionary reader object
        with open("DC1117SC.csv", "r", newline="", encoding="iso-8859-1") as f:

            data = csv.DictReader(f, fieldnames = ("Region", "Range", "All people"), delimiter=",", quotechar='"')
            for i in range(5): # Skipping the first 4 lines
                next(data)

            # Creating a list of dictionaries
            input_dicts = []
            for row in data:
                input_dicts.append(row)
            
            # Defining a set of unique values for the "Region" and "Range" keys
            regions = set([data["Region"] for data in input_dicts])
            age_ranges = set([data["Range"] for data in input_dicts])
            
            # Loops through all the above defined regions
            for region in regions:
                self.data_dict[region] = {} # At every iteration defines a new dictionary with the region as the key
                for age_range in age_ranges: # Loops through all age ranges for every region
                    # For every dictionary in the list of dictionaries return the number of people
                    # living there if the current iteration of the for loops matches the region and age range 
                    n_people_list = [d["All people"] for d in input_dicts if d['Region'] == region and d['Range'] == age_range]

                    if len(n_people_list) != 1: # If the list does not have an element continues the loop
                        continue

                    n_people = n_people_list[0] # First element of the list is the number of people living there in that age range

                    self.data_dict[region][age_range] = n_people # Fills up the dictionary with the desired values
        
        return True # Returns True on success

    def regions(self) -> list:
        """
        Returns a list of all regions
        """
        return list(self.data_dict.keys())
    
    def total_population(self, region: str, age: int) -> int:
        """
        Returns the number of people living in the input region up to and including the input age
        """
        if region not in list(self.data_dict.keys()): # If region is not in the list returns 0
            return 0

        summed = 0
        # Loops through the dictionary within a given region and redefines the keys appropriately 
        for key, population in self.data_dict[region].items():
            if key == "Under 1":
                key = 0
            elif key == "85 to 89":
                key = 89
            elif key == "90 to 94":
                key = 94
            elif key == "95 and over":
                key = 100
            elif key == "All people": # Does not count "All people" values towrds the summation
                continue 
            
            if age >= int(key): # Sums up the appropriate values associated with the given age
                summed += int(population.replace(",", ""))
        return summed


class SIMD_Data:
    """
    Class to store SIMD data in dictionary format and perform methods
    """
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.data_dict = {} # Dictionary to hold the census data

    def __repr__(self) -> str:
        """
        Returns class data members within a string along with their names
        """
        return f"filename:{self.filename}" + "\n" + f"data_dict:{self.data_dict}"

    def load(self) -> bool:
        """
        Method to load in the census data to the above defined dictionary
        """
        exists = os.path.isfile("SIMD_2020v2csv.csv")
        if not exists: # If file is not in given directory returns False
            return False
        
        # Otherwise open the dataset and load it into a dictionary reader object
        with open("SIMD_2020v2csv.csv", "r", newline="", encoding="iso-8859-1") as f:

            # Read in the data in a dictionary reader object
            data = csv.DictReader(f, delimiter=",", quotechar='"')
            input_dicts = []
            for row in data: # Creating a list of dictionaries
                input_dicts.append(row)
            
            # Assigning a list of unique regions in dataset to variable
            regions = list(set([data.get("MMWname") for data in input_dicts]))                
            for region in regions:  # Loops through all the regions
                self.data_dict[region] = [] # Creates an empty dicitonary to store values at every iteration
                # Stores rankings as a list of integers if the cyrrent iteration of for loop corresponds to region
                ranking = [int(d["SIMD2020v2_Rank"]) for d in input_dicts if d['MMWname'] == region] 
                average_ranking = sum(ranking)/len(ranking)  # Calculating the average ranking for each region
                self.data_dict[region] = average_ranking # Assigning it to the above created nested dicitonary
        return True # Returns True on success

    def regions(self) -> list:
        """
        Returns a list of all regions
        """
        return list(self.data_dict.keys())
    
    def lowest_simd(self) -> str:
        """
        Return the region with the lowest simd rank
        """
        values = self.data_dict.values() # A list of all dictionary values
        min_value = min(values) # Getting the minimum value from the list

        # Returning the key associated with the minimum value
        for region, ranking in self.data_dict.items():
            if ranking == min_value:
                return region


def skip_lines(file_connection: str, no_of_lines: int) -> bool:
    """
    Returns True if the input number of lines in the input file can be skipped
    """
    lst = [] 
    lst.append(file_connection.readline()) # Reading in the first line
    
    # Reading in the data line by line as long as it does not return an empty string which means there is no more lines to read in
    while lst[-1] != "": 
        lst.append(file_connection.readline())
    return len(lst) >= no_of_lines # Returns a boolean

def main():
    simd_data = SIMD_Data("SIMD_2020v2csv . csv") # Instantiating the SIMD_Data class
    
    # If it can be loaded in print out the lowest ranking region 
    if simd_data.load(): 
        lowest_simd = simd_data.lowest_simd()
        print(lowest_simd)

    # Also prints out the ranking of that region 
        lowest_ranking = 0
        for region, ranking in simd_data.data_dict.items():
            if region == lowest_simd:
                lowest_ranking += ranking
                print(ranking)

    census_data = CensusData("DC1117SC . csv") # Instantiating the CensusData class
    # If it loads then prints out the number of people below the age of 15 living in the lowest ranking region
    if census_data.load():
        print(census_data.total_population(lowest_simd, 15))     


if __name__ == "__main__":
    main()




