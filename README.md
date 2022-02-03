# RSACodingChallenge

Dependencies:

Created using python3.9.7 on MacOS

It is reccomended, but not necessary, to create and enter a virtual environment before installing these dependencies as they might collide with some existing modules.
do this by running `python3 -m venv .venv` then `. ./.venv/bin/activate` within the project directory.

[PyInquirer](https://github.com/CITGuru/PyInquirer#types) is a required CLI dependency. Install by running `pip install PyInquirer`
If there are any errors involving prompt_toolkit, install it seperately with `pip install prompt_toolkit==1.0.14`

[Pure Python RSA Implementation](https://pypi.org/project/rsa/) is a required RSA key pair generation dependency. Install using `pip install rsa`

Unit Test:
please reference the [tutorial video](/unit_test_tutorial/unittest.mov) within the unit_test_tutorial file

1. Head to the directory for the project within your CLI and run `python3 main.py`. You will be greeted with the [main menu](/unit_test_tutorial/mainmenu.png)

You will need to complete each of the features in order

2. [Create Key Pair and Shard Private Keys](/unit_test_tutorial/CreatingKeyPair.png) into whatever desired amount of Shareholders. Additionally set the minimum threshold needed to reassemble the Private key.

3. [Encrypt your plain text](/unit_test_tutorial/encryptplaintxt.png)

4. [Reassemble your Private Key](/unit_test_tutorial/reassemblePrivKey.png) using the minimum amount of shards set in step 2. Make sure you enter the exact file path or it will not be validated. The shards are validated by using Shamir's Secret Sharing Algorithm; the ordered pair within each of the shards are used to solve the polynomial created using the unique numeric value derived from the private key.

5. [Decrypt](/unit_test_tutorial/Decrypt.png) your encrypted plain text!
