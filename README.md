# handotate
basic video annotation program

# installation

* git clone https://github.com/hrc2da/handotate.git
* cd handotate
* virtualenv venv -p python3
* source venv/bin/activate
* pip install -r requirements.txt

# usage
* run python handotate.py to annotate all the video files in ./vid
* hit the keys indicated on the window to label each frame and auto-advance
* hit q to exit
* to setup the labels, edit the labels.yaml file
* command line options:
** --dir: a directory containing your videos (default 'vid')
** --out: a directory where the .csv files will be output (default 'out')
** --labels: the labels .yaml file (default 'labels.yaml')


disclaimers: haven't tested w/more than one video file. haven't really tested if the output file is correct at all.
