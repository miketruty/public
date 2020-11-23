import argparse, json, os, random


class InvalidDataError(Exception):
  pass


class Exam(object):
    def __init__(self, data_file):
        try:
            self.__dict__ = json.load(data_file)
        except ValueError:
            raise InvalidDataError(
                'ERROR: mis-formed JSON in {}!'.format(data_file.name))
        self._validate()

    def __getitem__(self, key):
        return self.__dict__[key]

    def _validate(self):
        if not 'exam' in self.__dict__:
            raise InvalidDataError('ERROR: mis-formed data!')
        count = 1
        for q in self.__dict__['exam']:
            if (not 'q' in q) or (not 'a' in q):
                raise InvalidDataError(
                    'ERROR: mis-formed exam, question {}.'.format(count))
            count += 1

    def update(self, exam_data):
        self.__dict__['exam'].extend(exam_data['exam'])

    def length(self):
        return len(self.__dict__['exam'])

    def show(self):
        count = 1
        for q in self.__dict__['exam']:
            print('{}) {}\n  {}'.format(count, q['q'], q['a']))
            count += 1


def init_exam_data(data_file_names):
    """Build a dictionary style object with questions and answers.

    Questions and answers contained in the 'exam' element of the outer dict.
    The 'exam' element is a list of dicts, 1 for each question. The 
    question dicts have keys of 'q' and 'a'.

    Args:
        data_file_names (list): Sequence of JSON file name strings.

    Returns:
        Exam object: data structure with all questions and answers.
    """
    all_exam_data = None
    for data_file_name in data_file_names:
        with open(data_file_name) as data_file:
            exam_data = Exam(data_file)
            if not all_exam_data:
                all_exam_data = exam_data
            else:
                all_exam_data.update(exam_data)
    return all_exam_data


def check_exit(answer):
    return (answer.lower() == 'quit') or (answer.lower() == 'exit')


def pause_clear():
    answer = input('\nEnter to continue.')
    os.system('clear')
    return check_exit(answer)


def game_over(correct, asked):
    print('Your score was: {}/{}. Exiting now.'.format(correct, asked))


def do_exam(data_file_names, inputs=[], max_count=9999):
    """Assemble the exam questions/answers, then loop through questions.

    Args:
        data_file_names (list): list of names of JSON files to parse for 
                                questions and answers.
        inputs (list): for testing - list of answers to questions instead of
                       capturing user inputs.
        max_count (int): for testing - ask no more than max_count questions.

    Returns:
        None
    """

    e = init_exam_data(data_file_names)
    # e.show()  # For debugging Exam creation.

    if not inputs:
        os.system('clear')
        print('Welcome! There are {} questions to review.\n'.format(e.length()))
        print('Type "quit" or "exit" to stop.')
        if pause_clear():
            return

    count = 0
    score = 0

    while count < max_count:
        if count:
            print("You're {} for {}; that's {}%.".format(
                score, count, (score/count*100)))
        q = random.choice(e.exam)
        count += 1
        print('{}) {}'.format(count, q['q']))
        answer = inputs[count-1] if inputs else input('\nYour response: ')
        if check_exit(answer):
            game_over(score, count-1)
            return
        if answer == q['a']:
            print('\n==>Correct!')
            score += 1
        else:
            print('\n==>Incorrect! Expected: {}'.format(q['a']))
        if not inputs and pause_clear():
            game_over(score, count-1)
            return

    game_over(score, count)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_files", nargs='+',
                        help="Name of data file.", type=str)

    args = parser.parse_args()

    do_exam(args.data_files)


if __name__ == '__main__':
    main()
