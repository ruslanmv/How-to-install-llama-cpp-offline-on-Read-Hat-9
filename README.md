# How to install llama.cpp on RedHat Linux 9 offline.


We are going first create a Python enviroment where we are going to get the dependencies.



## Computer with Internet

First we need to following the next steps in the computer with internet.

### Step 1: Update Your System

First, ensure your system is up to date:

```bash
sudo yum update
```

### Step 2: Install Dependencies

Python requires several development libraries and tools to be installed. You can install these using `yum`:

```bash
sudo yum groupinstall "Development Tools"
sudo yum install openssl-devel bzip2-devel libffi-devel zlib-devel
sudo yum install wget
```

### Step 3: Download Python 3.9.18 Source Code

Next, download the source code for Python 3.9.18:

```bash
cd /usr/src
sudo wget https://www.python.org/ftp/python/3.9.18/Python-3.9.18.tgz
```

### Step 4: Extract the Tarball

Extract the downloaded tarball:

```bash
sudo tar xzf Python-3.9.18.tgz
cd Python-3.9.18
```

### Step 5: Configure the Script

Run the configure script to prepare the build environment:

```bash
sudo ./configure --enable-optimizations
```

The `--enable-optimizations` flag will optimize the Python binary using profile-guided optimization (PGO), which can take a while but results in a faster Python interpreter.

### Step 6: Build and Install Python

Compile and install Python. You can specify the number of CPU cores to use for the build process with the `-j` flag:

```bash
sudo make altinstall -j 4
```

The `altinstall` command prevents the overwriting of the default system Python.

### Step 7: Verify the Installation

Once the installation is complete, verify that Python 3.9.18 is installed correctly:

```bash
python3.9 --version
```
![](assets/2024-07-22-20-55-44.png)
### Step 8: Set Up Virtual Environment (Optional but Recommended)

It's a good practice to use virtual environments to manage dependencies for different projects. You can set up a virtual environment using `venv`:

```bash
python3.9 -m venv myenv
```

Activate the virtual environment:

```bash
source myenv/bin/activate
```



1. **Updating Pip**: After setting up Python, you may want to update `pip` to the latest version:

    ```bash
    python -m pip install --upgrade pip
    ```




# llama python cpp



### Step 2: Install `pip-tools`

`pip-tools` is a package used to manage dependencies in a more controlled manner. Install it in your virtual environment:

```bash
pip install pip-tools
```

### Step 3: Create a Requirements File

Next, create a `requirements.txt` file with the dependencies for `llama.cpp`. For demonstration purposes, I'll assume that `llama.cpp` has specific dependencies. Create a file named `requirements.in` with the following content:

```txt
# requirements.in
llama.cpp
```

### Step 4: Compile Dependencies

Compile the `requirements.in` file into a `requirements.txt` file that includes all dependencies and their versions:

```bash
pip-compile requirements.in
```

This will generate a `requirements.txt` file with all the dependencies.

### Step 5: Download Dependencies

Use `pip` to download all the dependencies listed in the `requirements.txt` file into a folder:

```bash
mkdir llama_cpp_dependencies
pip download -r requirements.txt -d llama_cpp_dependencies
```

This command will download all the required packages into the `llama_cpp_dependencies` directory.

### Step 6: Create a Zip File

Zip the `llama_cpp_dependencies` folder:

```bash
zip -r llama_cpp_dependencies.zip llama_cpp_dependencies
```

Now you have a zip file (`llama_cpp_dependencies.zip`) containing all the dependencies required to install `llama.cpp`.

### Step 7: Transfer the Zip File to the Target System

Transfer the `llama_cpp_dependencies.zip` file to your RedHat Linux 9 system using a USB drive, SCP, or any other file transfer method.

### Step 8: Set Up Environment on the Target System

On your RedHat Linux 9 system, create a new virtual environment and activate it:

```bash
python3.9 -m venv myenv
source myenv/bin/activate
```

### Step 9: Install Dependencies Offline

Transfer the `llama_cpp_dependencies.zip` file to a suitable location on the RedHat Linux 9 system and unzip it:

```bash
unzip llama_cpp_dependencies.zip -d llama_cpp_dependencies
```

Navigate to the directory where the dependencies are located:

```bash
cd llama_cpp_dependencies
```

Install the dependencies from the local directory:

```bash
pip install --no-index --find-links=. -r ../requirements.txt
```

This command tells `pip` to install the packages from the local directory rather than searching online.

### Step 10: Install `llama-cpp-python`

Finally, install `llama-cpp-python`:

```bash
pip install llama-cpp-python
```

Since all the dependencies have already been installed, `pip` will not need to download anything from the internet.

### Summary

1. Set up and activate your virtual environment.
2. Install `pip-tools`.
3. Create a `requirements.in` file with the main package.
4. Compile the `requirements.in` file to `requirements.txt`.
5. Download all dependencies into a folder.
6. Zip the folder containing dependencies.
7. Transfer the zip file to the target system.
8. Set up a new virtual environment on the target system.
9. Unzip the dependencies and install them offline.
10. Install `llama-cpp-python`.
