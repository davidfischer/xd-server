from django.db import models


class Publication(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Crossword(models.Model):
    publication = models.ForeignKey(Publication)
    name = models.CharField(max_length=255, help_text='Crossword name')
    slug = models.SlugField(unique=True)
    author = models.CharField(max_length=255)
    editor = models.CharField(max_length=255)
    date = models.DateField()
    grid = models.TextField()
    # TODO: Rebus

    def __str__(self):
        return self.name


class Clue(models.Model):
    crossword = models.ForeignKey(Crossword)
    clue = models.CharField(max_length=255, db_index=True)
    answer = models.CharField(max_length=255, db_index=True)
    number = models.PositiveIntegerField()
    direction = models.CharField(choices=(('A', 'Across'), ('D', 'Down')), max_length=10)

    def __str__(self):
        return self.clue

    def pos(self):
        return '{}{}'.format(self.direction, self.number)
