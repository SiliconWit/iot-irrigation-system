## How to Run and Upload Code to STM32 Bluepill

- In PlatformIO project, there is a new file named pio_upload_script.py in the root directory of the project.
- To run the script, open the PlatformIO terminal (not system terminal).
- The vs code platform io terminal button will navigate and open the project directory.
- Just run `$ python pio_upload_script.py`

**OR**

## Navigate to the project directory
cd /path/to/your/project

### Clean the project
pio run --target clean

### Build the project
pio run

### Upload the code
pio run --target upload

