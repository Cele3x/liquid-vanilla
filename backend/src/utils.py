from typing import Any, Dict, List
from bson import ObjectId
from bson.errors import InvalidId

def convert_object_ids(data: Dict[str, Any], field_paths: List[str]) -> Dict[str, Any]:
    """
    Recursively converts string IDs to ObjectIds based on provided field paths.

    @param data: Dictionary containing data to process
    @param field_paths: List of dot-notated paths to fields that need conversion
    @return: Dictionary with converted ObjectIds
    @raise ValueError: If invalid ObjectId string is encountered
    """
    def convert_value(value: Any) -> Any:
        """Helper function to convert a single value to ObjectId."""
        if isinstance(value, str):
            try:
                return ObjectId(value)
            except InvalidId as e:
                raise ValueError(f"Invalid ObjectId format: {e}")
        elif isinstance(value, list):
            return [convert_value(item) for item in value]
        return value

    def convert_path(current_data: Any, path_parts: List[str]) -> Any:
        if not current_data:
            return current_data

        if not path_parts:
            return convert_value(current_data)

        current_field = path_parts[0]
        remaining_path = path_parts[1:]

        if isinstance(current_data, dict):
            if current_field in current_data:
                current_data[current_field] = convert_path(
                    current_data[current_field],
                    remaining_path
                )
        elif isinstance(current_data, list):
            return [convert_path(item, path_parts) for item in current_data]

        return current_data

    result = data.copy()
    for field_path in field_paths:
        parts = field_path.split('.')
        result = convert_path(result, parts)

    return result