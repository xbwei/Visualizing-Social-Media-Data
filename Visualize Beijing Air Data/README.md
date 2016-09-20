3D-Visulization-of-Beijing-Air-data
===================================

The tools will import the data from the https://github.com/xbwei/BeijingAirExtract project into ArcGIS, and visualize the air data in 3D.
In the tool box, there are 4 tools:

![alt tag](https://raw.githubusercontent.com/xbwei/3D-Visulization-of-Beijing-Air-data/master/tool.jpg)
 
<ul> 
<li>AddQT Field: create the numeric QT field of all air indices for each table.</li>

<li>	Calculate Time Difference: create a timediff field for the input table and calculate the difference between the data recording time and the current time (when running the tool) in seconds. This value can serve as the Z value in 3D modeling. Since the time is measured in a different unit, you can specify the scale in the tool interface.</li>

<li>	CalculateXY: this tool will add the Name, X, Y field for each table based on their table name.</li>

<li>	Clean: because the downloading program recorded all the index values in string data format to avoid errors, the tool can convert the string data into the numerical data format.</li>

<li>	MySQL2DBF: this tool can iterate the tables of the MySQL database via the Database Connection, and export all the tables into a dbf in a personal geodatabase.</li>

</ul>

![alt tag](https://raw.githubusercontent.com/xbwei/3D-Visulization-of-Beijing-Air-data/master/beijingair.jpg)
