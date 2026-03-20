# File: voter_analytics/models.py
# Author: Esha Wadher (eshaaw@bu.edu), 03/20/2026
# Description:
# The Voter model represents a registered voter in Newton, MA.
# It stores personal information (name, date of birth), residential
# address etc.

from django.db import models


# Create your models here.
class Voter(models.Model):
    """store and represent the data from one registed voted in Newton, MA
    last nae, first name, residential address, street number, street name, etc., dob,
     zip code, party, prescint number, data of registration etc."""

    # identification
    last_name = models.TextField()
    first_name = models.TextField()

    # address
    street_number = models.TextField()
    street_name = models.TextField()
    apartment_number = models.TextField(blank=True)
    zip_code = models.TextField()

    # registration info
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.IntegerField()

    # election participation
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)

    voter_score = models.IntegerField(default=0)

    def __str__(self):
        """return a string representation of this mdoel instance"""
        return f"{self.first_name} {self.last_name}, {self.street_number} {self.street_name}, {self.party_affiliation.strip()}"


def load_data():
    """load voted data from the file into the db"""
    Voter.objects.all().delete()
    filename = "/Users/eshawadher/Desktop/newton_voters.csv"
    f = open(filename)
    f.readline()  # discard headers

    for line in f:
        fields = line.split(",")

        try:
            voter = Voter(
                last_name=fields[1].strip(),
                first_name=fields[2].strip(),
                street_number=fields[3].strip(),
                street_name=fields[4].strip(),
                apartment_number=fields[5].strip(),
                zip_code=fields[6].strip(),
                date_of_birth=fields[7].strip(),
                date_of_registration=fields[8].strip(),
                party_affiliation=fields[9],  # keep spacing intact
                precinct_number=fields[10].strip(),
                v20state=fields[11].strip() == "TRUE",
                v21town=fields[12].strip() == "TRUE",
                v21primary=fields[13].strip() == "TRUE",
                v22general=fields[14].strip() == "TRUE",
                v23town=fields[15].strip() == "TRUE",
                voter_score=int(fields[16].strip()),
            )

            voter.save()
        except:
            print("Something went wrong!")
            print(f"Skipped: {fields}")
    print(f"Done. Created {len(Voter.objects.all())} Voters.")
