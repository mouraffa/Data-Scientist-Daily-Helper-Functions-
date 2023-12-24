# this helper function will foucus on Data preprocessing , especially for Images
import os
import shutil
from tqdm import tqdm  # Assuming you have tqdm installed for the progress bar
import cv2


def copy_images(source_folder, target_folder):
    """
    Copy images from subfolders to a target folder.

    Parameters:
    - source_folder (str): The path to the folder containing subfolders with images.
    - target_folder (str): The path to the folder where the images will be copied.

    Returns:
    None

    Example:
    ```python
    source_path = "/path/to/source/folder"
    target_path = "/path/to/target/folder"
    copy_images(source_path, target_path)
    ```
    """
    # Iterate through all subfolders in the source folder
    for root, dirs, files in tqdm(os.walk(source_folder), desc="Copying Images"):
        for file in files:
            # Check if the file is an image (you can customize this condition)
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                # Create the target folder if it doesn't exist
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)

                # Build the new filename using the subfolder name
                subfolder_name = os.path.basename(root)
                new_filename = f"{subfolder_name}_{file}"

                # Construct the full paths for source and target files
                source_path = os.path.join(root, file)
                target_path = os.path.join(target_folder, new_filename)

                # Copy the file to the target folder
                shutil.copy2(source_path, target_path)
                # Uncomment the next line if you want to print each copy operation
                # print(f"Copied: {file} to {new_filename}")


def rename_subfolders(folder_path, prefix='video_'):
    """
    Rename subfolders in a given folder with a specified prefix and index.

    Parameters:
    - folder_path (str): The path to the folder containing subfolders to be renamed.
    - prefix (str, optional): The prefix to be added to the new subfolder names. Default is 'video_'.

    Returns:
    None

    Example:
    ```python
    folder_directory = "/path/to/folder"
    new_prefix = "new_prefix_"
    rename_subfolders(folder_directory, new_prefix)
    ```
    """
    try:
        subfolders = [f.path for f in os.scandir(folder_path) if f.is_dir()]
        subfolders.sort()  # Sort subfolders to ensure the correct order

        for index, old_name in enumerate(subfolders, start=1):
            new_name = os.path.join(folder_path, f"{prefix}{index}")
            os.rename(old_name, new_name)
            # Uncomment the next line if you want to print each rename operation
            # print(f"Renamed: {old_name} -> {new_name}")

        print("All subfolders renamed successfully.")
    except OSError as e:
        print(f"Error: {e}")

def frames_to_video(frames_folder, output_video_path, fps=30):
    """
    Convert a sequence of image frames in a folder to a video.

    Parameters:
    - frames_folder (str): The path to the folder containing image frames.
    - output_video_path (str): The path to save the output video.
    - fps (int, optional): Frames per second for the output video. Default is 30.

    Returns:
    None

    Example:
    ```python
    frames_directory = "/path/to/frames"
    output_video = "/path/to/output/video.mp4"
    frames_to_video(frames_directory, output_video, fps=24)
    ```
    """
    # Get the list of image files in the frames folder
    image_files = [f for f in os.listdir(frames_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    # Sort the image files to ensure the correct order
    image_files.sort()

    # Get the dimensions of the first image to set video size
    first_image_path = os.path.join(frames_folder, image_files[0])
    first_image = cv2.imread(first_image_path)
    height, width, _ = first_image.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use appropriate codec based on file extension
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    # Iterate through image files and write frames to video
    for image_file in image_files:
        image_path = os.path.join(frames_folder, image_file)
        frame = cv2.imread(image_path)
        video_writer.write(frame)

    # Release the VideoWriter object
    video_writer.release()
