####################
# source/teach_me.py
####################

import random

from . import quizcore

################################################################################

class FAQ:

    def __init__(self, testbank):
        self.test = quizcore.UnitTest(testbank)

    def __iter__(self):
        unittest = self.test
        yield Enter(unittest)
        unittest_report = Report(unittest)
        for chapter in unittest.chapters:
            yield Enter(chapter)
            chapter_report = Report(chapter, unittest_report)
            for section in chapter.sections:
                yield Enter(section)
                section_report = Report(section, chapter_report)
                QnA = []
                for category in section.categories:
                    category.build()
                    QnA.extend(category.QnA)
                random.shuffle(QnA)
                for question in QnA:
                    yield Question(section_report, *question)
                yield Exit(section)
                section_report.finalize()
                yield section_report
            yield Exit(chapter)
            chapter_report.finalize()
            yield chapter_report
        yield Exit(self.test)
        unittest_report.finalize()
        yield unittest_report

################################################################################

class _Status:

    def __init__(self, division):
        self.kind = division.__class__.__name__
        self.name = division.name

    def __str__(self):
        return '{}: {}'.format(self.kind, self.name)

class Enter(_Status): pass

class Exit(_Status): pass

################################################################################

class Report:

    def __init__(self, level, parent=None):
        self.__level = level.__class__.__name__
        self.__parent = parent
        self.__right = 0
        self.__wrong = 0
        self.__problems = []
        self.__finalized = False

    def right_answer(self):
        assert not self.__finalized
        self.__right += 1

    def wrong_answer(self):
        assert not self.__finalized
        self.__wrong += 1

    def review(self, question, answer):
        assert not self.__finalized
        self.__problems.append((question, answer))

    def problems(self):
        assert self.__finalized
        for question, answer in self.__problems:
            yield Answer(answer, *question)

    def finalize(self):
        assert not self.__finalized
        if self.__parent is not None:
            self.__parent.__right += self.__right
            self.__parent.__wrong += self.__wrong
            self.__parent.__problems.extend(self.__problems)
        self.__finalized = True

    @property
    def level(self):
        return self.__level

    @property
    def right(self):
        assert self.__finalized
        return self.__right

    @property
    def wrong(self):
        assert self.__finalized
        return self.__wrong

    @property
    def total(self):
        assert self.__finalized
        return self.__right + self.__wrong

    @property
    def final(self):
        return self.__parent is None

################################################################################

class Question:

    def __init__(self, report, category, question, choices, right):
        self.__report = report
        self.__category = category
        self.__question = question
        self.__choices = choices
        self.__right = right
        self.__answered = False
        self.__QnA = category, question, choices, right

    @property
    def category(self):
        return self.__category

    @property
    def question(self):
        return self.__question

    @property
    def choices(self):
        return self.__choices

    def answer(self, index_or_string):
        assert not self.__answered
        if isinstance(index_or_string, int):
            index_or_string = self.__choices[index_or_string]
        if index_or_string == self.__right:
            self.__report.right_answer()
        else:
            self.__report.wrong_answer()
            self.__report.review(self.__QnA, index_or_string)
        self.__answered = True

################################################################################

class Answer(Question):

    def __init__(self, answer, *question):
        super().__init__(None, *question)
        self.__answer = answer

    @property
    def answer(self):
        return self.__answer

    @property
    def right(self):
        return self._Question__right
