from datetime import datetime
from typing import List, Dict, Any

class DataProcessor:
    @staticmethod
    def flatten_repo_data(raw_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Transforms nested API objects into a flat structure suitable for CSV.
        Focus: Extracting 'owner' login and formatting dates.
        """
        flattened_list = []
        
        for item in raw_items:
            # We select specific fields to maintain a strict schema
            clean_record = {
                "repo_id": item.get("id"),
                "name": item.get("name"),
                "full_name": item.get("full_name"),
                "owner_login": item.get("owner", {}).get("login"),  # Flattening nested dict
                "stars": item.get("stargazers_count", 0),
                "forks": item.get("forks_count", 0),
                "language": item.get("language", "Unknown"),
                "created_at": DataProcessor._format_date(item.get("created_at")),
                "updated_at": DataProcessor._format_date(item.get("updated_at")),
                "url": item.get("html_url")
            }
            flattened_list.append(clean_record)
            
        return flattened_list

    @staticmethod
    def _format_date(date_str: str) -> str:
        """Standardizes ISO 8601 strings to YYYY-MM-DD HH:MM:SS."""
        if not date_str:
            return ""
        try:
            # GitHub returns: 2024-01-30T12:00:00Z
            dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return date_str  # Return as-is if format differs
        
if __name__ == "__main__":
    # Mock data representing a tiny fragment of GitHub's response
    mock_raw = [{"id": 1, "name": "test-repo", "owner": {"login": "user1"}, "stargazers_count": 10, "created_at": "2024-01-01T10:00:00Z"}]
    processor = DataProcessor()
    clean = processor.flatten_repo_data(mock_raw)
    print(f"Cleaned Data: {clean}")