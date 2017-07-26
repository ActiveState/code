####################
# source/quizcore.py
####################

import random

from . import testbank

################################################################################

class UnitTest:

    def __init__(self, testbank):
        self.name = testbank.attr
        self.chapters = []
        for child in testbank.children:
            self.chapters.append(Chapter(child))
        assert len(self.chapters) > 0, 'UnitTest is empty!'

class Chapter:

    def __init__(self, chapter):
        self.name = chapter.attr
        self.sections = []
        for child in chapter.children:
            self.sections.append(Section(child))
        assert len(self.sections) > 0, 'Chapter is empty!'

class Section:

    def __init__(self, section):
        self.name = section.attr
        self.categories = []
        for child in section.children:
            self.categories.append(Category(child))
        assert len(self.categories) > 0, 'Section is empty!'

################################################################################

def Category(category):
    if category.attr == 'multiple_choice':
        return Multiple_Choice(category)
    elif category.attr == 'true_or_false':
        return True_Or_False(category)
    elif category.attr == 'matching':
        return Matching(category)
    else:
        raise ValueError(category.attr)

class _Category:

    def __init__(self, category):
        self.facts = []
        for child in category.children:
            tof = self.__class__.__name__ == 'True_Or_False'
            self.facts.append(Fact(child, tof))
        assert len(self.facts) > 0, 'Category is empty!'

class _MCM(_Category):

    def build(self):
        kinds = {}
        for fact in self.facts:
            fact.build()
            if fact.kind not in kinds:
                kinds[fact.kind] = {'Q': {}, 'A': {}}
            for question in fact.Q2A:
                if question in kinds[fact.kind]['Q']:
                    kinds[fact.kind]['Q'][question].update(fact.Q2A[question])
                else:
                    kinds[fact.kind]['Q'][question] = set(fact.Q2A[question])
            for answer in fact.A2Q:
                if answer in kinds[fact.kind]['A']:
                    kinds[fact.kind]['A'][answer].update(fact.A2Q[answer])
                else:
                    kinds[fact.kind]['A'][answer] = set(fact.A2Q[answer])
        self.QnA = []
        for kind in kinds:
            questions = set(kinds[kind]['Q'])
            answers = set(kinds[kind]['A'])
            for question in questions:
                wrong = answers.difference(kinds[kind]['Q'][question])
                sample = random.sample(wrong, min(len(wrong), self.CHOICES))
                right = random.choice(tuple(kinds[kind]['Q'][question]))
                sample.append(right)
                random.shuffle(sample)
                category = self.__class__.__name__.replace('_', ' ')
                self.QnA.append((category, question, tuple(sample), right))

################################################################################

class True_Or_False(_Category):

    def build(self):
        questions = {}
        for fact in self.facts:
            fact.build()
            for question in fact.Q2A:
                if question in questions:
                    questions[question].update(fact.Q2A[question])
                else:
                    questions[question] = set(fact.Q2A[question])
        for question in questions:
            assert len(questions[question]) == 1, 'Question is invalid!'
        self.QnA = []
        for question in questions:
            sample = random.sample(('True', 'False'), 2)
            right = tuple(questions[question])[0]
            self.QnA.append(('True or False', question, tuple(sample), right))

class Multiple_Choice(_MCM): CHOICES = 3

class Matching(_MCM): CHOICES = 25

################################################################################

class Fact:

    def __init__(self, fact, tof):
        self.kind = fact.attr
        self.questions = []
        self.answers = []
        for child in fact.children:
            if isinstance(child, testbank.Question):
                self.questions.append(Question(child))
            elif isinstance(child, testbank.Answer):
                self.answers.append(Answer(child, tof))
            else:
                raise TypeError(child)
        assert len(self.answers) > 0, 'Fact is empty!'

    def build(self):
        questions = frozenset(question.text for question in self.questions)
        answers = frozenset(answer.text for answer in self.answers)
        self.Q2A = dict((question, answers) for question in questions)
        self.A2Q = dict((answer, questions) for answer in answers)

class Question:

    def __init__(self, question):
        self.text = question.text

class Answer:

    def __init__(self, answer, tof):
        if tof:
            assert answer.text in ('True', 'False'), 'Answer is invalid!'
        self.text = answer.text
