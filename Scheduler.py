import schedule
import time
import GradeTracker


def job():
    GradeTracker.check_grades()

schedule.every(5).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
