# HandGestureRecognition

## It is a CNN based Machine Learning Model to detect Hand Gestures.

- This is a college project in which we have built a machine learning model to recognize a hand gesture which is available in the database.
- We used CNN algorith to train the model 
- Training and Testing dataset consists of over 3000 monochrome images of resolution 400x400 . Each class of hand gesture has average 600 images in it.
- Model is trained using monochrome images so it can only take input of monochrome images of 400x400 so it can be used to identify the the gesture using the model.
- Model has accuracy of over 92% on test dataset and 90% on validation dataset.

## Limitations of this model
- Since model is trained on monochrome images and can only detect patterns in a monochrome image, we have lot less detail to work on.
- Monochrome images leads to one more challenege and that is: we have to seprate the background from foreground to remove noise in the image.
- To seprate the foreground from backgrou we used pixel based background subtraction,in which we take still image of background without the foreground and the we introduce the 
  foreground object in it.This makes it possible to fill the foreground object with white pixles and background with black pixels.

# Prerequisites
- Install python 3.6 or above
- Setting up virtual enviroment is recommended
- Go to the project directory
- Open Command line in current direcory and excecute these commands
  - pip install -r requirements.txt
  ##### To run the project
  - python run.py

Co-Authors: Arindam Ray and Aman Bahal
