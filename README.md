# Face Detection
These Python scripts perform simple face detection using the default Haar Cascade data provided by OpenCV.

## Example
Sample output shown below.

![Example](images/example.png)

## Environment
An environment file has been provided to generate and use an Anaconda environment. See [requirements.txt](env/requirements.txt). To use:

`$ conda create --name vision -- file env/requirements.txt`

`$ conda activate vision`

## Running
With the conda environment activated, run the following command:

- For a local desktop "application"

`$ python face-detection.py`

*Note: To exit the program, select the active UI window and type the *'q'* key or *'Ctrl-c'* in the terminal.*

- For a local web server (served at http://localhost:8080)

`$ python face-detection-web.py`

## License
Please see [License](LICENSE) file for usage information.
