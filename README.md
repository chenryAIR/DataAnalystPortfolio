# Chad Henry: Data Analyst Portfolio
## The following are examples my work in Python, SQL, ArcGIS, and Tableau

### Python:
*Driving Distance and Driving Time Calculations using HERE API*</br>
 I worked with a dataset of 250,000 pre-K students across Oklahoma and identified the nearest pre-K center for each student based on drive time. To reduce processing time and API costs, I first calculated straight-line distances between each student and all centers using their latitude and longitude coordinates. I then selected the 10 nearest centers for each student and used the HERE API to calculate actual drive times to those locations. These results were used in the following report. NOTE: The code for this is not available, but you can see the code for a smaller project using HERE below. 

![Report](https://github.com/chenryAIR/KYWP/blob/main/Screenshot%202025-04-23%20141127.png)

*[PYTHON Geocoding Addresses with HERE API.py](https://github.com/chenryAIR/DataAnalystPortfolio/blob/main/PYTHON%20Geocoding%20Addresses%20with%20HERE%20API.py)*</br>
40k addresses needed to be geocoded quickly with a small level of descriptions to determine the quality of the geocodes (e.g., the number of geocodes with a score < 0.9 and number of geocodes by result type). 

*[PYTHON ArcPy General Symbology.py](https://github.com/chenryAIR/DataAnalystPortfolio/blob/main/PYTHON%20ArcPy%20General%20Symbology.py)*</br>
To streamline the GIS team’s workflow, I developed a generalized Python script to automate the creation of map layers in ArcGIS Pro. This tool:</br>
- Loads data into ArcGIS Pro, either mapping points from latitude/longitude coordinates or joining tabular data to shapefiles  
- Applies custom symbology to visualize key attributes  
- Scales easily to generate dozens of layers in a loop for large projects

The script is designed for novice users—they can simply fill in a few variables (e.g., file paths, field names, color settings) and run the code in ArcGIS Pro without modifying the core logic. This significantly reduced manual GIS work and improved consistency across projects.

