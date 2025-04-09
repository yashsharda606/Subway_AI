# subwAI - AI Plays Subway Surfers

**subwAI** is a project that demonstrates how to train an artificial intelligence to play the popular endless runner game Subway Surfers. It utilizes a supervised machine learning approach, where the AI learns by imitating human gameplay. A convolutional neural network (CNN) is employed for image classification, enabling the AI to understand the game screen and make informed decisions.

This project achieved a good prediction accuracy of 85% using a CNN architecture comprising convolutional layers, average pooling, dense layers, dropout, and an output layer. Data augmentation techniques, specifically horizontal mirroring, doubled the dataset size and further enhanced the robustness of the trained model. The resulting AI is capable of playing the game for extended periods (over a minute regularly) and effectively navigates common in-game obstacles. Interestingly, the AI's unconventional exploration led to the discovery of an unexpected in-game glitch!



## Description/Usage

This repository provides all the necessary scripts to build and run your own Subway Surfers playing AI. Here's a breakdown of the available functionalities:

**Data Gathering:**

1.  **Run the data gathering script:**
    ```bash
    python ai.py gather
    ```
    This will start the game (ensure Subway Surfers is installed and the path in `game.py` is correct) and capture rapid screenshots of the game screen. The captured images, along with the corresponding action you take (jump, roll, left, right, no action), will be saved into separate folders (`down`, `left`, `noop`, `right`, `up`) within the `images` directory.
2.  **Quit the gathering process:** Press `q` or `esc` during gameplay.

**Model Training:**

1.  **Train the AI model:**
    ```bash
    python ai.py train
    ```
    This script will train the neural network (defined in the `get_model()` function within `ai.py`) using the image dataset collected in the `images` directory.
2.  **Load a preloaded dataset (optional):** If you have previously saved a preprocessed dataset for a specific image width, you can load it during training:
    ```bash
    python ai.py train load <image_width>
    ```
    Replace `<image_width>` with the width (and height, as they are assumed to be equal) used when the preloaded dataset was saved. The preloaded data should be located in the `dataset_preloaded` directory.

**Data Augmentation:**

1.  **Augment the dataset:**
    ```bash
    python data.py
    ```
    This script will double the size of your training dataset by horizontally flipping each existing image. It will also automatically adjust the labels for mirrored actions (e.g., a flipped 'left' action will be relabeled as 'right'). The augmented images will be saved in new `_flipped` subdirectories within the `images` directory.

**Model Inspection and Label Correction:**

1.  **Check model predictions and correct labels:**
    ```bash
    python check_predictions.py
    ```
    This script allows you to review individual images from your training dataset and see what the currently trained model predicts for them, along with the prediction certainty. This is useful for identifying instances where the player might have made an incorrect action during data gathering. You can interact with the script using the following keys:
    * `y`: Move to the next image.
    * `n`: Delete the current image.
    * `w`: Move the current image to the 'up' folder.
    * `a`: Move the current image to the 'left' folder.
    * `s`: Move the current image to the 'down' folder.
    * `d`: Move the current image to the 'right' folder.
    * `esc`: Terminate the program.

**Image Sorting (Utility):**

1.  **Sort images (if order is changed):**
    ```bash
    python image_sort.py
    ```
    Run this script if the order of images within the action folders has been unintentionally altered. It helps ensure consistency in the dataset.

**Letting the AI Play:**

1.  **Run the AI to play the game:**
    ```bash
    python ai.py play
    ```
    This will load the trained model (the Sequential model which is the CNN) and start the game. The AI will then use its predictions to control the game.
2.  **Quit the AI:** Press `q` or `esc` during gameplay.
3.  **Save screen recording (after run):** After the game ends, you will be prompted to save a screen recording of the run. Press `y` to save or `n` to skip.
4.  **Automatic saving of long runs:** To automatically save recordings of runs longer than 40 seconds, run the script with the `auto` argument:
    ```bash
    python ai.py play auto
    ```

## Additional Information

* **`recordings` folder:** This directory stores the screen captures of the AI's gameplay. You can review these recordings to observe the AI's actions and the model's predictions for each frame. The frame rate of the recording is also indicated.
* **`models` folder:** This is where your trained AI models are saved. The `Sequential` subdirectory will contain the best-performing CNN model. You will also find visualizations of the CNN architecture (`architecture.png`) and a text file (`report.txt`) containing details about the model's layer configurations, training accuracy, and loss. While the CNN (`Sequential()` model) provides the best results, you can potentially experiment with other simpler machine learning models (commented out in `ai.py`).
* **`models\Sequential\model.keras`:** This is the saved file for the trained Convolutional Neural Network model.
* **`dataset_preloaded` folder:** This directory is used to store preprocessed datasets (if you choose to load and save them).

By following these steps, you can build, train, and deploy your own AI to play Subway Surfers! Remember to adjust file paths and experiment with different parameters to potentially improve the AI's performance.
