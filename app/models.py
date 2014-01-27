from django.db import models

LECTURE = 'LEC'
SEMINAR = 'SEM'
PROJECT = 'PRJ'
WORKSHOP = 'WKS'
LAB = 'LAB'
COURSE_TYPES = (
    (LECTURE, 'Lecture'),
    (SEMINAR, 'Seminar'),
    (PROJECT, 'Project'),
    (WORKSHOP, 'APS Workshop'),
    (LAB, 'Lab')
)

class Professor(models.Model):
    name = models.CharField(max_length=50)
    department = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return str(name)

class Professor_Rating(models.Model):
    prof = models.ForeignKey('Professor')
    course = models.ForeignKey('Course')
    rating = models.FloatField()

    def __unicode__(self):
        return "Rating " + str(prof.name)

class Course(models.Model):
    course_id = models.IntegerField()
    course_type = models.CharField( max_length=3,
                                    choices=COURSE_TYPES,
                                    default=LECTURE)
    name = models.CharField(max_length=100)
    instructors = models.ManyToManyField('Professor')
    credits = models.FloatField()
    description = models.CharField(max_length=2000)
    additional_info = models.CharField(max_length=2000, blank=True, null=True)
    sections_info = models.CharField(max_length=2000, blank=True, null=True)
    catalogue = models.CharField(max_length=300)
    grades = models.CharField(max_length=300, blank=True, null=True)
    abreviation = models.CharField(max_length=50, blank=True, null=True)
    participants = models.CharField(max_length=10, blank=True, null=True)
    hours_per_week = models.CharField(max_length=10, blank=True,null=True)

    general_rating = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return str(name)