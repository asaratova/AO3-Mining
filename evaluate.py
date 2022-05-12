import os
from collections import Counter
from xml.sax.saxutils import prepare_input_source
import matplotlib.pyplot as plt
import math
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_predict
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from joblib import dump, load


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
# valid_tags_lower = [word.lower() for word in valid_tags]
num_valid_tags = len(valid_tags)
tag_dict = dict([(w, i) for (i, w) in enumerate(valid_tags)])


def filter(tag_list, valid=True):
    if valid:
        return [i for i in tag_list if i != "" and i != " " and i != "\n" and i in valid_tags]
    return [i for i in tag_list if i != "" and i != " " and i != "\n"]

def filterData():
    numFiles = 0
    numRemoved = 0
    for root, _, files in os.walk("./data"):
        numFiles = len(files)
        for i, file in enumerate(files):
            if file[-3:] == "txt":
                with open(root + "/" + file, encoding="utf-8") as f:
                    all_text = f.read()

                    chaptertext_index = 0
                    try:
                        chaptertext_index = all_text.index("Chapter Text") + 12
                    except:
                        chaptertext_index = all_text.index("Work Text:") + 10

                    starting_tags_index = all_text.index("[starting tags]")
                    # This is the actual text
                    fic_text = all_text[chaptertext_index:starting_tags_index]

                    # Extract relevant tags from fanfiction
                    # Account for length of freeform
                    freeform_index = all_text.index("freeform:") + 9
                    fandom_index = all_text.index("fandom:")
                    freeform_tags = all_text[freeform_index:fandom_index]
                    tags_separated = freeform_tags.split("\n")
                    filtered_tags = filter(tags_separated)

                    if len(fic_text) < 100 or fic_text is None or fic_text == " " or filtered_tags == ["None"]\
                         or fic_text == ":" or fic_text == "\n" or filtered_tags is None\
                              or filtered_tags == []:
                        numRemoved += 1
                        os.remove(root + "/" + file)

    print("Num files: ", numFiles)
    print("Num files removed: ", numRemoved)
    print("Percent Removed: ", numRemoved/numFiles)


def countTags():
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
                with open(root + "/" + file, encoding="utf-8") as f:
                    all_text = f.read()
                    # Account for length of freeform
                    freeform_index = all_text.index("freeform:") + 9
                    fandom_index = all_text.index("fandom:")
                    freeform_tags = all_text[freeform_index:fandom_index]
                    tags_separated = freeform_tags.split("\n")
                    filtered_tags = filter(tags_separated)

                    allTagsCntCur = Counter(filter(tags_separated, False))
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

    # fig, ax = plt.subplots()
    # ax.bar(x,y)
    # plt.setp( ax.xaxis.get_majorticklabels(), rotation=45, ha="right" )
    # plt.xticks(rotation = 45, size = 7)
    # plt.title("Percent of Tags that are Valid for Each Fanfiction")
    # plt.xlabel("Fanfiction ID")
    # plt.ylabel("Percentage of Valid Tags")
    # plt.savefig("percentValid_plot.png", bbox_inches='tight')

    fig, ax = plt.subplots()

    x = [i/10 for i in range(10)]
    new_y = [0 for _ in range(10)]

    for perc in y:
        if float(perc) == 1:
            new_y[9] += 1
        else:
            new_y[math.floor(float(perc) * 10)] += 1

    y = new_y
    ax.bar(x, y, width=0.1, align="edge")
    # plt.setp( ax.xaxis.get_majorticklabels(), rotation=45, ha="right" )
    # plt.xticks(rotation = 45, size = 7)
    plt.title("Number of Fanfictions that Had a Certian Percentage of Valid Tags")
    plt.xlabel("Percent of Tags that are Valid")
    plt.ylabel("Number of Fanfictions")
    plt.savefig("percentValid_plot.png", bbox_inches='tight')

    # Used to plot frequency of tags

    x = []
    y = []

    for tag in validTagsCnt.most_common()[:20]:

        x.append(tag[0])
        y.append(tag[1])

    fig, ax = plt.subplots()
    ax.bar(x, y)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")
    plt.xticks(rotation=45, size=7)
    plt.title("20 Most Frequent Valid Tags for Subset of Fanfiction")
    plt.xlabel("Tag Label")
    plt.ylabel("Number of Times Each Tag Appeared")
    plt.savefig("tagFrequency_plot.png", bbox_inches='tight')


def extractData(max_ngram=2):
    corpus = []
    numFiles = 0
    y = None
    inside = 0
    for root, _, files in os.walk("./subset_data"):
        if ".DS_Store" in files:
            numFiles = len(files) - 1
        else:
            numFiles = len(files)

        y = np.zeros((numFiles, num_valid_tags))
        i = 0
        for file in files:
            if file[-3:] == "txt":
                inside += 1
                with open(root + "/" + file, encoding="utf-8") as f:
                    all_text = f.read()

                    # Add fan fiction text to corpus
                    chaptertext_index = 0
                    try:
                        chaptertext_index = all_text.index("Chapter Text") + 12
                    except:
                        chaptertext_index = all_text.index("Work Text") + 9

                    starting_tags_index = all_text.index("[starting tags]")
                    # This is the actual text
                    fic_text = all_text[chaptertext_index:starting_tags_index]
                    # Adding the text to our corpus list
                    corpus.append(fic_text)

                    # Extract relevant tags from fanfiction
                    # Account for length of freeform
                    freeform_index = all_text.index("freeform:") + 9
                    fandom_index = all_text.index("fandom:")
                    freeform_tags = all_text[freeform_index:fandom_index]
                    tags_separated = freeform_tags.split("\n")
                    filtered_tags = filter(tags_separated)

                    target = np.zeros(num_valid_tags)
                    for tag in filtered_tags:
                        index = tag_dict[tag]
                        target[index] = 1

                    y[i] = target
                    i += 1
            else:
                print(file)

    vectorizer = TfidfVectorizer(ngram_range=(1, max_ngram))
    X = vectorizer.fit_transform(corpus)

    return X, y

def train(X, y, saveModel = True, modelName = None):
    model = None
    cutoff = int(X.shape[0]*0.8)
    X_train = X[:cutoff]
    X_test = X[cutoff:]
    y_train = y[:cutoff]
    y_test = y[cutoff:]

    if modelName is not None:
        model = load(modelName)
    else:
        # neighbors = KNeighborsClassifier()
        forest = RandomForestClassifier()
        multi_target_forest = MultiOutputClassifier(forest)
        model = multi_target_forest.fit(X_train, y_train)

    y_pred = model.predict(X)
    total_correct = 0
    total_predicted_tags = 0
    total_actual_tags = 0
    false_pos = 0
    false_neg = 0
    true_pos = 0
    true_neg = 0

    with open("./predictions.txt", "w", encoding="utf-8") as f:
        for count,pred in enumerate(y_pred):
            actual_tags = [valid_tags[i] for (i, tag) in enumerate(y[count]) if tag == 1]
            predicted_tags = [valid_tags[i] for (i, tag) in enumerate(pred) if tag == 1]

            num_correct = 0
            correct_tags = []
            incorrect_tags = []

            for j in range(len(pred)):
                if y[count][j] == 0 and pred[j] == 0:
                    true_neg += 1
                elif y[count][j] == 0 and pred[j] == 1:
                    false_pos += 1
                elif y[count][j] == 1 and pred[j] == 0:
                    false_neg += 1
                elif y[count][j] == 1 and pred[j] == 1:
                    true_pos += 1
                else:
                    print("unexpected values")


            for tag in predicted_tags:
                if tag in actual_tags:
                    num_correct += 1
                    correct_tags.append(tag)
                else:
                    incorrect_tags.append(tag)

            total_correct += num_correct
            total_predicted_tags += len(predicted_tags)
            total_actual_tags += len(actual_tags)
            f.write(f"Predicted Tags: {str(predicted_tags)}, Actual Tags: {actual_tags}, Number of Correct Tags: {num_correct}, Correct Tags: {correct_tags}, Incorrect Tags: {incorrect_tags} \n")
    
    precision = true_pos / (true_pos + false_pos)
    recall = true_pos / (true_pos + false_neg)
    accuracy = (true_pos + true_neg) / (true_neg + true_pos + false_neg + false_pos)
    f1 = (2 * precision * recall) / (precision + recall)

    with open("./results.txt", "w", encoding="utf-8") as f:
        f.write("Total Correct: " + str(total_correct) + "\n")
        f.write("Total Predicted Tags: " + str(total_predicted_tags) + "\n")
        f.write("Total Actual Tags: " + str(total_actual_tags) + "\n")
        f.write("False Positives: " + str(false_pos) + "\n")
        f.write("True Positives: " + str(true_pos) + "\n")
        f.write("False Negatives: " + str(false_neg) + "\n")
        f.write("True Negatives: " + str(true_neg) + "\n")
        f.write("Precision: " + str(precision) + "\n")
        f.write("Recall: " + str(recall) + "\n")
        f.write("Accuracy: " + str(accuracy) + "\n")
        f.write("F1: " + str(f1) + "\n")

    if saveModel:
        dump(model, 'model.joblib')



def train_old(X, y):
    clf = MultinomialNB()
    clf.fit(X, y)
    # 5 fold cross validation
    y_pred = cross_val_predict(clf, X, y, method="predict_proba")

    num_tags_predicted = 5

    predictions = []
    correct_tags = []
    incorrect_tags = []
    num_correct = 0

    for i,pred in enumerate(y_pred):
        # Finds indices of top N largest values
        indices = np.argpartition(pred, -num_tags_predicted)[-num_tags_predicted:]
        # Get the N largest values
        topN = pred[indices]

        for ind in indices:
            if y[i][ind] == 1:
                correct_tags.append(valid_tags[ind])
                num_correct += 1
            else:
                incorrect_tags.append(valid_tags[ind])

        predictions.append((indices, topN))

    predictions = np.array(predictions)
    
    with open("./predictions.txt", "w", encoding="utf-8") as f:
        for count, pred in enumerate(predictions):
            # indicies are indicies of predicted tags, vals are the probabilities of every valid tag
            indices, vals = pred
            pred_tags = []

            for i in range(len(indices)):
                pred_tags.append((valid_tags[indices[i]], vals[i]))

            actual_tags = [valid_tags[tag] for tag in y[count] if tag == 1]
            
            f.write(f"Predicted Tags: {pred_tags}, Actual Tags: {actual_tags}, Number of Correct Tags: {num_correct}, Correct Tags: {correct_tags}, Incorrect Tags: {incorrect_tags}")

def evaluatePredictions(y):
    with open("./predictions.txt", "r+", encoding="utf-8") as f:
        predictions = f.read()
        for count, pred in enumerate(predictions):
            # indicies are indicies of predicted tags, vals are the probabilities of every valid tag
            indices, vals = pred
            pred_tags = []

            for i in range(len(indices)):
                pred_tags.append((valid_tags[indices[i]], vals[i]))

            actual_tags = [valid_tags[tag] for tag in y[count] if tag == 1]
            
            f.write(f"Predicted Tags: {pred_tags}, Actual Tags: {actual_tags}, Number of Correct Tags: {num_correct}, Correct Tags: {correct_tags}, Incorrect Tags: {incorrect_tags}")

def main():
    # countTags()
    # filterData()

    X, y = extractData()
    train(X, y)
    


if __name__ == "__main__":
    main()
