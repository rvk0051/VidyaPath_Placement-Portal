from .models import PlacedStudent
from django.db.models import Max, Count

def calculate_salary_distribution():
    max_salary = PlacedStudent.objects.aggregate(Max('salary_lpa'))['salary_lpa__max']

    if max_salary is None:  # If no data exists, return empty list
        return []

    salary_ranges = []
    range_size = 10  # Each salary range is 10 LPA
    for start in range(0, int(max_salary) + range_size, range_size):
        end = start + range_size
        count = PlacedStudent.objects.filter(salary_lpa__gte=start, salary_lpa__lt=end).count()
        salary_ranges.append({
            'salary_range': f"{start}-{end} LPA",
            'students_count': count
        })

    return salary_ranges