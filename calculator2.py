def readNumber(line, index):
    number = 0
    flag = 0
    keta = 1
    while index < len(line) and (line[index].isdigit() or line[index] == '.'):
        if line[index] == '.':
            flag = 1
        else:
            number = number * 10 + int(line[index])
            if flag == 1:
                keta *= 0.1
        index += 1
    token = {'type': 'NUMBER', 'number': number * keta}
    return token, index


def readPlus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def readMinus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def readTimes(line, index):
    token = {'type':'TIMES'}
    return token, index + 1

def readDivide(line, index):
    token = {'type':'DIVIDE'}
    return token, index + 1

def readBracketLeft(line, index):
    token = {'type':'LBRACKET'}
    return token, index + 1

def readBracketRight(line, index):
    token = {'type':'RBRACKET'}
    return token, index + 1


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index)
        elif line[index] == '+':
            (token, index) = readPlus(line, index)
        elif line[index] == '-':
            (token, index) = readMinus(line, index)
        elif line[index] == '*':
            (token, index) = readTimes(line, index)
        elif line[index] == '/':
            (token, index) =  readDivide(line, index)
        elif line[index] == '(':
            (token, index) = readBracketLeft(line, index)
        elif line[index] == ')':
            (token, index) = readBracketRight(line, index)
        else:
            print 'Invalid character found: ' + line[index]
            exit(1)
        tokens.append(token)
    return tokens

def evaluateBrackets(tokens):
    index = 0
    bracket_left_index = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'RBRACKET':
            for i in range(0,index):
                if tokens[i]['type'] == 'LBRACKET':
                    bracket_left_index = i

            #calculate inside the brackets
            value = evaluate(tokens[bracket_left_index+1:index])
            tokens[index] = {'type':'NUMBER', 'number':value}
            del tokens[bracket_left_index:index]
            index = bracket_left_index
            
        index += 1
        
        
def evaluateTimesAndDivide(tokens):
    index = 0
    #this function calculate * and /
    while index < len(tokens):
        #calculate times
        if tokens[index]['type'] == 'TIMES':
            if tokens[index-1]['type'] == 'NUMBER':
                if tokens[index+1]['type'] == 'NUMBER':
                    value = tokens[index-1]['number'] * tokens[index+1]['number']
                    tokens[index-1] = {'type':'NUMBER','number':value}
                    del tokens[index:index+2]
                    index -= 1
        #calculate divide
        elif tokens[index]['type'] == 'DIVIDE':
            if tokens[index-1]['type'] == 'NUMBER':
                if tokens[index+1]['type'] == 'NUMBER':
                    value = tokens[index-1]['number'] / tokens[index+1]['number']
                    tokens[index-1] = {'type':'NUMBER','number':value}
                    del tokens[index:index+2]
                    index -= 1
        index += 1

    return tokens
        
                    
            
            
def evaluate(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    evaluateBrackets(tokens)
    evaluateTimesAndDivide(tokens)

    #calculate + and -
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print 'Invalid syntax'
        index += 1
    return answer


def test(line, expectedAnswer):
    tokens = tokenize(line)
    evaluateBrackets(tokens)
    actualAnswer = evaluate(tokens)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print "PASS! (%s = %f)" % (line, expectedAnswer)
    else:
        print "FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer)


# Add more tests to this function :)
def runTest():
    print "==== Test started! ===="
    test("1",1)
    test("1+2",3)
    test("1.2+2",3.2)
    test("3+4*2",11)
    test("2*(3*(2+1))+1",19)
    test("3*2+3.0/1.5",8)
    test("(4*(2+3))/5",4)
    test("15-2*(8/2)",7)

    print "==== Test finished! ====\n"

runTest()

while True:
    print '> ',
    line = raw_input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print "answer = %f\n" % answer
