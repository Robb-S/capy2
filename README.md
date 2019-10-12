# capy2 - Capybara Detector (deployment in Flask)

The Capybara Detector is a deployment of an AI-driven image-classification model that uses a Convolutional Neural Net for transfer learning.  The model is trained with the help of Python's PyTorch and FastAI  libraries, and it recognizes images of capybaras and 11 other animals, with over 99% accuracy on training data.

The deployment uses Flask plus a bit of Javascript to load user-supplied images and sample images, then access the model for predictions.  It's deployed at DreamHost, running under Passenger.   

Details of the model training process can be found at https://github.com/Robb-S/capybara-train 
