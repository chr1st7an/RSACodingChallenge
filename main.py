# Author: Christian Rodriguez
# Date: 02/03/2022
# Title: RSA CLI Program
import RSA
from PyInquirer import prompt
from prompt_toolkit.validation import Validator, ValidationError
from examples import custom_style_2
import os.path
from os import path


class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message="Enter a valid Integer", cursor_position=len(document.txt))


questions = [
    {
        'type': 'list',
        'name': 'user_choice',
        'message': 'RSA Coding Challenge',
        'choices': ['Create RSA Key Pair & Shard Private Key', 'Encrypt Plain Text', 'Reassemble Private Key', 'Decrypt Cypher Text']
    }
]
questions2 = [
    {
        'type': 'input',
        'name': 'n',
        'message': 'How many shareholder shards would you like to create?',
        'validate': NumberValidator
    },
    {
        'type': 'input',
        'name': 'k',
        'message': 'What would you like your threshold to be?',
        'validate': NumberValidator
    }
]
questions3 = [
    {
        'type': 'input',
        'name': 'plaintext',
        'message': 'Enter a string to be encrypted:'
    }
]
questions4 = [
    {
        'type': 'input',
        'name': 'shard',
        'message': 'Enter the Shard file path (eg. keys/Shard[number].txt):'
    }
]


def main():
    answers = prompt(questions, style=custom_style_2)
    while answers['user_choice'] != 'Create RSA Key Pair & Shard Private Key':
        print("You must create an RSA Key Pair before Utilizing any of these features")
        answers = prompt(questions, style=custom_style_2)
    else:
        field_size = 10**5
        priv, pub = RSA.createKeys()
        answers = prompt(questions2, style=custom_style_2)
        n = answers.get("n")
        k = answers.get("k")
        instance1 = RSA.Keys(priv, pub, k, n, field_size)
        secret = instance1.privateHash()
        coefficients = RSA.coefficient(k, secret)
        shards = instance1.generateShards(secret, coefficients)
        print("Check your 'keys' folder for your Public Key and Private Key Shards!")
    answers = prompt(questions, style=custom_style_2)
    while answers['user_choice'] != 'Encrypt Plain Text':
        print("You must Encrypt plain text before proceeding with Decrypting")
        answers = prompt(questions, style=custom_style_2)
    else:
        answers = prompt(questions3, style=custom_style_2)
        plaintext = answers.get("plaintext")
        cypher = instance1.encryptTxt(plaintext)
        print('Here is your encrypted text: {}'.format(cypher))
    answers = prompt(questions, style=custom_style_2)
    while answers['user_choice'] != 'Reassemble Private Key':
        print('You must put together your Private Key using at least {} of your shards!'.format(k))
        answers = prompt(questions, style=custom_style_2)
    else:
        print('You must put together your Private Key using at least {} of your shards!'.format(k))
        shardlist = []
        for i in range(int(k)):
            answers = prompt(questions4, style=custom_style_2)
            fileName = answers.get("shard")
            while path.exists(fileName) == False:
                print("That shard is non-existent. Try again.")
                answers = prompt(questions4, style=custom_style_2)
                fileName = answers.get("shard")
            else:
                shardFile = open(fileName, 'r')
                shard = shardFile.read()
                shardFile.close()
                num = 0
                for char in fileName:
                    if char.isdigit():
                        num += int(char)
                shardlist.append(shards[num - 1])
        reconstructed = instance1.reconstructKey(shardlist)
        while reconstructed != secret:
            print("Reconstruction Failure. Try again.")
            answers = prompt(questions, style=custom_style_2)
        else:
            print("Congratulations! Your Private Key has been Reassembled.")
        answers = prompt(questions, style=custom_style_2)
        while answers['user_choice'] != 'Decrypt Cypher Text':
            print("You are finally able to decrypt your cypher text!")
            answers = prompt(questions, style=custom_style_2)
        else:
            decryptedtxt = instance1.decryptMsg(cypher)
            print("Converting the cypher code ({}) into decrypted plain text.....\n{}".format(
                cypher, decryptedtxt))


if __name__ == "__main__":
    main()
