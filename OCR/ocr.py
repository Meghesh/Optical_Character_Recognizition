#!/usr/bin/python
#
# ./ocr.py : Perform optical character recognition, usage:
#     ./ocr.py train-image-file.png train-text.txt test-image-file.png
# 
# Authors: (insert names here)
# (based on skeleton code by D. Crandall, Oct 2017)
###########################################################################################################################
# REPORT!!
# Approch: Firstly, i began with reading the data and updated several dictionaries, so that I can compute the
# probabilities further. For example, my program calculates All the transitions probabilities i.e. all the probabilities
# that a letter has with another letter.
#
# After All the initial probabilities are calculated, I begin the main execution of the program.
#
# In simplified approach what I do is, I calculate what is the most likely probability of a given character being that
# actual letter. For this I have used the hit and miss approach. If the two images that I compare pixel by pixel match
# each other then i increase the hit count, if not then I increase the miss count. Finally, I take ratio of it and store
# Then I take the maximum value of it and print the most likely word.
#
# In HMM_VE, we require initial probability, emission probability and transition probability, to get the best letter
# for the corresponding image. However, the for the first letter, we do not require a transition probability
# so I have calculated the emission probability of how much the given image matches with our Train image. Then I store
# these values as TAO and use it further. When, I calculate my probabilities for other letters I even multiply the
# transition probability. Then I take the sum of all the characters that the current image can be and keep them as the
# next TAO i.e. for the next letter. Finally, the maximum value of TAO at that level is given as the part of speech to
# the word.
#
#
# In HMM_Viterbi, I have done the same process as above to calculate all the probabilities in the similar was as above.
# However, the main difference is that instead of taking a sum of all the multiplied values i.e. emission*transition*
# Previous TAO, we take the maximum value at that stage and store it as TAO at the current stage. So we take the maximum
# value. Finally, we calculate the maximum at every state of TAO and give a particular image a the max calculated
# character.
#
# i have made use of smoothing techniques while calculating my transition probabilities, i.e. for example to calculate
# the transition probability of C|C , we take how many times C followed as C(numerator), and C followed an other letter
# (denominator). So, to perform smoothing I added 1000000 to both numerator and denominator.
#
############################################################################################################################

from PIL import Image, ImageDraw, ImageFont
import sys
import math

CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25


def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }

def training_text(fname):
    transistions = {}
    trans_count = 0
    exemplars = []
    TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    p_transistions = {}
    file = open(fname, 'r');
    for line in file:
        data = [w for w in line.split()]
        k = ""
        for l in data:
            if l == "DET" or l == "NOUN" or l == "ADJ" or l == "ADP" or l == "ADV" or l == "CONJ" or l == "NUM" or l == "PRON" or l == "VERB" or l == "X" or l == "PRT":
                pass
            else:
                if k != "":
                    for i in range(0,len(l)):
                        if i==0:
                            if " "+","+l[i] not in transistions:
                                transistions[" "+","+l[i]] = float(1)
                                trans_count += float(1)
                            else:
                                value = float(+transistions[" "+","+l[i]])
                                value += float(1)
                                transistions[" "+","+l[i]] = float(value)
                                trans_count += float(1)
                        else:
                            if l[i-1]+","+l[i] not in transistions:
                                transistions[l[i-1]+","+l[i]] = float(1)
                                trans_count += float(1)
                            else:
                                value = float(+transistions[l[i-1]+","+l[i]])
                                value += float(1)
                                transistions[l[i - 1] + "," + l[i]] = float(value)
                                trans_count += float(1)
                else:
                    for i in range(0,len(l)):
                        if i>=1:

                            if l[i-1]+","+l[i] not in transistions:
                                transistions[l[i-1]+","+l[i]] = float(1)
                                trans_count += float(1)
                            else:
                                value = float(+transistions[l[i-1]+","+l[i]])
                                value += float(1)
                                transistions[l[i - 1] + "," + l[i]] = float(value)
                                trans_count += float(1)

                        if i == (len(l)-1):
                            if l[i]+","+" " not in transistions:
                                transistions[l[i]+","+" "] = float(1)
                                trans_count += float(1)#*1000000
                            else:
                                value = float(transistions[l[i]+","+" "])
                                value += float(1)
                                transistions[l[i]+","+" "] = float(value)
                                trans_count += float(1)
                    k = l
    for m in TRAIN_LETTERS:
        for j in TRAIN_LETTERS:
            if j + "," + m in transistions:
                trans = float(transistions[j + "," + m])  # Calculatin Transistion
            else:
                trans = 1

            cal = 0
            for l_t in TRAIN_LETTERS:
                if l_t + "," + m in transistions:
                    cal += transistions [l_t + "," + m]
                else:
                    cal += 1
            trans += 10000000
            cal += 10000000
            trans = float(float(trans) / float(cal))
            p_transistions[j + "," + m] = float(trans)
    li = [transistions,p_transistions]
    return li

#####
# main program
(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)
train_text = training_text(train_txt_fname)


## Below is just some sample code to show you how the functions above work. 
# You can delete them and put your own code here!


# Each training letter is now stored as a list of characters, where black
#  dots are represented by *'s and white dots are spaces. For example,
#  here's what "a" looks like:

#print "\n".join([ r for r in train_letters['B'] ])

# Same with test letters. Here's what the third letter of the test data
#  looks like:
#print "\n".join([ r for r in test_letters[1] ])

#a = load_training_letters()

def Simplified(train_letters, test_letters):
    final1 = []
    stri = ''

    #print train_letters
    for i in range(0, len(test_letters)):
        TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
        final = {}
        for letter in TRAIN_LETTERS:
            count = 0
            miss = 1
            co = 0
            for ig in range(0, len(train_letters[letter])):
                for ik in range(0, len(train_letters[letter][ig])):
                    if test_letters[i][ig][ik] == " " and train_letters [letter][ig][ik] == " ":
                        co += 1
                    else:
                        if test_letters[i][ig][ik] == train_letters[letter][ig][ik]:
                            count = count + 1
                        else:
                            miss += 1

            if co > 345:
                if letter == " ":

                    final[letter] = 2
                else:
                    final[letter] = float(float(count) / float(miss))
            else:
                final[letter] = float(float(count) / float(miss))


        co = 0
        for id in final:
            if final[id] > co:
                co = final[id]
                stri = id
        final1.append(stri)
        final = []
    print " Simple: %s" %('').join(final1)



def hmm_ve(train_letters, test_letters, l):
    final1 = []
    stri = ''
    tao = {}
    tao_count = 0
    em = {}
    transition = {}
    transition = l[0]
    x = {}
    p_transition = {}
    p_transition = l[1]

    # print train_letters
    for i in range(0, 1):
        # print test_letters[i]
        TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
        final = {}
        for letter in TRAIN_LETTERS:
            #print letter
            count = 0
            miss = 1
            co = 0
            for ig in range(0, len(train_letters[letter])):
                for ik in range(0, len(train_letters[letter][ig])):
                    if test_letters[i][ig][ik] == " " and train_letters [letter][ig][ik] == " ":
                        co += 1
                    else:
                        if test_letters[i][ig][ik] == train_letters[letter][ig][ik]:
                            count = count + 1
                        else:
                            miss += 1
            if miss > 1:
                miss -= 1
            if co > 340:
                if letter == " ":
                    final[str(tao_count) + "," + letter] = 1
                    tao[str(tao_count) + "," + letter] = 1
                else:
                    final[str(tao_count) + "," + letter] = float(float(count) / 350)
                    tao[str(tao_count) + "," + letter] = float(float(count) / 350)
            else:
                final[str(tao_count)+","+letter] = float(float(count)/350)
                x[str(tao_count) + "," + letter] = float(float(count)/ 350)
                tao[str(tao_count) + "," + letter] = float(float(count) / 350)

            co = 0



    for i in range(1,len(test_letters)):
        tao_count += 1
        TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
        x = {}

        for letter in TRAIN_LETTERS:
            count = 0
            miss = 1
            co = 0
            for ig in range(0, len(train_letters[letter])):
                for ik in range(0, len(train_letters[letter][ig])):
                    if test_letters[i][ig][ik] == " " and train_letters [letter][ig][ik] == " ":
                        co += 1
                    else:
                        if test_letters[i][ig][ik] == train_letters[letter][ig][ik]:
                            count = count + 1
                        else:
                            miss += 1
            if miss > 1:
                miss -= 1
            if co > 340:
                if letter == " ":
                    final[str(tao_count) + "," + letter] = 1
                else:
                    final[str(tao_count) + "," + letter] = float(float(count) / 350)
            else:
                final[str(tao_count)+","+letter] = float(float(count)/ 350)
                x[str(tao_count) + "," + letter] = float(float(count)/ 350)

    for i in range(1,len(test_letters)):
        for j in TRAIN_LETTERS:

                value = 0

                for l in TRAIN_LETTERS:
                    emission = (float(final[str(i)+","+j]))                 #Calculating Emission


                    if l+","+j in p_transition:
                        trans = float(p_transition[l+","+j])                #Calculatin Transistion
                    else:
                        trans = 1

                    if str(i-1)+","+l in tao.keys():
                        if tao[str(i-1)+","+l] == 0:
                            ta = 1
                        else:
                            ta = ((tao[str(i-1)+","+l]))
                    else:
                        ta = float(0.1)
                    value += float((float((ta)*float(emission)*float(trans))))
                tao[str(i)+","+j] = (float(value))
                value = 0

    final1 = []
    for e in range(0, len(test_letters)):
        count = 0
        state = ""

        for s in TRAIN_LETTERS:
            if str(e) + "," + s in tao.keys():
                if float(tao[str(e) + "," + s]) > count:
                    count = float(tao[str(e) + "," + s])
                    state = s
        final1.append(state)
        count = 0

    print " HMM VE: %s"%('').join(final1)


def hmm_viterbi(train_letters, test_letters, l):
    final1 = []
    stri = ''
    tao = {}
    tao_count = 0
    em = {}
    transition = {}
    transition = l[0]
    x = {}
    v = {}
    p = 0
    p_transistions = {}
    p_transistions = l[1]

    # print train_letters
    for i in range(0, 1):
        TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
        final = {}
        for letter in TRAIN_LETTERS:
            co = 0
            count = 0
            miss = 1
            for ig in range(0, len(train_letters[letter])):
                for ik in range(0, len(train_letters[letter][ig])):
                    if test_letters[i][ig][ik] == " " and train_letters [letter][ig][ik] == " ":
                        co += 1
                    else:
                        if test_letters[i][ig][ik] == train_letters[letter][ig][ik]:
                            count = count + 1
                        else:
                            miss += 1
            if miss > 1:
                miss -= 1

            if co > 340:
                if letter == " ":
                    final[str(tao_count) + "," + " "] = 1
                    tao[str(tao_count) + "," + letter] = 1
                    x[str(tao_count) + "," + letter + "," + letter] = 1
                else:
                    final[str(tao_count) + "," + letter] = float(float(count) / 350)
                    x[str(tao_count) + "," + letter + "," + letter] = float(float(count) / 350)
                    tao[str(tao_count) + "," + letter] = float(float(count) / 350)
            else:
                final[str(tao_count)+","+letter] = float(float(count)/ 350)
                x[str(tao_count) + "," + letter+ "," + letter] = float(float(count)/ 350)
                tao[str(tao_count) + "," + letter] = float(float(count) / 350)

    for i in range(1,len(test_letters)):
        tao_count += 1
        TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "

        for letter in TRAIN_LETTERS:
            count = 0
            miss = 1
            co = 0
            for ig in range(0, len(train_letters[letter])):
                for ik in range(0, len(train_letters[letter][ig])):
                    if test_letters[i][ig][ik] == " " and train_letters [letter][ig][ik] == " ":
                        co += 1
                    else:
                        if test_letters[i][ig][ik] == train_letters[letter][ig][ik]:
                            count = count + 1
                        else:
                            miss += 1
            if miss > 1:
                miss -= 1
            if co > 340:
                if letter == " ":
                    final[str(tao_count) + "," + " "] = 1
                else:
                    final[str(tao_count) + "," + letter] = float(float(count) / 350)
            else:
                final[str(tao_count)+","+letter] = float(float(count)/ 350)

    for i in range(1,len(test_letters)):
        for j in TRAIN_LETTERS:#s1
                value = 0
                for l in TRAIN_LETTERS:#s2
                    emission = float(final[str(i)+","+j])                 #Calculating Emission


                    if l+","+j in p_transistions:
                        trans = float(p_transistions[l+","+j])  #Calculatin Transistion
                    else:
                        trans = 1
                    if str(i-1)+","+l in tao:
                        if tao[str(i-1)+","+l] == 0:
                            ta = 1
                        else:
                            ta = float(tao[str(i-1)+","+l])
                    else:
                        ta = 1

                    value = float((ta)*(emission)*(trans))
                    v[str(i)+","+l] = (value)
                count = 0
                stri = ""
                for t in TRAIN_LETTERS:
                    if v[str(i)+","+t] > count:
                        count = float(v[str(i)+","+t])
                        stri = t
                tao[str(i)+","+j] = float(count)
                x[str(i)+","+j+","+stri] = float(count)

                value = 0
                v = {}
                p = i

    final1 = []
    for e in range(0, len(test_letters)):
        count = 0
        state = ""

        for s in TRAIN_LETTERS:
            if str(e) + "," + s in tao.keys():
                if float(tao[str(e) + "," + s]) > count:
                    count = float(tao[str(e) + "," + s])
                    state = s
        final1.append(state)
        count = 0


    print "HMM MAP: %s" %('').join([element for element in final1])

Simplified(train_letters, test_letters)
hmm_ve(train_letters, test_letters, train_text)
hmm_viterbi(train_letters, test_letters, train_text)
