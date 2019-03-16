import datetime
from pathlib import Path
import re

from django.core.management.base import BaseCommand, CommandError

from crossword.models import Publication, Crossword, Clue


class Command(BaseCommand):
    help = 'Import an XD file into the database'

    def add_arguments(self, parser):
        parser.add_argument('xdfile', nargs='+', type=str)

    def xdfile_parser(self, fd):
        retval = {'clues': []}

        metadata, grid, clues = fd.read().split('\n\n\n')

        # metadata
        for line in metadata.splitlines():
            key, value = line.split(': ', maxsplit=1)
            retval[key.strip().lower()] = value.strip()

        # grid
        retval['grid'] = grid.strip()

        # clues
        for clueline in clues.splitlines():
            if not clueline:
                continue

            match = re.match(r'(?P<direction>[AD])(?P<number>\d+)\. (?P<clue>.+) ~ (?P<answer>.+)', clueline)
            if not match:
                self.stderr.write('Failed to parse clue "{}"'.format(clueline))

            retval['clues'].append(match.groupdict())

        return retval

    def handle(self, *args, **options):
        for xdfile in options['xdfile']:

            path = Path(xdfile)

            # Assumes pubid is first 3 chars of the filename
            xword_slug = path.stem
            pub_slug = path.stem[:3]
            publication = Publication.objects.filter(slug=pub_slug).first()
            if not publication:
                self.stderr.write('Publication matching {} not found'.format(pub_slug))
                continue

            try:
                with open(xdfile, 'r', encoding='utf-8') as fd:
                    data = self.xdfile_parser(fd)

                    crossword = Crossword(
                        publication=publication,
                        slug=xword_slug,
                        name=data['title'],
                        author=data['author'],
                        editor=data['editor'],
                        grid=data['grid'],
                        date=datetime.datetime.fromisoformat(data['date']).date(),
                    )
                    crossword.save()

                    for clue_data in data['clues']:
                        clue = Clue(
                            crossword=crossword,
                            direction=clue_data['direction'],
                            number=clue_data['number'],
                            clue=clue_data['clue'],
                            answer=clue_data['answer'],
                        )
                        clue.save()
            except IOError:
                self.stderr.write('Failed to find file {}'.format(xdfile))

        self.stdout.write(self.style.SUCCESS('Success'))
