import re

class Constraints:
    # representation of the constraints in conjunctive normal form (CNF)
    and_list = []

    def __init__(self, file):
        lines = open(file, 'r').readlines() # AND

        num_labels = int(lines[0])
        for index in range(1, len(lines)):
            elements = re.split(' +', lines[index])
            i = 0
            labels = [] # OR
            while elements[i].startswith('y'):
                labels.append(label_index(elements[i]))
                i += 1

            constraint = clean_string(elements[i])
            i += 1

            if constraint == 'min':
                for other in range(num_labels):
                    if other not in labels:
                        self.and_list.append([(other, label) for label in labels])

            if constraint == 'max':
                for other in range(num_labels):
                    if other not in labels:
                        self.and_list.append([(label, other) for label in labels])

            if constraint == 'notmin':
                others = filter(lambda x: x not in labels, range(num_labels))
                # this constraint makes only sense with one label
                label = labels[0]
                self.and_list.append([(label, other) for other in others])

            if constraint == 'notmax':
                others = filter(lambda x: x not in labels, range(num_labels))
                # this constraint makes only sense with one label
                label = labels[0]
                self.and_list.append([(other, label) for other in others])

            if constraint == '<':
                label2 = label_index(elements[i])
                self.and_list.append([(label2, label) for label in labels])

            if constraint == '>':
                label2 = label_index(elements[i])
                self.and_list.append([(label, label2) for label in labels])


def clean_string(string):
    return string.replace('\n', '')

def label_index(label):
    return int(clean_string(label)[1:])