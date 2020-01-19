# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 21:15:02 2020

@author: Claire PLECHE <plecheclaire@gmail.com>
"""
# !pip install pygame

# IMPORT PACKAGES
import pandas
import os
import pygame
import time
import random

# SET DIRECTORY
os.chdir('C:\\Users\\Claire PLECHE\\PCBS_srt.git\\stimuli\\')

# IMPORT MENU (created and saved in directory before)
import menu

# SET SCREEN SIZE // Check that zoom display on computer is 100% and not more on Windows
width = int(1920)
height = int(1080)

#LOAD STIMULI (PICTURES for task, instructions, breaks)
Close_pics = list()
Spaced_pics = list()
for i in range(1,5):
    img1 = pygame.image.load('Inputs/test_close_position'+str(i)+'.jpg')
    img1= pygame.transform.smoothscale(img1,(width,height))
    Close_pics.append(img1)

    img2 = pygame.image.load('Inputs/test_spaced_position'+str(i)+'.jpg')
    img2= pygame.transform.smoothscale(img2,(width,height))
    Spaced_pics.append(img2)



pic_INSTRUCTIONS = pygame.image.load('Inputs/instructions.jpg')
pic_INSTRUCTIONS= pygame.transform.smoothscale(pic_INSTRUCTIONS,(width,height))


pic_pause = pygame.image.load('Inputs/pause.png')
pic_pause= pygame.transform.smoothscale(pic_pause,(width,height))

#INIT PYGAME AND DISPLAY
pygame.init()
window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
window.fill(color=(0,0,0))
clock = pygame.time.Clock()

print(window.get_size())
pygame.display.set_caption('Revised SRT Task')


#DEFINE SEQUENCE (order of picture presentation for the testing blocks aka Sequence Blocks)
Seq1 = (0,3,2,1,2,0,3,2,1,0)

#CONDITION for allowed KEYS
def COND(event):
    return event.type == pygame.KEYDOWN and (event.key==pygame.K_a or event.key==pygame.K_d or event.key==pygame.K_k or event.key==pygame.K_SEMICOLON )


# DEFINE THE TWO TYPES OF BLOCKS (random and sequence)
# block with pictures randomly presented
def RANDOM_BLOCK(N_BLOCK,tps):
    Results = pandas.DataFrame()
    i=0
    rnd = random.randint(0,3)
    window.blit(pics[rnd], (0,0))
    pygame.display.flip()
    carry_on=True
    T0 = time.time()
    while carry_on:

        T1=time.time()
        #CONDITION ACCORDING TO TIME (IF NO EVENT BUT DISPLAY TOO LONG THEN CHANGES PICTURE)
        if T1-T0>tps and i< 10:
            Results = Results.append({'BLOCK':N_BLOCK,'TRIAL':i,'CORRECT_ANS':rnd,'KEY_PRESSED':'TIME_ELAPSED','TIME':tps,'SPEED':tps},    ignore_index=True)
            T0 = time.time()
            nextrnd = random.randint(0,3)
            while rnd == nextrnd:
                nextrnd = random.randint(0,3)

            window.blit(pics[nextrnd], (0,0))
            pygame.display.flip()
            rnd= nextrnd
            i=i+1
        if T1-T0>tps and i==10:
                carry_on=False
                T0 = time.time()

        # CONDITION IF KEY PRESSED BEFORE THE LIMIT TIME OF DISPLAY (records key and changes picture)
        for event in pygame.event.get():
            if COND(event) and i< 10:
                Results = Results.append({'BLOCK':N_BLOCK,'TRIAL':i,'CORRECT_ANS':rnd,'KEY_PRESSED':event.unicode,'TIME':T1-T0,'SPEED':tps},    ignore_index=True)
                T0 = time.time()
                nextrnd = random.randint(0,3)
                while rnd == nextrnd:
                    nextrnd = random.randint(0,3)

                window.blit(pics[nextrnd], (0,0))
                pygame.display.flip()
                rnd= nextrnd
                i=i+1
            if (event.type == pygame.KEYDOWN and event.key== pygame.K_ESCAPE) or i==10:
                carry_on=False
                T0 = time.time()


        clock.tick(100)
    pygame.display.flip()
    return Results


# block in which the pictures are presented in a specific order, defined in Seq1
def SEQUENCE_BLOCK(N_BLOCK,tps):
    Results = pandas.DataFrame()
    i=0
    print(i)
    window.blit(pics[Seq1[i]], (0,0))
    pygame.display.flip()
    carry_on=True
    T0 = time.time()
    while carry_on:

        T1=time.time()
        #CONDITION ACCORDING TO TIME
        if T1-T0>tps and i< len(Seq1):
            Results = Results.append({'BLOCK':N_BLOCK,'TRIAL':i,'CORRECT_ANS':Seq1[i],'KEY_PRESSED':'TIME_ELAPSED','TIME':tps,'SPEED':tps},    ignore_index=True)
            T0 = time.time()
            i=i+1
            if i<len(Seq1):
                window.blit(pics[Seq1[i]], (0,0))
                pygame.display.flip()
        if T1-T0>tps and i==len(Seq1) :
                carry_on=False
                T0 = time.time()


        for event in pygame.event.get():
            if COND(event) and i< len(Seq1):
               Results = Results.append({'BLOCK':N_BLOCK,'TRIAL':i,'CORRECT_ANS':Seq1[i],'KEY_PRESSED':event.unicode,'TIME':T1-T0,'SPEED':tps},    ignore_index=True)
               T0 = time.time()
               i=i+1
               if i<len(Seq1):
                   window.blit(pics[Seq1[i]], (0,0))
                   pygame.display.flip()
            if (event.type == pygame.KEYDOWN and event.key== pygame.K_ESCAPE) or i==len(Seq1) :
                carry_on=False
                T0 = time.time()

        pygame.display.flip()
        clock.tick(100)

    return Results


#FONCTION for a PAUSE, continues on with the task when the participant presses the Return key
def PAUSE_click():
    #WHITE SCREEN
    window.blit(pic_pause, (0,0))

    pygame.display.flip()

    carry_on=True
    while carry_on:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                carry_on=False
        pygame.display.flip()
        clock.tick(100)



#FONCTION that displays the instructions, the participant decides to start the task by pressing on the return key
def PAUSE_instructions():
    #WHITE SCREEN
    window.blit(pic_INSTRUCTIONS, (0,0))

    pygame.display.flip()

    carry_on=True
    while carry_on:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                carry_on=False
        pygame.display.flip()
        clock.tick(100)




######           RUN - MAIN PROGRAM          ##########

#CREATE RESULTS DATAFRAME
Results = pandas.DataFrame(columns=['BLOCK','TRIAL','CORRECT_ANS','KEY_PRESSED','TIME','SPEED'])

# MENU is displayed: enter number of participant, choose if spaced or closed pictures will be used, choose if the display time is short or long
Subject = menu.MENU_SRT(window)

Speeds = (0.65, 0.95)

tps= Speeds[Subject['speed'][0]]


if Subject['close_spaced'][0]==1:
    pics = Close_pics
else:
    pics = Spaced_pics



#INSTRUCTIONS are displayed

PAUSE_instructions()

#DEFINE order and number of random + sequence blocks
Blocks = (1,1,2,2,2,2,1,1,2,2,2,2)

N_rep=8 ### CHOOSE the number of time the 1Oitem sequence(or random) is going to be repeated BY BLOCK
n_block=1 #k tarverse block de 1 à 12

for bk in Blocks:
    if bk==1:
        for n in range(N_rep):
            Results = Results.append(RANDOM_BLOCK(n_block,tps))
        PAUSE_click()
    if bk==2:
        for n in range(N_rep):
            Results = Results.append(SEQUENCE_BLOCK(n_block,tps))
        PAUSE_click()
    n_block=n_block+1

# end of task
pygame.quit()


Results.to_csv('C:\\Users\\Claire PLECHE\\PCBS_srt.git\\data\\'+str(Subject['ID_subj'][0])+'_Results'+'.csv',sep=';')
Subject.to_csv('C:\\Users\\Claire PLECHE\\PCBS_srt.git\\data\\'+str(Subject['ID_subj'][0])+'_Subject.csv',sep=';')
