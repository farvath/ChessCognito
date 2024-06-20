
# **CHESSCOGNITO** ♔♚

This project tackles automatic chess game analysis through image recognition. It captures the chessboard, identifies pieces, and generates a FEN (board position) for analysis using the Lichess API. This analysis provides valuable feedback to players, including:

* Move suggestions 🕵️ 
* Strategic insights 🧠
* Overall game assessment 👑

ChessCognito automates the process, saving time and offering real-time feedback for improved chess gameplay.


## **Software Installation**

Installation instructions for a Windows computer are presented below.

1. First clone the repository and cd into it:
    ```bash
    git clone https://github.com/farvath/ChessCognito.git
    cd ChessCognito
    ```

2. Create a python virtual environment, activate it and upgrade pip:
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    ```
4. Install the required python packages:
    ```bash
    pip install -r requirements_pc.txt
    ```

5. Install **Python 3.10** from Microsoft Store. It is important **NOT** to install Python 3.11 instead as it would create dependency (numpy) issues when we later install onnxruntime and tensorflow==2.12.0.

6. If you see any warning about some directory not on PATH, follow [this](https://stackoverflow.com/questions/49966547/pip-10-0-1-warning-consider-adding-this-directory-to-path-or/51165784#51165784) and restart the computer to resolve it.

7. Install tensorflow and corresponding [CUDA version](https://docs.nvidia.com/cuda/cuda-installation-guide-microsoft-windows/index.html).

8. Now you can install all the relevant packages by running the following commands in Windows PowerShell:
```bash
    pip install numpy
    pip install opencv-python
    pip install chess
    pip install tensorflow==2.12.0
    pip install onnxruntime
    pip install matplotlib
    pip install pyclipper
    pip install scikit-learn
    pip install tqdm
    pip install pandas
    pip install onnx
    pip install tf2onnx
    pip install pytest
```
Note: the above commands would install all the latest-possible versions of the required packages (it was found that there might not be any restrictions on the versions of nontensorflow packages). Alternatively, you could use the "requirements_pc.txt" file (pip install -r requirements_pc.txt) to install the specific versions that have been tested to be 100% working.

10. Finally, in order to successfully import `tensorflow`, you also need to install a Microsoft Visual C++ Redistributable package from [here](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170).
If you are using Windows 11 ([Windows 11 only has the 64-bit version](https://www.intowindows.com/where-can-i-download-windows-11-32-bit-iso/)), you can simply download and install
[this](https://aka.ms/vs/17/release/vc_redist.x64.exe).

Also, depending on the inference engine you want to use, install the following dependencies:

 * Keras with tensorflow backend.
 * ONNX Runtime.
 * (Optional) TensorRT and PyCUDA.



## **USAGE INSTRUCTIONS**
1. Edit `predict_fen.py` and set the `ACTIVATE_*`, `MODEL_PATH_*`,
 `IMG_SIZE_*`, and `PRE_INPUT_*` constants.

   - `ACTIVATE_KERAS = True` will select Keras with tensorflow backend as the inference engine. The Keras engine is the slowest of the three.

   - `ACTIVATE_ONNX = True` will select ONNX Runtime as the inference engine. It is significantly faster than Keras but almost just as accurate. It is the recommended choice for any standard computer.

   - `ACTIVATE_TRT = True` will select TensorRT as the inference engine. It is the fastest of the three but only available on computers with Nvidia GPUs.

2. Run the `test_lc2fen.py` script.

## **TRAINING NEW MODELS**

To train new models, check the [this repo](https://github.com/davidmallasen/LiveChess2FEN/blob/master/README.md#training-new-models) . That directory contains 
the python scripts used to train the chess piece models. It also contains 
the scripts used to manipulate both the dataset and the models.
## **USAGE OF END-TO-END FRAMEWORK**

To use the main program, `app.py` :

1. Make sure your phone and Windows computer are in the connected to same camera . You may use third-party application to do so (one such is [DroidCam](https://droidcam.app/) ).

2. Open the app on your phone (that turns your phone into an IP camera), mount the phone on some kind of physical structure (Tripod), and edit the IMAGE_SOURCE variable in `app.py` (Incase you want to try on a image you can directly use the `predict_fen.py`).

3. Edit the FULL_FEN_OF_STARTING_POSITION, A1_POS, and BOARD_CORNERS variables in `app.py` (feel free to edit other variables as well, but these three are generally the most relevant to the user).

4. Run the application . 

5. After the game, feel free to use SAVE option for postgame analysis.

**NOTE:** If `BOARD_CORNERS` is set to None, automatic (neural-network-based) chessboard detection is used, and each moves takes at most 8 seconds to register with Intel Core i7.
## **TECHNICAL DETAILS**

The figure below shows a high-level flow diagram for the signal-processing workflow. Models details are mentioned in this [paper](https://arxiv.org/abs/2012.06858):

!["FLOW DIAGRAM"](https://github.com/farvath/ChessCognito/blob/main/flow-diagram.jpg)
## **SETUP**

<img src="https://github.com/farvath/ChessCognito/blob/main/setup.jpg" width="400px" height="400px" alt="alt text">

## **DEMONSTRATION**
[https://github.com/farvath/ChessCognito/blob/main/demo.jpg](https://youtu.be/DUXy-wxAJ5M)

## **ACKNOWLEDGEMENTS**

I give special thanks to David Mallasén Quintana. This project was made possible by Quintana's work: [LiveChess2FEN](https://github.com/davidmallasen/LiveChess2FEN/tree/master). LiveChess2FEN provided me with the foundation for chess-piece identification. The "models.zip" file (in "ChessPieceModelTraining/ModelTrainer") came directly from the LiveChess2FEN repository, and the "SqueezeNet1p1_model_training.ipynb" notebook (in "ChessPieceModelTraining/ModelTrainer") was written largely based on the work in "cpmodels" folder in the repository as well.
