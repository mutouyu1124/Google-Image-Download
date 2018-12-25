# Download Image from Google
## [googlesearchimage.py](https://github.com/mutouyu1124/Google-Image-Download/blob/master/googlesearchimage.py)
Use this script to download images from Google. 

If you would want to download more than 100 images per keyword, you would need to install Selenium library along with chromedriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads), and then use '--chromedriver' or '-cd' argument to specify the path of chromedriver that you have downloaded in your machine. 

The arguments includes:
* --keywords(-k): the search keywords
* --format(-f): download images with specific format, possible choice: 'jpg','gif','png','bmp','svg'
* --limit(-l): delimited list input
* --color_type(-ct): filter on color, possible choice: 'full-color','black-and-white','transparent'
* --output_directory(-o): downloading images in a specific main directory
* --safe_search(-sa): Turns on the safe search filter while searching for images
* --chromedriver(-cd): specify the path to chromedriver executable in your local machine

Run like
```
python googlesearchimage.py -k BMW --format jpg -l 110 -t photo -o car --chromedriver ./Desktop/googlesearchimage/chromedriver -sa
```
