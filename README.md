Project prepared during the "Machine learning for embedded systems" course.

Contains:

data-science part:
  1. Data scraper, which uses bs4 library, to fetch car data from otomoto.pl website
  2. Data preprocessing
  3. Comparision and evaluation of few possible ML algorithms, taken from sklearn library.

android part:
  1. Simplified data preprocessing and creation of Pytorch NN model.
  2. Android Studio project, which contains dummy VW PASSAT price predictor.
  
Best predictors, that I managed to prepare, were created within data-science part, using tree based algorithms from sklearn library.
Unfortunately, due to a technical barrier, I did not succed to apply such a model in the mobile-project. That's why trained pytorch model is just a dummy nn.

![alt text](https://github.com/HubertWdowiak/otomoto-predictor/blob/main/otomoto.jpg)
