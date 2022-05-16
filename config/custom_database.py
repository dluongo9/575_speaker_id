import pickle

from bob.db.base.tests.sample import Database
import os

FILE_EXTENSION = '.wav'

db = Database()

db.allfiles = [file[:-4] for file in os.listdir('../res') if file[-4:] == FILE_EXTENSION]
for sample in db.objects():
    print(sample)

all_samples = list(db.objects())
f = all_samples[0]  # get only sample 0
list_of_samples = [file.make_path('../res', FILE_EXTENSION) for file in all_samples]
with open("../databases/a_dumped_pickle", 'wb') as opened_file:
    pickle.dump(list_of_samples, opened_file)
print(f.make_path('../res', FILE_EXTENSION))
print(f.path)
print(all_samples)
