# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 21:12:49 2020

@author: Claire PLECHE
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 21:15:02 2020

@author: Claire PLECHE
"""
# !pip install pygame
import pandas
import os
import pygame



os.chdir('C:\\Users\\Claire PLECHE\\PCBS_srt.git\\stimuli\\')


#SCREEN SIZE
width = int(1920)
height = int(1080)


def MENU_SRT(window):
    pic_close = pygame.image.load('Inputs/Menu_close.jpeg')
    pic_close= pygame.transform.smoothscale(pic_close,(width,height))

    pic_spaced = pygame.image.load('Inputs/Menu_spaced.jpeg')
    pic_spaced= pygame.transform.smoothscale(pic_spaced,(width,height))

    pic_fast= pygame.image.load('Inputs/Menu_fast.jpeg')
    pic_fast= pygame.transform.smoothscale(pic_fast,(width,height))


    pic_slow= pygame.image.load('Inputs/Menu_slow.jpeg')
    pic_slow= pygame.transform.smoothscale(pic_slow,(width,height))


    clock = pygame.time.Clock()




    def id_subject():
        id = ""
        font = pygame.font.Font(None, 50)
        carry_on=True
        while carry_on==True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.unicode.isnumeric():
                        id = id + event.unicode
                    elif event.key == pygame.K_BACKSPACE: #supprimer caractère chaine
                        id = id[:-1]
                    elif event.key == pygame.K_RETURN:
                        carry_on=False


            window.fill((0, 0, 0))
            block = font.render('Subject ID : '+id, True, (255, 255, 255))
            rect = block.get_rect()
            rect.center = window.get_rect().center
            window.blit(block, rect)
            pygame.display.flip()

        return str(id)


    def MENU1():
        #WHITE SCREEN
        choice = 1
        window.blit(pic_close, (0,0))

        pygame.display.flip()

        carry_on=True
        while carry_on:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key==pygame.K_RIGHT:
                    window.blit(pic_spaced, (0,0))
                    pygame.display.flip()
                    choice=2
                if event.type == pygame.KEYDOWN and event.key==pygame.K_LEFT:
                    window.blit(pic_close, (0,0))
                    pygame.display.flip()
                    choice=1
                if event.type == pygame.KEYDOWN and event.key==pygame.K_RETURN:
                    carry_on=False
            pygame.display.flip()
            clock.tick(100)

        return choice

    def MENU2():
        #WHITE SCREEN
        choice = 0
        window.blit(pic_fast, (0,0))

        pygame.display.flip()

        carry_on=True
        while carry_on:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key==pygame.K_RIGHT:
                    window.blit(pic_slow, (0,0))
                    pygame.display.flip()
                    choice=1
                if event.type == pygame.KEYDOWN and event.key==pygame.K_LEFT:
                    window.blit(pic_fast, (0,0))
                    pygame.display.flip()
                    choice=0
                if event.type == pygame.KEYDOWN and event.key==pygame.K_RETURN:
                    carry_on=False
            pygame.display.flip()
            clock.tick(100)

        return choice



    def RUN_menu():
        Menu_Choices= pandas.DataFrame(columns=['ID_subj','close_spaced','speed'])
        Menu_Choices= Menu_Choices.append(  {'ID_subj':id_subject(),'close_spaced':MENU1(),'speed':MENU2()}, ignore_index=True)
        return Menu_Choices

    return RUN_menu()
