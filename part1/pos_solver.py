###################################
# CS B551 Fall 2017, Assignment #3
#
# Your names and user ids:
#
# (Based on skeleton code by D. Crandall)
#
#
###########################################################################################################################
# Put your report here!!
# Approch: Firstly, i began with reading the data and updated several dictionaries, so that I can compute the
# probabilities further. For example, my program calculates All the transitions probabilities, and the prob-
# -abilities that every word has with a particular state and so on.
#
# After All the initial probabilities are calculated, I begin the main execution of the program.
#
# In simplified approach what I do is, I calculate what is the most likely probability of a particular word having
# a particular state. Then I take the maximum of it and attach that part of speech to my word and print the result.
#
# In HMM_VE, we require initial probability, emission probability and transition probability, to get the best part of
# speech tag for it. However, the part of speech for the first word does not require a transition probability
# so I have calculated the emission probability of how likely the given word is a particular part of speech and what is
# the likely hood of a part of speech being the first word. Then i have stored these values as TAO and used it further.
# When, I calculate my probabilities for other words i even multiply the transition probability. Then I take the sum
# of all the states and keep them an the next TAO i.e. for the next word. Finally, the maximum value of TAO at that
# level is given as the part of speech to the word.
#The|Noun = max((The|Noun)*(Noun|Noun)(tao|noun)+(The|Noun)*(Verb|Noun)(tao|verb))
#
# In HMM_Viterbi, I have done the same process as above to calculate all the probabilities in the similar was as above.
# However, the main difference is that instead of taking a sum of all the multiplied values i.e. emission*transition*
# Previous TAO, we take the maximum value at that stage and store it as TAO at the current stage. For example,
# The|Noun = max((The|Noun)*(Noun|Noun)(tao|noun), (The|Noun)*(Verb|Noun)(tao|verb)) so we take the maximum value.
# Finally, when we reach the last state, we take the maximum of the TAO's calculated at that stage and then check how
# did we get that value i.e. what previous state lead to this state and attach that part of speech for the previous word
# and son on.
#
# The accuracy that i could get was as follows
# So far scored 2000 sentences with 29442 words.
#                    Words correct:     Sentences correct:
#    0. Ground truth:      100.00%              100.00%
#      1. Simplified:       93.92%               47.50%
#          2. HMM VE:       92.66%               41.65%
#         3. HMM MAP:       94.36%               50.60%
# #########################################################################################################################

####

import random
import math


# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:

    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling
    def posterior(self, sentence, label):
        return 0

    # Do the training!
    #
    def train(self, data):
        first_word = {}
        first_word_count = 0
        initial_state = {}
        states = {}
        total_states_count = 0
        transistions = {}
        words = {}
        d = data
        trans_count = 0
        s_words = {}    #probability of state given a word>>>>to calculate P(W|S)
        word_only = {}
        p_transition = {}
        #print d
        # print len(d[0][0])
        for line in d:
            #for i in range(0,len(line)):
            for j in range(0, len(line[0])):
                    #print line[0][j]
                    #print line[1][j]
                    if j==0:
                        if (line[0][j] not in first_word):
                            first_word[line[0][j]] = 1
                            first_word_count += 1
                        else:
                            value = float(first_word[line[0][j]])
                            value += 1
                            first_word[line[0][j]] = float(value)
                            first_word_count += 1

                    #states will give p(noun) P(Si)
                    if line[1][j] not in states:
                        states[line[1][j]] = 1
                        total_states_count += 1
                    else:
                        value = states.get(line[1][j])
                        value += 1
                        total_states_count += 1
                        states[line[1][j]] = value




                    ###############################################################

                    #calculating P(Si+1|Si) transistions

                    if j >= 1:
                        if (line[1][j] + "," + line[1][j-1]) not in transistions:
                            transistions[(line[1][j] + "," + line[1][j-1])] = 1
                            trans_count +=1
                        else:
                            value = float(transistions.get((line[1][j] + "," + line[1][j-1])))
                            value += 1
                            trans_count += 1
                            transistions[(line[1][j] + "," + line[1][j - 1])] = value

                    #################################################################

                    #words P(Wi|Si)
                    if line[0][j] + "," + line[1][j] not in words:
                        words[line[0][j] + "," + line[1][j]] = 1
                    else:
                        value = float(words.get(line[0][j] + "," + line[1][j]))
                        value += 1
                        words[line[0][j] + "," + line[1][j]] = float(value)

                    ####################################################################
                    if line[1][j] + "," + line[0][j] not in s_words:
                        s_words[line[1][j] + "," + line[0][j]] = 1
                    else:
                        value = s_words.get(line[1][j] + "," + line[0][j])
                        value += 1
                        s_words[line[0][j] + "," + line[1][j]] = value

                    #####################################################################
                    word_only_count = 0
                    if line[0][j] not in word_only:
                        word_only[line[0][j]] = 1
                        word_only_count += 1
                    else:
                        value = word_only[line[0][j]]
                        value += 1
                        word_only_count += 1
                        word_only[line[0][j]] = value

        for s2 in states:
            for s1 in states:
                if s2 + "," + s1 in transistions:
                    trans_t = transistions[s2 + "," + s1]  # Transistion
                else:
                    trans_t = 1

                cal = 0
                for s_trans in states:
                    if s_trans + "," + s1 in transistions:
                        cal += transistions[s_trans + "," + s1]
                    else:
                        cal += 1
                trans_t *= 1000000
                cal *= 1000000
                va = float(float(trans_t)/float(cal))

                p_transition[s2 + "," + s1] = float(va)

        for e in states:
            value = float(states[e])
            x = float(value/float(total_states_count))
            initial_state[e] = x

        #print transistions
        l = [states, words, transistions, trans_count, s_words, word_only, initial_state, word_only_count, first_word_count,first_word, p_transition]
        return l



#Functions for each algorithm.
    #
    def simplified(self, sentence,l):
        # print "test"
        # print l[2]
        # print l[3]
        wd = {}
        wd = l[5]
        st = {}
        st = l[0]   #states
        #print "st"
        a = {}
        a = l[1]    #words
        all_count = {}
        final = []
        initial = {}
        initial = l[6]

        for e in sentence:  #word

            for k in l[0]:  #states
                if e+","+k in a:
                    value = float(a[e+","+k])
                    v1 = float(st[k])
                    p_w_s = float(value)
                    all_count[k] = p_w_s
                else:
                    value = float(0.0000000001)
                    v1 = float(st[k])
                    p_w_s = float(value )
                    all_count[k] = p_w_s

            if e not in wd:
                all_count = {}
                all_count["noun"] = 5


            count = 0
            state = ""
            for k in all_count:
                if all_count[k] > count:
                    # print "in"
                    count = all_count[k]
                    state = k
            final.append(state)
            all_count = {}


        return final#[ "noun" ]

    def hmm_ve(self, sentence,l):
        st = {}
        st = l[0]  # states
        # print "st"
        a = {}
        a = l[1]  # words
        trans = {}
        trans = l[2] #transistions
        c = l[3]
        all_count = {}
        final = []
        s_w = {}
        s_w = l[4] #P(S|W)
        #tao_count = -1
        value = 0
        init = {}
        init = l[6]
        emission = 0
        emission_prev = 0
        emission_count = 0
        emission_count_prev = 0
        tao = {}
        first_word = ""
        #words count and total count
        wd = {}
        wd = l[5]
        wd_co = l[7]
        p_transitions = {}
        p_transitions = l[10]

        tao_count = 0
        for k in l[0]:
            if sentence[0] + "," + k in a:
                value = float(a[sentence[0] + "," + k])
                v1 = float(st[k])
                p_w_s = float(value)
                all_count[k] = p_w_s
                tao[str(tao_count) + "," + k] = p_w_s

            else:
                value = float(1)  # float(a[e + "," + k])
                v1 = float(st[k])
                p_w_s = float(value)
                all_count[k] = p_w_s
                tao[str(tao_count) + "," + k] = p_w_s


        prev = sentence[0]

        for e in range(1,len(sentence)):
            value = 0
            for s2 in st:
                for s1 in st:
                    if s2 + "," + s1 in p_transitions:
                        trans_t = p_transitions[s2 + "," + s1]  # Transistion
                    else:
                        trans_t = 1
                    initial = tao[str(e - 1) + "," + s1]

                    emission_count = st[s2]

                    if sentence[e] + "," + s2 in a:
                        emission = float(float(a[sentence[e] + "," + s2]) / float(emission_count))  # Emission
                    else:
                        emission = (float(0.000000000000001) / float(emission_count))

                    value += float(float(initial) * float(trans_t) * float(emission))

                tao[str(e) + "," + s2] = float(float(value))
                value = 0
                emission = 0
                emission_prev = 0
            prev = sentence[e]

        for e in range(0, len(sentence)):
            count = 0
            state = ""
            for s in st:
                if tao[str(e) + "," + s] > count:  # and tao.has_key(str(e)+","+s):
                    count = tao[str(e) + "," + s]
                    state = s
            final.append(state)

        return final  # [ "noun" ] * len(sentence)

    def hmm_viterbi(self, sentence,l):

        st = {}
        st = l[0]  # states
        # print "st"
        a = {}
        a = l[1]  # words
        trans = {}
        trans = l[2]  # transistions

        c = l[3]
        all_count = {}
        final = []
        s_w = {}
        s_w = l[4]  # P(S|W)
        value = {}      #dictionary
        init = {}
        init = l[6]
        emission = 0
        emission_prev = 0
        emission_count = 0
        emission_count_prev = 0
        tao = {}
        tao_temp = {}
        first_word = ""
        # words count and total count
        wd = {}
        wd = l[5]
        wd_co = l[7]
        p_transitions = {}
        p_transitions = l[10]

        v = {}
        p = 0
        first_word_count = l[8]
        first_word = l[9]

        tao_count = 0
        for k in l[0]:
            if sentence[0] + "," + k in a:
                value = float(a[sentence[0] + "," + k])
                v1 = float(st[k])

                if sentence[0] in first_word:
                    z = first_word[sentence[0]]
                else:
                    z = 0.000000001

                p_w_s = (float(value))
                all_count[k] = p_w_s
                tao[str(tao_count) + "," + k ] = p_w_s
                tao_temp[str(tao_count) + "," + "null"] = p_w_s

            else:
                value = float(0.000001)  # float(a[e + "," + k])
                v1 = float(st[k])

                if sentence[0] in first_word:
                    z = first_word[sentence[0]]
                else:
                    z = 0.00001
                p_w_s = (float(value))
                all_count[k] = p_w_s
                tao[str(tao_count) + "," + k ] = p_w_s
                tao_temp[str(tao_count) + "," + k + "," + "null"] = p_w_s

        for e in range(1,len(sentence)):
            value = 0
            for s2 in st:
                for s1 in st:
                    if s2 + "," + s1 in p_transitions:
                        trans_t = p_transitions[s2 + "," + s1]  # Transistion
                    else:
                        trans_t = 1

                    initial = tao[str(e - 1) + "," + s1]      ####doubt

                    emission_count = st[s2]

                    if sentence[e] + "," + s2 in a:
                        emission = float(float(a[sentence[e] + "," + s2]) / float(emission_count))  # Emission
                    else:
                        emission = (float(0.00001) / float(emission_count))

                    value = float(float(float(initial) * float(trans_t) * float(emission)))
                    v[str(e)+","+s1] = float(value)

                count = 0
                state = ""

                for s in st:
                    if v[str(e) + "," + s] > count:
                        count = v[str(e) + "," + s]
                        state = s
                v = {}

                tao[str(e) + "," + s2] = count #* float(emission)

                tao_temp[str(e) + "," + s2 + "," + state] = count

                p = e

            value = 0
            emission = 0
            emission_prev = 0

        final = []
        count = 0
        stri = ""
        for s in st:
            if tao[str(p) + "," + s] > count:
                count = tao[str(p) + "," + s]
                stri = s
        final.append(stri)

        for n in range(p, -1, -1):
            for ss in st:
                if n == p:
                    if str(n)+","+stri+","+ss in tao_temp:
                        stri = ss
                        final.append(stri)
                        break
                else:
                    if n >= 0:
                        if str(n) + "," + stri + "," + ss in tao_temp:
                            stri = ss
                            final.append(stri)
                            break
        f1 = []
        for i in range(0,len(final)):
            f1.append(final.pop())

        return f1


    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, algo, sentence,l):
        if algo == "Simplified":
            return self.simplified(sentence,l)
        elif algo == "HMM VE":
            return self.hmm_ve(sentence,l)
        elif algo == "HMM MAP":
            return self.hmm_viterbi(sentence,l)
        else:
            print "Unknown algo!"

