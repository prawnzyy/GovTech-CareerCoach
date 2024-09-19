# GovTech-CareerCoach
Techincal Assessment for GovTech CareerCoach Data Engineer

Running the code locally
1. From the command line at the root directory of the project, run the following command `python .\src\main.py`.
Alternatively, just running `main.py` from an IDE such as VScode will work.
2. The CSV files will be generated at the root of the project.

For running unittest
1. Run `python -m unittest` in the root directory of the project to run all test cases.
2. To run each test file separately, run the following command `python -m unittest .\tests\{name of test file}`
3. Note that launching the file directly from VScode and not the command may not work.

# Design and Deployment on Cloud
A possible design implementation to be used with cloud services would be similar to the current architecture.

There would be 3 main components to this:
1. __Data reading__
    - For data reading, a cloud service such as AWS lambda can be triggered to read the data periodically. Using a cron job from Amazon EventBridge, lambda can be triggered to read these online files, either from a storage such as AWS S3 or just another hosted source. After the data is read, it will check if the data is new or has changed. If so, move on to the data processing portion.
2. __Data Processing__
    - AWS Lambda can once again be used to process these data. The processing stage will be where operations such as filter, sorting or merger will happen. Once the data has been processed, it will move on the storage section. 
3. __Data Writing / Storage__
    - For data storage, AWS S3 can be used to store all the data (E.g. CSV files) efficiently and quickly and also allows for easy retrieval if we need the data.

# Design Considerations
There were a few design considerations which I had when trying to come up with a solution.
1. Efficiency
    - Dealing with high volumes of data, there needs to be an easy way to be able to sort through all of them quickly. 
    - Extraction of data without the code getting too convoluted is important to ensure further updates or extensibility in the future.
    - As such, I chose to use the Pandas library with Python as it does help resolve a lot of these issues.
2. Extensibility
    - The ability to scale the solution up and to further improve upon it easily is an important factor when coming up with the solution. 
    - Having an object oriented design approach allows many software principles as such Single Responsibility Principle (SRP) to be used.
3. Testability
    - Code that cannot be tested easily is hard to expand upon as debugging becomes tricky.
    - By modularising the code into the various classes and objects, it ensures that the each object can be tested individually.
    - Only after each component is working would it be integrated fully to get a working solution. 


# Architecture Diagram
![Architecture Diagram](./img/GovTech%20Archi.png)

The above is an overarching architecture diagram of the current code. 

We have two file readers, Excel Reader and Json Reader which will read in their respective types of file and then convert the data read into Dataframes which will then be based into main or the main data processing portion. 

The processing portion will extract and filter the necessary data, after which it will be sent to the CSV writer

The CSV writer will write out to the corresonding file along with certain conditions or columns imposed on it. 