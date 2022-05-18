from dagster import repository

from vnexpress.jobs.scrape import scrape_business, scrape_life, scrape_news


@repository
def vnexpress_repository():
  """Repository of VNExpress scraping jobs, schedules

  Returns:
      RepositoryDefinition: Repository containing all jobs, schedules
  """
  return [scrape_news, scrape_business, scrape_life]
