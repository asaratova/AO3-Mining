import os
from collections import Counter 
import matplotlib.pyplot as plt

valid_tags = ['Abduction',
 'Abuse',
 'Action/Adventure',
 'Age Difference',
 'Age Play',
 'Aged-Up Character(s)',
 'Alcohol',
 'Alpha/Beta/Omega Dynamics',
 'Alternate Canon',
 'Alternate Universe',
 'Ambiguity',
 'Angst',
 'Anxiety',
 'AO3 Tags - Freeform',
 'Art',
 'Asexuality Spectrum',
 'Asphyxiation',
 'Audio Content',
 'Awkwardness',
 'Badass',
 'Bathing/Washing',
 'BDSM',
 'Beds',
 'Birthday',
 'Biting',
 'Blood',
 'Bodily Fluids',
 'Bonding',
 'Bottoming',
 'Break Up',
 'Canon Related',
 'Canon Universe',
 'Character Study',
 'Chatting & Messaging',
 'Children',
 'Clothing',
 'Coercion',
 'Comfort',
 'Confessions',
 'Consent',
 'Crack',
 'Crimes & Criminals',
 'Crossovers & Fandom Fusions',
 'Crushes',
 'Crying',
 'Cuddling & Snuggling',
 'Dancing and Singing',
 'Dark',
 'Dating',
 'Death',
 'Deviates From Canon',
 'Disability',
 'Domestic',
 'Dorkiness',
 'Drabble',
 'Drama',
 'Dreams and Nightmares',
 'Drugs',
 'Education',
 'Enemies',
 'Everyone Is Alive',
 'Falling In Love',
 'Family',
 'Feelings',
 'Feels',
 'Female Characters',
 'Female Relationships',
 'Ficlet',
 'Fights',
 'Fingerfucking',
 'Firsts',
 'Fix-It',
 'Flashbacks',
 'Flirting',
 'Fluff',
 'Food',
 'Friendship',
 'Future',
 'Gender Related',
 'Getting Together',
 'Gore',
 'Happy Ending',
 'Harm to Children',
 'Hatred',
 'Heroes & Heroines',
 'Higher Education',
 'Historical',
 'Holidays',
 'Homophobia',
 'Horror',
 'Human',
 'Human/Monster Romance',
 'Humiliation',
 'Humor',
 'Hurt',
 'Hurt/Comfort',
 'I Wrote This Instead of Sleeping',
 '\"I\'m\" Sorry',
 'Idiots in Love',
 'Illnesses',
 'Implied/Referenced Character Death',
 'In Public',
 'Incest',
 'Infidelity',
 'Injury',
 'Inspired by...',
 'Intoxication',
 'Introspection',
 'Issues',
 'Jealousy',
 'Kinks',
 'Kissing',
 'Language',
 'LGBTQ Themes',
 'Light-Hearted',
 'Loss',
 'Love',
 'Making Out',
 'Manipulation',
 'Marriage',
 'Medical',
 'Memory Related',
 'Mental Health Issues',
 'Misunderstandings',
 'Modern Era',
 'Music',
 'My First...',
 'Mystery',
 'Mythical Beings & Creatures',
 'Non-Consensual',
 'Non-Sexual',
 'Not Beta Read',
 'Oblivious',
 'One Shot',
 'Orgasm',
 'Original Character(s)',
 'Out of Character',
 'Pain',
 'Panic',
 'Penises',
 'Pining',
 'Plot',
 'Podfic & Podficced Works',
 'Poetry',
 'Polyamory',
 'Porn',
 'Possessive Behavior',
 'Post-Canon',
 'Posted Elsewhere',
 'POV Multiple',
 'Praise Kink',
 'Pre-Canon',
 'Pregnancy',
 'Prompt Fill',
 'Protectiveness',
 'Reader-Insert',
 'Relationship(s)',
 'Religion',
 'Restaurants',
 'Romance',
 'Roughness',
 'Royalty',
 'Sad',
 'Science Fiction & Fantasy',
 'Secrets',
 'Self-Esteem',
 'Self-Harm',
 'Sex Work',
 'Sexual Content',
 'Sexual Inexperience',
 'Shapeshifting',
 'Sharing',
 'Short',
 'Slash',
 'Slice of Life',
 'Slow Build',
 'Smut',
 'Soulmates',
 'Spoilers',
 'Sports',
 'Substance Abuse',
 'Suicide',
 'Supernatural Elements',
 'Team',
 'Teasing',
 'Teenagers',
 'Tension',
 'Threesome',
 'Time Travel',
 'Topping',
 'Torture',
 'Trauma',
 'Tumblr',
 'Underage - Freeform',
 'Unrequited',
 'Violence',
 'Voyeurism',
 'War Weapons',
 'Weather',
 'Whump']

def filter(tag_list, valid = False):
    if valid:
        return [i for i in tag_list if i != "" and i != " " and i != "\n" and i in valid_tags] 
    return [i for i in tag_list if i != "" and i != " " and i != "\n"]

allTagsCnt = Counter()
validTagsCnt = Counter()

# with open("./data/30893183.txt") as f:
#     all_text = f.read()
#     freeform_index  = all_text.index("freeform:") + 9   # Account for length of freeform
#     fandom_index = all_text.index("fandom:")
#     freeform_tags = all_text[freeform_index:fandom_index]
#     tags_separated = freeform_tags.split("\n")
#     filtered_tags = filter(tags_separated)
#     cnt += Counter(filtered_tags)

x = []
y = []
numFiles = 0
for root, dirs, files in os.walk("./data"):
    numFiles = len(files)
    for file in files:
        if file[-3:] == "txt":
            with open(root + "/" + file) as f:
                all_text = f.read()
                freeform_index  = all_text.index("freeform:") + 9   # Account for length of freeform
                fandom_index = all_text.index("fandom:")
                freeform_tags = all_text[freeform_index:fandom_index]
                tags_separated = freeform_tags.split("\n")
                filtered_tags = filter(tags_separated, True)

                allTagsCntCur = Counter(filter(tags_separated))
                allTagsCnt += allTagsCntCur

                validTagsCntCur = Counter(filtered_tags)
                validTagsCnt += validTagsCntCur

                numValid = round(sum(validTagsCntCur.values()), 4)
                numTags = round(sum(allTagsCntCur.values()), 4)
                
                if numTags > 0:
                    x.append(file[:-4])
                    y.append(numValid / numTags)


print("Total # of Tags Found: ", sum(allTagsCnt.values()))
print("Total # of Valid Tags Found: ", sum(validTagsCnt.values()))
print("Total # of Files: ", numFiles)

# used to plot percent valid tags

fig, ax = plt.subplots()
ax.bar(x,y)
plt.setp( ax.xaxis.get_majorticklabels(), rotation=45, ha="right" )
plt.xticks(rotation = 45, size = 7)
plt.title("Percent of Tags that are Valid for Each Fanfiction")
plt.xlabel("Fanfiction ID")
plt.ylabel("Percentage of Valid Tags")
plt.savefig("percentValid_plot.png", bbox_inches='tight')


# Used to plot frequency of tags

x = []
y = []

for tag in validTagsCnt:
    x.append(tag)
    y.append(validTagsCnt[tag])

fig, ax = plt.subplots()
ax.bar(x,y)
plt.setp( ax.xaxis.get_majorticklabels(), rotation=45, ha="right" )
plt.xticks(rotation = 45, size = 7)
plt.title("Valid Tag Frequency for Subset of Fanfiction")
plt.xlabel("Tag Label")
plt.ylabel("Number of Times Each Tag Appeared")
plt.savefig("tagFrequency_plot.png", bbox_inches='tight')
