
# Public Library Management System (Tkinter + Python)

A simple, local library management system built with **Tkinter** for the GUI and a lightweight **Python backend** for inventory, membership, and rental operations.

## Features
- Tkinter GUI with menu bar and quick-action launchers.
- In-memory registry for members and books with CSV persistence.
- Add, import, edit, delete, and search inventory.
- Check-out and check-in workflow with borrowing log.
- Simple reports viewer for the borrowing log.

## Repository Contents
- lms_backend.py : backend python code.
- lms_backend.py : python code that handles frontend GUI.
- import.csv : import file containing sample data outlining format required for import jobs.
- library.png : main menu background photo. 

## Installation
- git clone https://github.com/<your-org>/<your-repo>.git
cd <your-repo>
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

- libraryapp.py and lms_backend.py files must be in the same folder. 



## Running the App
- run the python libraryapp.py

- running the file will automatically generate the borrowinglog.csv and inventory.csv files. 
