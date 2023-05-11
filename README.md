# Box-Office-Database

This Python script implements a movie database management system using MySQL and PrettyTable. It allows users to perform various operations such as adding movies, updating box office figures, searching for movie details, and more.

## Getting Started

To run this code, you need to have MySQL and the PrettyTable library installed. Follow the steps below to set up the environment:

1. Install MySQL on your system if you haven't already.
2. Install the `mysql-connector-python` library by running the command: `pip install mysql-connector-python`.
3. Install the `prettytable` library by running the command: `pip install prettytable`.

## Usage

Once you have set up the environment, follow these steps to use the movie database management system:

1. Run the script in a Python environment.
2. You will be presented with a menu-driven interface where you can choose different options by entering the corresponding number.
3. Each option performs a specific operation such as displaying database features, adding movies, updating figures, searching for movies, and more.
4. Follow the instructions provided by the script to interact with the database and perform the desired operations.
5. Enter '#' to exit the script.

## Dependencies

The following libraries are required to run this code:

- MySQL Connector/Python: [https://pypi.org/project/mysql-connector-python/](https://pypi.org/project/mysql-connector-python/)
- PrettyTable: [https://pypi.org/project/prettytable/](https://pypi.org/project/prettytable/)

## Notes

- This code assumes that you have a local MySQL server running with the appropriate credentials. Modify the connection details in the code if necessary.
- The database schema includes two tables: `nett_gross` and `footfalls`. You can modify the table structure as needed.
- The box office figures (nett gross and footfalls) are assumed to be in crores.


