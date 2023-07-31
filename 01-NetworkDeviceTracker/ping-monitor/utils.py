import logging
import pandas as pd
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('Log')


class FileHandler:
    """
    File Handler to read and write files based on type
    Supports: json, csv
    """

    def __init__(self, filepath: str, *, default_data: str, file_type: str = 'json') -> None:
        """
        Initiate File Handler with Specific file
        Args:
            filepath: Full Path of the file
            default_data: Default Data to be inserted in case of file do not exist
            file_type: Type of the file to create (json,csv)
        """
        self.filepath: str = filepath
        self.file_type: str = file_type

        # Check if File Exists or Not
        if not os.path.isfile(filepath):
            logging.info(f"{filepath} Not Found \n Creating... {filepath}")
            file = open(filepath, 'a')
            file.write(default_data)
            file.close()

    def read_file(self) -> pd.DataFrame:
        """
        Read Contents of a file
        Returns: Pandas DataFrame for the data
        """
        match self.file_type:
            case 'json':
                return pd.read_json(self.filepath)
            case 'csv':
                return pd.read_csv(self.filepath)

    def rewrite_file(self, data) -> str | None:
        """
        Writing Data to the File
        Args:
            data: any
        Returns:

        """
        match self.file_type:
            case 'json':
                return pd.DataFrame(data).to_json(self.filepath, orient="records")
            case 'csv':
                return pd.DataFrame(data).to_csv(self.filepath, mode='a', header=False, index=False, )
