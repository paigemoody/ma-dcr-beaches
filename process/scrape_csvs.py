import os
import requests

class CSVDownloader:
    def __init__(self, year, start_month=5):
        self.year = year
        self.start_month = start_month
        self.current_month = start_month
        self.current_day = 1

    def fetch_csv(self, url, local_filename):
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(local_filename, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {local_filename}")
        except Exception as e:
            print(f"Failed to download {local_filename}: {str(e)}")

    def download_csvs(self):
        while self.current_month <= 12:  # Loop through months until December
            month_str = str(self.current_month).zfill(2)  # Zero-padding for month
            day_str = str(self.current_day).zfill(2)  # Zero-padding for day
            # url=   "https://www.mass.gov/files/csv/2023-08/BeachPostingTbl-08-31pm.csv"
            url = f"https://www.mass.gov/files/csv/{self.year}-{month_str}/BeachPostingTbl-{month_str}-{day_str}pm.csv"
            filename = url.split('/')[-1]
            filepath = os.path.join("process", "outputs", filename)
            
            # Check if the file exists before downloading
            self.fetch_csv(url, filepath)

            # Increment the day and month
            if self.current_day < 31:
                self.current_day += 1
            else:
                self.current_day = 1
                self.current_month += 1

if __name__ == "__main__":
    year = 2023
    downloader = CSVDownloader(year)
    downloader.download_csvs()
