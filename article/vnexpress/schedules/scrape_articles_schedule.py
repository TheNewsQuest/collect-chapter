from dagster import (DefaultScheduleStatus, RunRequest, ScheduleDefinition,
                     get_dagster_logger, schedule)

from article.vnexpress.jobs.scrape_articles import \
    VNExpressScrapeArticlesJobFactory
from common.configs import DateFormats, VNExpressCategories
from common.configs.env import EnvVariables

CRON_EVERY_10_MINS = "*/10 * * * *"


def scrape_articles_schedule_factory(category: VNExpressCategories,
                                     **kwargs) -> ScheduleDefinition:
  """Factory for generating scraping articles schedule on category

  Args:
      category (VNExpressCategories): Category

  Returns:
      ScheduleDefinition: Schedule
  """
  # Pre-configure parameters for schedule
  scrape_articles_job_factory = VNExpressScrapeArticlesJobFactory()
  scrape_category_articles_job = scrape_articles_job_factory.create_job(
      category=category)
  default_status = DefaultScheduleStatus.RUNNING
  if EnvVariables.APP_ENV == "local":
    default_status = DefaultScheduleStatus.STOPPED
  execution_timezone = str(EnvVariables.SCHEDULE_TIMEZONE)

  @schedule(name=f"scrape_{category}_articles_schedule",
            cron_schedule=CRON_EVERY_10_MINS,
            job=scrape_category_articles_job,
            execution_timezone=execution_timezone,
            default_status=default_status,
            **kwargs)
  def _schedule(context):
    scheduled_date = context.scheduled_execution_time.strftime(
        DateFormats.YYYYMMDD)
    get_dagster_logger().info(
        f"Trigger schedule of scraping {category} articles on VNExpress at {scheduled_date}."
    )
    return RunRequest(run_key=None, tags={"date": scheduled_date})

  return _schedule
