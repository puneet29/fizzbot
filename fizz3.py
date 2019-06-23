# Interactive python client for fizzbot

import json
import urllib.request
import urllib.error

domain = 'https://api.noopschallenge.com'

def print_sep(): print('----------------------------------------------------------------------')

# print server response
def print_response(dict):
    print('')
    print('message:')
    print(dict.get('message'))
    print('')
    for key in dict:
        if key != 'message':
            print('%s: %s' % (key, json.dumps(dict.get(key))))
    print('')

# try an answer and see what fizzbot thinks of it
def try_answer(question_url, answer):
    print_sep()
    body = json.dumps({'answer': answer})
    print('*** POST %s %s' % (question_url, body))
    try:
        req = urllib.request.Request(
            domain + question_url, data=body.encode('utf8'), headers={'Content-Type': 'application/json'})
        res = urllib.request.urlopen(req)
        response = json.load(res)
        print_response(response)
        print_sep()
        return response

    except urllib.error.HTTPError as e:
        response = json.load(e)
        print_response(response)
        return response

def getAnswer(question_data):
    rules = question_data['rules']
    numbers = question_data['numbers']
    number = []
    response = []

    for rule in rules:
        number.append(rule['number'])
        response.append(rule['response'])

    for i in range(len(numbers)):
        res = ''
        for j in range(len(number)):
            if(not numbers[i] % number[j]):
                res += response[j]
        if(res != ''):
            numbers[i] = res

    return(" ".join([str(x) for x in numbers]))


# keep trying answers until a correct one is given
def get_correct_answer(question_url, question_data, firstTwo):
    while True:
        if(firstTwo):
            answer = 'python'
        else:
            answer = getAnswer(question_data)
            # answer = input('Enter your answer:\n')
        print(answer)

        response = try_answer(question_url, answer)

        if (response.get('result') == 'interview complete'):
            print('congratulations!')
            exit()

        if (response.get('result') == 'correct'):
            # input('press enter to continue')
            return response.get('nextQuestion')

# do the next question
def do_question(domain, question_url, firstTwo):
    print_sep()
    print('*** GET %s' % question_url)

    request = urllib.request.urlopen(('%s%s' % (domain, question_url)))
    question_data = json.load(request)
    print_response(question_data)
    print_sep()

    next_question = question_data.get('nextQuestion')

    if next_question:
        return next_question
    return get_correct_answer(question_url, question_data, firstTwo)


def main():
    question_url = '/fizzbot'
    question_url = do_question(domain, question_url, True)
    question_url = do_question(domain, question_url, True)
    while question_url:
        question_url = do_question(domain, question_url, False)


if __name__ == '__main__':
    main()
