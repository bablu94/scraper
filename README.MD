
## Requirements

- Python 3.9+
- FastAPI
- requests
- BeautifulSoup4
- python-dotenv
- pytest

## Setup

1. Clone the repository:

    ```sh
    git clone <repository-url>
    cd scraper
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add the base URL:

    ```env
    BASE_URL=https://dentalstall.com/shop/
    ```

## Running the Application

1. Start the FastAPI server:

    ```sh
    uvicorn app.main:app --reload
    ```

2. Make a POST request to start scraping:

    ```sh
    curl -X POST "http://127.0.0.1:8000/scrape?token=your_token" -H "Content-Type: application/json" -d '{"pages_limit": 1, "proxy": null}'
    ```

## Running the Tests

1. Run the tests using `pytest`:

    ```sh
    pytest
    ```

## Usage

- **Environment Variables**: Set the base URL and other configurations in the `.env` file.
- **Scraping**: Use the provided endpoint to start scraping with configurable parameters.
- **Testing**: Ensure all tests pass by running `pytest`.

