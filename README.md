# Loblaw SRE Assignment Overview

## Installation Instructions

### Prerequisites

- Python 3 version 3.8.2
  - `venv` for virtual environment management
  - `pip` version 20.0.2

### Virtual Environment Instructions

#### Initial Installation

Activate the virtual environment

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

#### Useful virtual environment commands

Export dependencies

```bash
pip freeze > requirements.txt
```

Deactivate the virtual environment

```bash
deactivate
```

## Program Execution

Run the analysis using the following commands

```bash
./analysis.py <path-to-dataset.csv> <optional: output-file-path.csv>
# or
python analysis.py <path-to-dataset.csv> <optional: output-file-path.csv>
```

Usage

```text
usage: analysis.py [-h] [-o] input_csv_path

positional arguments:
  input_csv_path  The path to the csv containging the image dataset.

optional arguments:
  -h, --help      show this help message and exit
  -o, --output    The filename for the output csv.
```

## Output

- CSV file will need to have 4 fields (image1, image2, similar, elapsed).
- The total amount of records is the same as the input file.
- Scoring algorithm is based on visual appearance not binary contents.
  - A value of `0` indicates a perfect match.
  - Any value above indicates a difference in pixels between both images. Using the Mean Square Error cost function.
  - Does not calculate a similarity score for images of different sizes.
- `elapsed` indicates the time to compute each score

## Testing

In order to test the functionality of the program, you can run the following test suite to make sure it matches with the pre-tested output csv.

```bash
./test_analysis.py
# or
python test_analysis.py
```

## Important Considerations

- Portability - Usage on MacOS and Windows
  - The usage of the application on any operation system, be it unix based on Windows based, are the same. The application takes care of the path differences between operating sytem through the use of the `pathlib` library.
  - If a more universal solution is required, then a suggestion would be to use a containerized environment such as a Docker container. The overhead of this is large for such a small application, but it would depend on the needs of the end-user and its deployment strategy.
- How do you know if your code works?
  - The validity of my code can be confirmed through the use of my integration testing. My integration test confirms that the entire analysis function returns the pre-tested output in the requested requested data format, csv. The use of multiple images with minor variations test the potential differences in images that the program might face in its software lifecycle. Such variations include: size differences (shape), photo alterations, different formats of the same image.
- How are you going to teach Bjorn how to use the program?
  - My approach to teaching Bjorn how to use the program depends entirely on the skill set that he has available. Based on that skll set, I would pair with Bjorn and walk him through a bird-eye view of the program's functionality without diving into the specifics of the code. The reason for this is to account for no prior knowledge and a business application background.
  - I would first help him setup his virtual environment for the application and explain it's importance. If his needs do not require a virtual environment due to only needing the application itself, I would help him setup a global installation for future ease of use.
  - Once the environment is setup, I would walk through the various optional commandline argument and explain the reasonable defaults that come out of the box. Such reasonable assumptions include: file path defaults and file names.
  - When it comes to the output, I would have to teach Bjorn how the scoring algorithm considers different images. These measures are outlined in the `README.md`. Such measures include; a similarity score of `0`, and the handling of different file formats and sizes.
  - Once a general understanding of the program is achieved, I would explain how to test the program, using the test suite, if he were ever to belive that the program is malfunctioning.
  - I would also walk him through the `README.md` document in an effort to teach him how to undestand the program's changelog and increasing feature list.
- Your manager Jeanie is assigning you to a different task and is making Ferris the maintainer of your application. How do you make sure he succeeds?
  - First and foremost, a transition of knowledge meeting is required in order to aid Ferris to assume ownership of the project. In this meeting a demo of the project as well as its stakeholders and their requirements is required to ensure a technical and business transition of information.
  - Next, the most valuable piece of information for any inherited project is the documentation associted with said project. This will allow for the explanation of anything that was not explicitly stated in the transition meeting.
  - Lastly, in the time following the transfer, a point of contact must be maintained in order to ensure that any lingering questions not answered by the previous points are addressed.
- How are you ensuring Bjorn gets the latest version of your application?
  - First and foremost, the delivery of the application entirely depends on the end-user. If Bjorn is assumed to have prior coding knowledge and is simply a business end-user, then a reasonable solution were to have a provisioning system such as `Ansible` deploy the application on all the required systems company-wide. 
  - Another potential solution were to be a stateless internal solution where the employee could submit their `csv` data onto a serverless application and simply expect the output csv. This solution is mostly viable if the image dataset is stored in a database with a possible connection to the application.
  - Any of the aforementioned deployment strategies are dependent on the current infrastructure in place and the requirements of the end-user.
  - It goes without saying but a CI/CD pipeline is required for the deployment of such an application. This would ensure the that the end-user receives the appropriate application updates seemlessly with the approrpriate testing.

## Design and Implementation

- Initial planning of requirements
  - During the initial planning phase there was two methods that were considered, a dictionary based solution and a data-science based approach using `Python Pandas`
  - The reason for ultimately choosing `pandas` was due to its widepread usage within the data science community which excels that analysis of large datasets. Creating an inhouse custom solution might create short terms benefits and potential faster computer, but this is heavily outweighed by the benefit of using a standard method of analysis. Using `pandas` allows for an easier transfer of knowledge between maintainers and allows it to receives updates without too much engineering effort on the maintainer through optimizations of the library itself.
- Scoring algorithm
  - This portion of the design was one of the most interesting portions of the assignment. There are multiple ways of scoring image similarity as this is a common problem for the machine-learning field currently due to computer vision.
  - As per this following [article](https://towardsdatascience.com/image-classification-using-ssim-34e549ec6e12), there are two main methods for comptuting a similarity score; using a Mean Square Error (MSE) and Structural Similarity Index (SSIM).
  - The choice to choose Mean Square Error came about by understanding the needs of the business. The requirements stated in the document, outline that the score needs to have a score of 0 when a match is detected. Such a scale is achieve using MSE, but not with SSIM due to its scale returning values between -1 and 1.
  - A raw comparison between algorithms clearly shows the SSIM is superior due to its inate ability to better compare images of different sizes as its look for similarities rather than differences (MSE).
  - The main pitfall of MSE is its inability to compare images of different sizes and its non-uniform scale which does not have a clear maximum values as it is a function of the shape of the images. 
  - Future improvements of this program would entail research of different algorithms and bypassing the limitations of MSE, meanwhile conserving the business requirements indicating that 0 is a match.
  - Currently, the program addresses this by not giving a score to images of different sizes. This should be addresses in future iterations. 
  - I have provdided a normalization method in an attempt to standardize the output of the `similar` score between 0 and 1. The problem with this is that it is entirely depending on the dataset as it uses `min-max` normalization. For this reason, I have chosen to include the function by not enable it.
- Output
  - The output was very much based on the requirements specific in the document.
  - The choice for OS-agonostic path and file access is to allow for cross-platform usage.
