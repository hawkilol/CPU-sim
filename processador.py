# -*- coding: utf-8 -*-
"""Processador.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/132X9slrB2MT6iwz4T0Q1ru-X5FmX1SGo
"""

memoria = {
    '00000000': 0b000110110100, #LDA
    '00000001': 0b010010110101, #Sub
    '00000010': 0b011100000101, #JN
    '00000011': 0b101010110100, #PRT
    '00000100': 0b100000000110, #jMP
    '00000101': 0b101010110101, #PRT
    '00000110': 0b001110110101, #ADD
    '00000111': 0b001010110110, #STR
    '00001000': 0b010100000101, #JZ
    '00001001': 0b011000000101, #JP
    '00001010': 0b011100000101, #JN
    '00001011': 0b100000001101, #jMP
    '00001100': 0b000000000000, #HALT
    '00001101': 0b100110110111, #GET
    '00001110': 0b101010110111, #PRT
    '00001111': 0b000000000000, #HALT
    '00010000': 0b000000000000, #HALT

    '10110100': 0b001010110011,
    '10110101': 0b000110100011,
    '10110110': 0b000000000000,
    '10110111': 0b000000000000,

}

RI=0
PC=format(0, '#010b')[2:]

Ro=0
RDM=0
REM=0

def buscar():
    global PC , RI , RDM , REM ,Ro
    print('\n--Buscando--')
    print('Ro:',Ro)

    REM = PC
    print('RDM1:',RDM)
    RDM = format(memoria['%s' % PC], '#014b')
    

    RI= RDM

    print('REM:',REM,'RDM:', RDM, 'RI:',RI, 'PC:',PC)

    PC = int(PC, 2) + int('00000001', 2)
    PC = format(PC, '#010b')[2:]

    print('PC:',PC)



def executar():
    global REM, RDM

    print('\n--Executando--')
    OPcode = RI[2:6]
    #Operando
    REM = RI[6:]
    RDM = format(memoria['%s' % REM], '#014b')
    print('OPcode:',OPcode)
    print('RDM:',RDM)
    print('Operando:',REM)

    if OPcode == '0000':
        HLT()
    if OPcode == '0001':
        LDA()
    if OPcode == '0010':
        STR()
    if OPcode == '0011':
        ADD()
    if OPcode == '0100':
        Sub()
    if OPcode == '0101':
        JZ()
    if OPcode == '0110':
        JP()
    if OPcode == '0111':
        JN()
    if OPcode == '1000':
        JMP()
    if OPcode == '1001':
        GET()
    if OPcode == '1010': #Instruções de 0 a 10
        PRT()


# Inicia o processo de busca e execução
def Start():
    while int(PC) < 111111111111111111111111:

        buscar()
        executar()



#Comandos da CPU
def HLT():
    print('\n--HALT--')
    quit()
    import sys
    sys.exit()


def LDA():
    global Ro, RDM
    print('\n--LDA--')
    Ro=RDM
    print('Ro:',Ro)


def STR():

    global memoria
    print('\n--STR--')
    endereço = REM
    dado = Ro[2:]
    dado = list(map(int, dado))
    atualizardic = {'%s' % endereço: dado}
    memoria = {key: atualizardic.get(key, memoria[key]) for key in memoria}



def ADD():
    global Ro
    print('\n--ADD--')
    Ro = int(Ro, 2) + int(RDM, 2)
    Ro = format(Ro, '#014b')[2:]
    print('Ro:', Ro)

def Sub():
    global Ro, FLAG
    print('\n--Sub--')
    Ro = int(Ro, 2) - int(RDM, 2)
    if Ro<0b000000000000:
        Ro = format(Ro, '#014b')[1:]
        FLAG='N'
        print('FLAG',FLAG)
    else:
        Ro = format(Ro, '#014b')

    print('Ro:', Ro)

def JZ():
    print('\n--JZ--')
    if Ro=='000000000000':
        PC = REM
        FLAG='Z'
        print('FLAG:',FLAG)

def JP():
    print('\n--JP--')
    if Ro>'0b000000000000':
        PC = REM
        FLAG='P'
        print('FLAG:', FLAG)

def JN():
    print('\n--JN--')
    if Ro<'000000000000':
        PC = REM
        FLAG='N'
        print('FLAG:', FLAG)

def JMP():
    print('\n--JMP--')
    global PC
    PC = REM
    print('REM:',REM)
    print('PC:',PC)

def GET():
    global memoria
    print('\n--GET--')

    endereço = REM
    dado = input('Digite um dado para o operando: ')
    dado = list(map(int, dado[2:]))
    atualizardic = {'%s' % endereço: dado}
    memoria = {key: atualizardic.get(key, memoria[key]) for key in memoria}



def PRT():
    print('\n--PRT--')
    Print=memoria['%s' % REM]
    print('PRINT(%s):' % REM,''.join(str(Print)))


#Comandos da memoria

def LListar():
    for item, amount in memoria.items():
        print('{} {}'.format(item, ' '.join(map(str, amount))))


def WEscrever():
    global memoria
    endereço = input('Digite o endereço de 4 bits: ')
    dado = input('Digite o dado de 8 bits: ')
    dado = list(map(int, dado))
    atualizardic = {'%s' % endereço: dado}
    memoria = {key: atualizardic.get(key, memoria[key]) for key in memoria}


def RLer():
    lere = input('Digite o endereço para ler')
    print(memoria['%s' % lere])


while True:
    try:
        escolher = input('Escolha INICIAR para iniciar a CPU ou Escolha a operação''\n''W para escrever,R para ler e L para listar todos: ')
    except ValueError:
        print('Isso não é um comando valido >:(')
        continue
    if escolher == 'W':
        WEscrever()
    if escolher == 'L':
        LListar()
    if escolher == 'R':
        RLer()
    if escolher == 'INICIAR':
        Start()
else:
    print('Isso não é um comando valido >:(')

#Escolher INICIAR para iniciar o processador