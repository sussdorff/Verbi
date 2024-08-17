# setup.py

import platform
import subprocess
from setuptools import setup, find_packages

def install_portaudio():
    if platform.system() == "Darwin":
        try:
            subprocess.check_call(["brew", "install", "portaudio"])
            print("PortAudio installed successfully via Homebrew.")
        except subprocess.CalledProcessError:
            print("Failed to install PortAudio. Please install it manually using 'brew install portaudio'")

install_portaudio()

setup(
    name='jarvis-voice-assistant',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'speechrecognition',
        'pygame',
        'openai',
        'groq',
        'deepgram-sdk',
        'python-dotenv',
        'colorama',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'jarvis=run_voice_assistant:main'
        ]
    },
    author='Prompt',
    author_email='engineerprompt@gmail.com',
    description='A modular voice assistant application with support for multiple state-of-the-art models.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/PromtEngineer/JARVIS-VoiceAssistant',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ],
    python_requires='>=3.10',
    include_package_data=True,
)
