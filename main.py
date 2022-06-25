
from bitstring import BitArray
#Huffman encoding test
class Letter:
    code = []
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

    def generateCode(self, startNode, code):
        code.append(startNode.dir)
        if startNode.hasSub() == True:
            for sub in startNode.children:
                if self.generateCode(sub, code) == True:
                    return True
            code[:] = code[:-1]
            return False
        else:
            if self.name == startNode.letter.name:
                self.code = code
                return True
            else:
                code[:] = code[:-1]
                return False





class BinaryTreeNode:
    ID = 0

    def __init__(self, letter, level, parent):
        BinaryTreeNode.ID += 1
        self.id = BinaryTreeNode.ID
        self.letter = letter
        self.level = level
        self.children = []
        self.parent = parent
        self.dir = 0

    def hasSub(self):
        if len(self.children) == 0:
            return False
        else:
            return True

    def decode(self, binary):
           if self.hasSub():
               dir = binary[0]
               binary[:] = binary[1:]
               return self.children[dir].decode(binary)
           else:
               return self.letter.name



toEncode = "bee"
print(toEncode)
listOfLetters = []
listOfLettersObj = []
for letter in toEncode:
    index = next((i for i, item in enumerate(listOfLettersObj) if item.name == letter), -1)
    if index == -1:
        listOfLetters.append(letter)
        listOfLettersObj.append(Letter(letter, 1))
    else:
        listOfLettersObj[index].amount+=1

sortedLetters = sorted(listOfLettersObj, key=lambda obj: (obj.amount, obj.name))
listOfNodes = []
for letter in sortedLetters:
    listOfNodes.append(BinaryTreeNode(letter, letter.amount, None))


while len(listOfNodes) != 1:
    listOfNodes = sorted(listOfNodes, key=lambda obj: (obj.level, obj.letter.name))
    leftNode = listOfNodes.pop(0)
    rightNode = listOfNodes.pop(0)
    level = leftNode.level + rightNode.level
    both = [leftNode, rightNode]
    both = sorted(both, key=lambda obj: obj.letter.name)
    NewNode = BinaryTreeNode(Letter(both[0].letter.name, level), level, None)
    leftNode.parent = NewNode
    rightNode.parent = NewNode
    leftNode.dir = 0
    rightNode.dir = 1
    NewNode.children.append(leftNode)
    NewNode.children.append(rightNode)
    listOfNodes.append(NewNode)

for letter in sortedLetters:
    letter.generateCode(listOfNodes[0], [])
    if len(letter.code) != 1:
        letter.code = letter.code[1:]
    print( letter.name, end=': ')
    print(letter.code)



Encoded = []
for letter in toEncode:
    for equivalent in sortedLetters:
        if letter == equivalent.name:
            for bit in equivalent.code:
                Encoded.append(bit)
            break

print("Encoded as:")
print(Encoded)

codeLength = len(Encoded)
intRepresentation = BitArray(Encoded)
intRepresentation = intRepresentation.uint
print(intRepresentation)
root = listOfNodes[0]



#translation
Message = ""
Format = '{0:0'
Format += str(codeLength)
Format += 'b}'
stringCode = Format.format(intRepresentation)
bitsToRead = []
for bit in stringCode:
    bitsToRead.append(int(bit))
print("translated to:")
result = ""
while len(bitsToRead) > 0:
    result+=root.decode(bitsToRead)
print(result)


