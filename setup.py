"""Setup script for AI Task Planning Agent."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ai-task-planning-agent",
    version="1.0.0",
    author="CVeSS",
    description="An intelligent AI-powered personal task planning and scheduling assistant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CVeSS/AI_Agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Scheduling",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "ai-agent=main:app",
        ],
    },
    include_package_data=True,
    keywords="ai planning scheduling calendar productivity task-management machine-learning",
    project_urls={
        "Bug Reports": "https://github.com/CVeSS/AI_Agent/issues",
        "Source": "https://github.com/CVeSS/AI_Agent",
        "Documentation": "https://github.com/CVeSS/AI_Agent/blob/main/USAGE_GUIDE.md",
    },
)
