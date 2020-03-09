# Age_Gender_Scraping

This is a simple combination of image scraping with a Convolutional Neural Network used for age and gender estimation. Simply edit the url in the python file and the program will extract all the images and estimate gender and age. 

Dependencies: 
```
pip3 install py-agender[cpu]  # for the cpu version of TensorFlow
pip3 install py-agender[gpu]  # for the gpu version of TensorFlow
pip3 install cv
```
Note: The CNN is pretrained, so the weight files are pretty large (200MB). Gender estimates are highly reliable, but the age estimation is fairly rough. Fine tuning is recommended. 
