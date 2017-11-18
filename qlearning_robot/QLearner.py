"""
Template for implementing QLearner  (c) 2015 Tucker Balch
"""

import numpy as np
import random as rand

class QLearner(object):

    def author(self):
        return 'hsikka3'

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):

        

        self.num_states, self.num_actions,self.alpha, self.gamma = num_states, num_actions, alpha, gamma
        self.rar, self.radr, self.s, self.a, self.dyna = rar, radr, 0, 0, dyna
        self.verbose = verbose
        self.Qtable = np.zeros((self.num_states, self.num_actions))


        
        ## setup for Dyna
        self.Rtable = np.ones((self.num_states, self.num_actions)) * -1.0
        self.Tcount = np.ones((self.num_states, self.num_actions, self.num_states)) * .00001
        self.Ttable = self.Tcount/self.Tcount.sum(axis=2, keepdims=True)
        

            
        

        

        

    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        self.s = s

        random_action = rand.randint(0, self.num_actions-1)

        max_a_value = np.amax(self.Qtable[s, :])
        count = 0
        for i in self.Qtable[s, :]:
            if i == max_a_value:
                determined_action = count
            count+=1

        # using np.where had some strange indexing that i don't like
        # potential_a = np.where(max_a_value == self.Qtable[s, :])[0]
        # determined_action = potential_a[0]
        # print determined_action

        random_chance = np.random.uniform(0.0, 1.0)

        if (self.rar > random_chance):
            self.a = random_action
            action = random_action
        else:
            self.a = determined_action
            action = determined_action
        
        
        if self.verbose: print "s =", s,"a =",action
        return action

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The ne state
        @returns: The selected action
        """

        dyna_count = self.dyna
        previous_s = self.s
        previous_a = self.a

        max_a_value = np.amax(self.Qtable[s_prime, :])

        count = 0
        for i in self.Qtable[s_prime, :]:
            if i == max_a_value:
                a_prime = count
            count+=1
          
        ## again strange indexing, resorted to loop above
        # potential_a = np.where(max_a_value == self.Qtable[s_prime,:])[0] 
        # a_prime = potential_a[0] ## wtf
        # print a_prime

        random_action = rand.randint(0, self.num_actions-1)
        random_chance = np.random.uniform(0.0, 1.0)

        
        if (self.rar > random_chance):
            action = random_action
        else:
            action = a_prime
        


        old_value = (1 - self.alpha) * self.Qtable[previous_s,previous_a]
        new_value = self.alpha * (r + self.gamma * self.Qtable[s_prime, action])
        

        self.Qtable[previous_s,previous_a] = old_value + new_value


        ## dyna portion is below
        if dyna_count > 0:
            self.Rtable[previous_s, previous_a] = (self.alpha * r) + (1 - self.alpha) * self.Rtable[previous_s,previous_a]
            self.Tcount[previous_s, previous_a, s_prime] += 1
            self.Ttable = self.Tcount/self.Tcount.sum(axis=2, keepdims=True)

            for i in range(0,dyna_count):
                dyna_action = np.random.randint(0,self.num_actions)
                dyna_state = np.random.randint(0,self.num_states)

                dyna_s_prime = np.random.multinomial(1, self.Ttable[dyna_state, dyna_action]).argmax()
                dyna_reward = self.Rtable[dyna_state, dyna_action]
                dyna_old_value = (1 - self.alpha) * self.Qtable[dyna_state,dyna_action]
                dyna_new_value = self.alpha * (dyna_reward + self.gamma * np.max(self.Qtable[dyna_s_prime]))
                # print dyna_old_value
                # print dyna_new_value
                # print 'hello'
                self.Qtable[dyna_state, dyna_action] = dyna_old_value + dyna_new_value


        






        self.s = s_prime # setting new state
        self.a = action # setting new action

        self.rar = self.rar * self.radr # decaying rar

        if self.verbose: print "s =", s_prime,"a =",action,"r =",r
        return action

if __name__=="__main__":
    print "Remember Q from Star Trek? Well, this isn't him"
    learner = QLearner(dyna=200)
    
    
    
    
    
