from typing import TypeVar, Type, Generic, Union
import json
import os
import logging as log
from models.IModel import IModel
import discord

T = TypeVar('T', bound=IModel)

class Utils(Generic[T]):

    @staticmethod
    async def fromJson(file_name: Union[str, os.PathLike], obj_type: Type[T]) -> list[T]:
        """
        Returns: a list of objects read from json and built with the provided object type or None if empty or wrong format.

        Params:
            (str or os.PathLike) file_name: allows for string paths or os.PathLike paths.
            (generic) obj_type: type of object you want the json items to convert to.
        """
        try:
            with open(file_name, "r") as file:
                data = json.load(file)

            if not isinstance(data, list):
                raise ValueError("Json content must be a list of objects")

            return [obj_type(**item) for item in data]
        
        except FileNotFoundError as f:
            log.info(f"Json file not found: {f}")
            return None
        
        except (ValueError, TypeError) as e:
            log.info(f"Json error: {e}")
            return None
        

    @staticmethod
    async def toJson(file_name: Union[str, os.PathLike], objects: list[T]) -> bool:
        """
        Writes a list of objects to a json file at the provided path.

        Params:
            (str or os.PathLike) file_name: allows for string paths or os.PathLike paths.
            (list[T]) objects: list of objects to be converted to dictionaries and written to the json file.

        Returns:
            (bool): True if writing is successful, False if any error occurs.
        """
        try:
            
            data = [obj.to_dict() for obj in objects]
            
            with open(file_name, "w") as file:
                json.dump(data, file, indent=4)
            
            return True
        
        except Exception as e:
            print(f"An error occurred while writing to the json file: {e}")
            return False


    @staticmethod
    async def fromJsonNoObject(file_name: Union[str, os.PathLike]) -> dict:
        """
        Returns: a dictionary from a json file

        Params:
            (str or os.PathLike) file_name: allows for string paths or os.PathLike paths.
        """
        try:
            with open(file_name, "r", encoding='utf-8') as file:
                data = json.load(file)

            return data
        
        except FileNotFoundError as f:
            log.info(f"Json file not found: {f}")
            return None
        
        except (ValueError, TypeError) as e:
            log.info(f"Json error: {e}")
            return None
        
        
    @staticmethod
    async def toJsonNoObject(data: dict, file_name: Union[str, os.PathLike]) -> bool:
        """
        Writes a dictionary to a json file without wrapping it in an object.

        Params:
            data (dict): The dictionary to write to the json file.
            (str or os.PathLike) file_name: The filename where the data will be saved.
        
        Returns:
            bool: True if the writing was successful, False otherwise.
        """
        try:
            with open(file_name, "w", ensure_ascii=False) as file:
                json.dump(data, file)
            return True

        except (IOError, ValueError) as e:
            log.info(f"Error writing JSON to file: {e}")
            return False
        

    @staticmethod
    async def appendToJson(file_name: Union[str, os.PathLike], obj: T) -> bool:
        """
        Appends a single object to a json file. If the file does not exist or
        contains invalid JSON, it creates a new file with the object in a list.

        Params:
            (str or os.PathLike) file_name: allows for string paths or os.PathLike paths.
            (T) obj: the object to be converted to a dictionary and appended to the json file.

        Returns:
            (bool): True if the operation is successful, False otherwise.
        """
        try:

            with open(file_name, "r+") as file:

                try:
                    data = json.load(file)

                    if not isinstance(data, list):
                        raise ValueError("Json content must be a list of objects")
                    
                except (ValueError, json.JSONDecodeError):
                    log.info("Invalid JSON format detected. Creating a new list.")
                    data = []

                data.append(obj.to_dict())
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()

            return True

        except Exception as e:
            log.info(f"An error occurred while appending to the json file: {e}")
            return False