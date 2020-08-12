# Illuma Offline Interview - DevOps



In this task, you will be provided a list of URLs ([illuma_devops_offsite_task_urls.csv](Illuma%20Offline%20Interview%20-%20DevOps/illuma_devops_offsite_task_urls.csv)) and you need to implement a continuous integration/continuous deployment (CI/CD) pipeline dockerising a Flask web application with the following functionalities: 

1. Iterate over the list of URLs, scrape it and obtain the content 
2. Detect the language of the the article by using the language identification service provided by [MeaningCloud](https://www.meaningcloud.com/) (free usage is available)
3. Cache scraping history to avoid duplications by an in-memory datastore (e.g. redis), you should consider docker compose to build a multi-container application

Notes

- Feel free to use any CI/CD tools (e.g. GitHub Actions, Jenkins, CircleCI) which you feel comfortable with
- You should consider continuous code testing in your CI/CD pipeline
- Please be aware the limitations of using the free service of MeaningCloud (e.g. the number of requests you can make per second)
- Please get to "production ready" as closely as possible
- Besides implementing the compulsory functionalities, please open your mind and invest your innovation
- Please submit your work as a zip file with git commit history
- Please provide a README document introducing your development (e.g. how to run and/or test your project)

You will be given 1 week to finish the task, but cumulatively you should try to complete the task in 3-4 hours.