import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    #Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    #Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    
    evidence, labels = load_data("shopping.csv")
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")

def monthconv(month):
    if month == "Jan":
        return 0
    elif month == "Feb":
        return 1
    elif month == "Mar":
        return 2
    elif month == "Apr":
        return 3
    elif month == "May":
        return 4
    elif month == "Jun":
        return 5
    elif month == "Jul":
        return 6
    elif month == "Aug":
        return 7
    elif month == "Sep":
        return 8
    elif month == "Oct":
        return 9
    elif month == "Nov":
        return 10
    else:
        return 11

def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    #raise NotImplementedError
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
        data = []
        for row in reader:
            fev = []

            ev0 = int(row[0])
            ev1 = float(row[1])
            ev2 = int(row[2])
            ev3 = float(row[3])
            ev4 = int(row[4])
            ev5 = float(row[5])
            
            ev6 = [float(cell) for cell in row[6:10]]

            ev7 = monthconv(row[10])
            
            ev8 = [int(cell) for cell in row[11:15]]

            ev9 = 1 if row[15] == "Returning_Visitor" else 0
            ev10 = 1 if row[16] == "True" else 0

            fev.append(ev0)
            fev.append(ev1)
            fev.append(ev2)
            fev.append(ev3)
            fev.append(ev4)
            fev.append(ev5)
            
            fev += ev6

            fev.append(ev7)

            fev += ev8

            fev.append(ev9)
            fev.append(ev10)

            data.append({
                "evidence": fev,
                "label": 1 if row[17] == "TRUE" else 0
            })
        evidence = [row["evidence"] for row in data]
        labels = [row["label"] for row in data]
        return (evidence,labels)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    #raise NotImplementedError
    model = KNeighborsClassifier(n_neighbors = 1)
    model.fit(evidence, labels)
    return model

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    #raise NotImplementedError

    TP = 0
    FP = 0
    FN = 0
    TN = 0
    for (i,j) in zip(labels,predictions):
        if i == j :
            if i == 1:
                TP += 1
            else :
                TN += 1    
        else :
            if i == 1:
                FP += 1
            else :
                FN += 1    
        
    #total = len(predictions)

    sensitivity = TP / (TP + FN)
    specificity = TN / (TN +FP)
    return (sensitivity,specificity)


if __name__ == "__main__":
    main()

