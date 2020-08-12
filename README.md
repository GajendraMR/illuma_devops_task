# Illuma-devops-task

This is a Python Flask Web Application to find the Language of an Article or List of Articles. This application performs [web scraping](https://en.wikipedia.org/wiki/Web_scraping) on the provided URL/s and with the help of a [MeaningCloud's Language Detection API](https://www.meaningcloud.com/developer/language-identification), identifies th=o which language the Article belongs to and provides the result on the webpage in Table form.

File Structure:
```
  illuma_devops_task
  ├── Dockerfile
  ├── Illuma\ Offline\ Interview\ -\ DevOps
  │   └── illuma_devops_offsite_task_urls.csv
  ├── README.md
  ├── app.py
  ├── config.py
  ├── docker-compose.yml
  ├── requirements.txt
  ├── static
  │   └── style.css
  ├── templates
  │   ├── base.html
  │   ├── scrape_by_url.html
  │   └── welcome.html
  └── test_app.py
```

## Project Setup

### Pre-Requisite:
1. Docker & Docker-Compose (Download & Install from [here](https://www.docker.com/products/docker-desktop))
2. Browser to access - http://localhost:5000
3. CircleCI - Only needed if to test CI process

### Steps to Run the application
1. Clone the Project or download the zip file on to your local
`git clone https://github.com/GajendraMR/illuma_devops_task.git`
2. Create a `config.py` in the root folder and update the License key like below for [MeaningCloud's Language Detection API](https://www.meaningcloud.com/developer/language-identification)
```
license_key = "YOUR-KEY"
```
3. Verify docker is up and running.
4. Launch the application using docker-compose
`docker-compose up`
5. Two containers namely, redis & web starts up.
6. Once the containers are up and running, access the http://localhost:5000 on the browser for the UI.

### Working with UI
The webpage is created with the help bootstrap. The webpage provides two functionalities, and can be naigated to each functionality by clicking on the respective function located on the right side of Navbar (just beside the *Home* button)
1. __Find the Language of list of Articles__ : Here, you can upload a text/csv file containing a list of articles for which language has to be detected.
2. __Find the Language of an Article__ : Here, you can type in the valid URL of an article and click on start.

The results will displayed right below on the same page in a datatable format and looks like below
| Article       | Language      |
| ------------- |:-------------:|
| https://google.com	| English |
| https://imigrante.sef.pt | Portuguese |