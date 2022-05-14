from dagster import repository

from news.jobs.link_scraper import scrape_link_job
from news.schedules.link_scraping_scheduler import scrape_link_schedule


@repository
def news_repository():
  """Repository of News scraping jobs, schedules

  Returns:
      RepositoryDefinition: Repository containing all jobs, schedules
  """
  return [scrape_link_job, scrape_link_schedule]
