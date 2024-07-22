#You should be on llama.cpp folder
import os
import shutil

# Define package directory
package_dir = 'llama_cpp_package'
binaries_dir = os.path.join(package_dir, 'bin')
os.makedirs(binaries_dir, exist_ok=True)

# List of compiled binaries
binaries = [
    'llama-convert-llama2c-to-ggml', 'llama-server', 'llama-simple', 'llama-speculative',
    'llama-tokenize', 'llama-export-lora', 'llama-train-text-from-scratch', 'llama-vdot',
    'llama-eval-callback', 'llama-gguf', 'llama-gguf-hash', 'llama-gguf-split',
    'llama-gritlm', 'llama-imatrix', 'llama-infill', 'llama-llava-cli', 'llama-lookahead',
    'llama-lookup', 'llama-lookup-create', 'llama-lookup-merge', 'llama-lookup-stats',
    'llama-parallel', 'llama-passkey', 'llama-perplexity', 'llama-q8dot', 'llama-quantize',
    'llama-quantize-stats', 'llama-retrieval', 'llama-save-load-state'
]

# Move binaries to the binaries directory
for binary in binaries:
    shutil.move(binary, os.path.join(binaries_dir, binary))

# Create the setup.py file
setup_code = """
from setuptools import setup, find_packages
import os

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join(path, filename))
    return paths

extra_files = package_files('bin')

setup(
    name='llama_cpp_package',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': extra_files,
    },
    data_files=[('', extra_files)],
    install_requires=[],
)
"""

# Write setup.py to the package directory
os.makedirs(package_dir, exist_ok=True)
with open(os.path.join(package_dir, 'setup.py'), 'w') as f:
    f.write(setup_code)


 # Move the wheel to a shared location (e.g., Google Drive)
import shutil

wheel_files = [f for f in os.listdir('dist') if f.endswith('.whl')]
for wheel_file in wheel_files:
    shutil.move(os.path.join('dist', wheel_file), '/content/' + wheel_file)    