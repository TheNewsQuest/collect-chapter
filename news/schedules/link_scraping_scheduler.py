from dagster import DefaultScheduleStatus, ScheduleDefinition
from news.jobs.link_scraper import scrape_link_job

scrape_link_schedule = ScheduleDefinition(
    job=scrape_link_job,
    cron_schedule="*/1 * * * *",
    default_status=DefaultScheduleStatus.RUNNING)
