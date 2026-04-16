# COMP 3300 Mini Project: CPU Scheduling Simulator

**Team Members:**
* Maria Kandikova
* John Rafael Diaz Cabangon
* Claudia Dinatale

## Overview
This is our simulation for the classic CPU scheduling algorithms. The program reads a JSON file to figure out which policy to run, simulates the CPU timeline, and outputs the Gantt chart and performance metrics strictly as JSON.

The algorithms we implemented are:
* FIFO
* SJF (non-preemptive)
* Round Robin
* Priority (non-preemptive)

For all of these algorithms, if there is ever a tie between jobs, we break it using the lexicographically smallest PID (so basically alphabetical order) just like the instructions asked.

## How to Run
You need Python 3 to run this project. Just use this command in the terminal:

`python3 main.py input.json > output.json`

If you want to test the other algorithms, just open the input file and change the "policy" string to one of the other options (like "SJF" or "FIFO").

## Code Structure / Explanation
We decided to put everything inside a single `main.py` file to make it super easy to test and run without dealing with crazy imports. 

* **Helper Functions:** At the top we have a few helpers to handle sorting the queues and a function to calculate the final turnaround and waiting times so we dont repeat that math 4 times.
* **Algorithms:** Then we have the 4 main scheduling functions. Each one takes the jobs list, simulates the time stepping, and builds the gantt chart step by step.
* **Main Block:** At the bottom is the main execution block. It reads the input file, cleans up the strings just in case there are weird spaces, routes the data to the correct algorithm function, and finally dumps the output as a strict JSON format so the autograder doesnt complain. Any errors get sent to standard error so they dont mess up the output file.

## AI Usage Statement
We used Gemini (AI tool) to help us generate a bunch of sample `.json` input files. This saved us a ton of time typing out test cases and let us test our code against different scenarios and edge cases. This helped us verify that our math and logic actually worked for all four algorithms. The actual scheduling logic and python code was put together and structured by our team based on the course materials.