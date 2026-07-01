from django.core.management.base import BaseCommand
from apps.jobs.services.scraper.save import save_jobs


class Command(BaseCommand):
    help = "Scrape jobs and save them to the database"

    def handle(self, *args, **options):
        self.stdout.write("Starting job scraper...")

        save_jobs()

        self.stdout.write(
            self.style.SUCCESS("Jobs scraped successfully!")
        )