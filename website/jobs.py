# We cannot import the models directly because it will then run and result in
# a circular reference for imports.
import website

"""
Job scheduler for asynchronous jobs related to the website.
"""
class JobScheduler():

    def get_next_job(self):
        job = None
        instance = None

        jobs = website.models.AsyncJob.objects.filter(
            status=website.models.AsyncJob.STATUS_UNPROCESSED
        ).order_by('priority')


        if jobs.exists():
            job = jobs[0]

            # The AsyncJob doesn't really tell us anything.
            # We need the job instance as well.
            instance = job.get_instance()

        return (job, instance)

