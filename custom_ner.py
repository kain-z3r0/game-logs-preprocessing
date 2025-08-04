import json
import spacy
import string
import random
from pathlib import Path
from spacy.lang.en import English
from spacy.pipeline import EntityRuler
from itertools import product
from faker import Faker

with open("./data/players.json") as f:
	players = json.load(f)


# nlp = spacy.load("en_core_web_lg")


file = Path("./data/test_data.txt")


text = file.read_text()

# A A Players
pairs = [f"{a} {b}" for a, b in product(string.ascii_uppercase, repeat = 2)]
players.extend(pairs)

low_pairs = [f"{a} {b}" for a, b in product(string.ascii_lowercase, repeat = 2)]
players.extend(low_pairs)

# Hyphen Players
fake = Faker()
last_names = [fake.last_name() for _ in range(1000)]
hyphens = []

for _ in range(500):
	initial = random.choice(string.ascii_uppercase)
	a, b = random.sample(last_names, 2)
	hyphens.append(f"{initial} {a}-{b}")

players.extend(hyphens)

# Number #34
nums = [f"#{num}" for num in range(500)]
players.extend(nums)

# Jrs
jrs = []
for _ in range(500):
	init = random.choice(string.ascii_uppercase)
	lname = random.choice(last_names)
	jrs.append(f"{init} {lname} Jr.")

players.extend(jrs)


# A Lastname
std = []
for _ in range(2000):
	init = random.choice(string.ascii_uppercase)
	last_name = random.choice(last_names)
	std.append(f"{init} {last_name}")

players.extend(std)

#======================================================================
#======================================================================
#======================================================================






def generate_rules(patterns):
	nlp = English()
	ruler = nlp.add_pipe("entity_ruler", config = {"validate": True})
	ruler.add_patterns(patterns)
	nlp.to_disk("rb_ner")


patterns = [{"label": "PERSON", "pattern": player} for player in players]

generate_rules(patterns)



def main():
	nlp = spacy.load("rb_ner")

	text = Path("./data/test_data.txt").read_text()

	doc = nlp(text)

	results = [ent.text for ent in doc.ents]

	print(results)








if __name__ == "__main__":
	main()