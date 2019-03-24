<h1> OpenEd.ai </h1>
Code and contributions for the OpenEd.ai Hackweek
This repository has the Dataset and code used to generate/clean the dataset as well as the code to run the QuickQuestion Command-line program.

<h3> Process </h3>

To create a Reinforcement Learning based, we needed a clean Multiple Choices Exam dataset with known answers.
We decided to use the one MCQ Dataset by CHIEN-CHUN NI <a href="http://www3.cs.stonybrook.edu/~chni/post/mcq-dataset/"> Link </a>

We then wrote and used DBExtract.py to transform the dataset into a CSV table.

Next, a python code was written to ask for user input and answer these MCQ until the user can get all the answers right. The code keeps track of the wrongly and correctly answered questions. To run:

<code> python askQuestions.py [name_of_questionnaire] </code>