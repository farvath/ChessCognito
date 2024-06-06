"""This module contains the `delete()` helper function."""


import os


def delete(filename: str):
    """Delete a file.

    This function constantly tries deleting a file until the file is
    deleted.

    :param filename: Filename of the file to be deleted.
    """
    successfullyDeleted = False
    while not successfullyDeleted:
        try:
            os.remove(filename)
            successfullyDeleted = True
        except PermissionError:
            pass
