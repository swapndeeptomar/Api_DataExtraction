import os
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
class GitHubClient:
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.token = os.getenv("GITHUB_TOKEN")
        self.session = self._path_session()

    def _path_session(self) -> requests.Session:
        """Configures a session with retry logic and headers."""
        session = requests.Session()
        
        # Industry Standard: Exponential Backoff
        # Retries on 500 (Internal Server Error), 502 (Bad Gateway), 
        # 503 (Service Unavailable), and 504 (Gateway Timeout).
        retry_strategy = Retry(
            total=3,
            backoff_factor=1, # Waits 1s, 2s, 4s between retries
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        
        # Add Authentication if token exists
        if self.token:
            session.headers.update({"Authorization": f"token {self.token}"})
        
        # Identify your bot (GitHub requirement)
        session.headers.update({"Accept": "application/vnd.github.v3+json"})
        
        return session

    def fetch_repositories(self, query: str = "language:python", page: int = 1):
        """Fetches a single page of repositories."""
        endpoint = f"{self.base_url}/search/repositories"
        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "page": page,
            "per_page": 30
        }
        
        try:
            response = self.session.get(endpoint, params=params, timeout=10)
            
            # Handle Rate Limiting specifically
            if response.status_code == 403:
                print(f"⚠️ Rate limit hit. Reset at: {response.headers.get('X-RateLimit-Reset')}")
                return None, None
            
            response.raise_for_status()
            
            # Return the JSON data and the pagination link headers
            return response.json(), response.links
            
        except requests.exceptions.RequestException as e:
            print(f"❌ API Error on page {page}: {e}")
            return None, None
        

if __name__ == "__main__":
    client = GitHubClient()
    data, links = client.fetch_repositories()
    if data:
        print(f"✅ Success! Found {data['total_count']} repositories.")
        print(f"🔗 Next page available: {'next' in links}")