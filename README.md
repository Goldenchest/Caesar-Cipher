Caesar-Cipher
=============

Caesar Cipher encryption and decryption tool, created in 11th grade as the final project for Carnegie Mellon's
Intro to Programming class in the AP/EA Pre-Collge program.

This project uses the Caesar Cipher and makes a game out of it.
The goal of the game is to decipher a group of words encrypted
with the Caesar Cipher as quickly as possible.

Once you have deciphered a word in the game, simply click on the
text box and type your answer in. If the answer was correct, the
box will turn green, and the next word will be shown. Press enter
to type in the next word. To avoid making things too difficult,
the highest key used in the game will be 4.

As a bonus, I also created a Caesar Cipher translator, which can
decrypt any Caesar Cipher message or encrypt your own message.

The project is mostly object oriented (besides the Tkinter code)
and makes extensive use of class inheritance for the buttons.
The words are randomly generated from a textfile containing over
55,000 words, and the cipher translator goes through this list to
see if a decrypted or encrypted string is a valid English word or
not.
