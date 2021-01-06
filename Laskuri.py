import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *


class Asunto:

    def __init__(self, korko_sken=0):
        """ Tämä init metodi asettaa arvot asunto-objektille. """

        self.hinta = float(kohde_hinta.get())             # asunnon velaton hinta
        self.oma = float(omarahoitus.get())               # omarahoitusosuus
        self.yvastike = float(vastike.get())              # yhtiövastike
        self.vkorko = float(korko.get())/100+korko_sken   # todellinen vuosikorko
        self.l_aika = int(aika.get())                     # laina-aika vuosina
        self.era = int(era_lkm.get())                     # maksuerien määrä vuodessa
        self.era_lkm = self.era*self.l_aika               # maksuerien kokonaismäärä
        self.vuokra = float(vuokraa.get())                # vuokra
        self.laina = self.hinta - self.oma                # lainan määrä
        self.annuiteetti = self.laina * ((1 + self.vkorko/self.era) **          # annuiteetti per maksuerä; huom jos erä=6 --> annuiteetti*2*kk
                           self.era_lkm * (self.vkorko /self.era)) / \
                          ((1 + self.vkorko / self.era) ** self.era_lkm - 1)

        self.kassavirta = (self.vuokra - self.yvastike) * (12 / self.era) - self.annuiteetti
        self.kok_korko = self.era_lkm * self.annuiteetti - self.laina # koron määrä

        self.create_data()
        print(self.kassavirta, self.annuiteetti)

    def create_data(self):
        """ Tämä metodi palauttaa Pandas DataFramen,
         jossa ovat laina- ja tuottotiedot jokaiselta kuukaudelta. """

        jaljella = self.laina       # jäljellä oleva laina looppia varten

        data = pd.DataFrame(columns=['Vuosi & Maksuerä', 'Koko pääoma tuotto %',
                                     'Oman pääoman tuotto %', 'Oma pääoma',
                                     'Jäljellä oleva laina', 'Korkokulut',
                                     'Lyhennys', 'Kassavirta'])

        for i in range(self.l_aika): # vuosi loop
            for m in range(self.era): # maksuerät vuodessa loop (kk)

                korko = (1 / self.era) * self.vkorko * jaljella         # 1/6 * 1% * 70 000 = 116.67€ korko/2kk
                lyhennys = self.annuiteetti - korko                     # 321.93€ - 116.67€ = 205.26€ lyhennys/2kk

                jaljella = jaljella - lyhennys      # jäljellä oleva laina
                oma_poma = self.hinta - jaljella    # oma pääoma

                opo_tuotto = ((self.vuokra - self.yvastike)*(12/self.era) - korko) * self.era / oma_poma * 100
                kok_poma_tuotto =  (self.vuokra - self.yvastike) * 12  / self.hinta * 100

                data = data.append({'Vuosi & Maksuerä': (i + 1, m + 1),
                                    'Koko pääoma tuotto %': kok_poma_tuotto,
                                    'Oman pääoman tuotto %': opo_tuotto,
                                    'Oma pääoma': oma_poma,
                                    'Jäljellä oleva laina': jaljella,
                                    'Korkokulut': korko,
                                    'Lyhennys': lyhennys,
                                    'Kassavirta': self.kassavirta},
                                    ignore_index=True)
        self.data = data



def korko_skenaariot():

    skenaariot = list(range(0,5,1))
    objektit = []

    # tekee eri skenaariot omaksi objekteiksi
    for i in skenaariot:
        sken = Asunto(i/100)        # objekti jokaisesta skenaariosta i/100 jotta prosentti
        objektit.append(sken)       # jokainen skenaatio omaksi objetiksi

    list_box.delete(0,'end')

    for i in range(len(objektit)):

        list_box.insert(END, "Korkoskenaario "+ str(round(objektit[i].vkorko*100,2))+"%")
        info = "Oman pääoman tuotto alussa: "+str(round(objektit[i].data.loc[0,'Oman pääoman tuotto %'],2))+'% '+\
               "Kassavirta: "+str(round(objektit[i].data.loc[0,'Kassavirta'],2))+' € '\
               "Lainan annuiteetti: "+  str(round(objektit[i].annuiteetti,2))+' € '\
               "Korkokulut maturiteettiin: "+str(round(objektit[i].kok_korko,2))+' €'

        list_box.insert(END, info)
        list_box.insert(END, '')

    # tee kuvaaja eri skenaarioilla
    fig, axes = plt.subplots(1, figsize=(12, 8))

    for i in range(len(objektit)):
        axes.plot(objektit[i].data.loc[:, 'Oman pääoman tuotto %'], label='Oman pääoman tuotto % (korko {}%)'.format(round(objektit[i].vkorko*100,2)))

    axes.plot(objektit[0].data.loc[:, 'Koko pääoma tuotto %'], label='Koko pääoman tuotto %')
    axes.set_ylim([0, objektit[0].data.iloc[0, 2] + 1])
    axes.set_ylabel('%')
    plt.title('Vuokratuotto')
    axes.legend()
    plt.show()

    objektit[0].data.to_excel('data.xlsx')


# ***** GRAPHIC SECTION *****

app = Tk()
app.title('Asuntosijoituslaskuri')
app.geometry('900x600') # size

float_var = tk.IntVar()

main_header = Label(app, text="Asuntosijoituslaskuri", font=('Arial',20), pady=20, padx=15)
main_header.grid(row=0,column=0)

# HINTA
label_hinta = Label(app, text='Asunnon hinta (€)', font=('bold',11),pady=4,padx=15)
label_hinta.grid(row=1,column=0, sticky=W)
kohde_hinta = Entry(app, width=20)
kohde_hinta.grid(row=1,column=1, sticky=W)

# OMARAHOITUS
label_omarahoitus = Label(app, text='Omarahoitusosuus (€)',font=('bold',11),pady=4,padx=15)
label_omarahoitus.grid(row=2,column=0, sticky=W)
omarahoitus = Entry(app, width=20, textvariable='omarahoitus')
omarahoitus.grid(row=2, column=1, sticky=W)

# YHTIÖVASTIKE
label_y_vastike = Label(app, text='Yhtiövastike (€/kk)',font=('bold',11),pady=4,padx=15)
label_y_vastike.grid(row=3,column=0, sticky=W)
vastike = Entry(app, width=20)
vastike.grid(row=3, column=1,sticky=W)

# VUOSIKORKO
label_korko = Label(app, text='Lainan todellinen vuosikorko (%)',font=('bold',11),pady=4,padx=15)
label_korko.grid(row=4,column=0, sticky=W)
korko = Entry(app, width=10)
korko.grid(row=4, column=1,sticky=W)

# LAINA-AIKA
label_aika = Label(app, text='Laina-aika vuosina',font=('bold',11),pady=4)
label_aika.grid(row=1,column=3, sticky=W)
aika = Entry(app, width=10)
aika.grid(row=1, column=4,sticky=W)

# ERIEN MÄÄRÄ VUODESSA
label_era_lkm = Label(app, text='Maksuerien lkm vuodessa (kerran kk =12)',font=('bold',11),pady=4)
label_era_lkm.grid(row=2,column=3, sticky=W)
era_lkm= Entry(app, width=10)
era_lkm.grid(row=2, column=4,sticky=W)

# VUOKRA
label_vuokraa = Label(app, text='Vuokra (€/kk)',font=('bold',11),pady=4)
label_vuokraa.grid(row=3,column=3, sticky=W)
vuokraa= Entry(app, width=20)
vuokraa.grid(row=3, column=4, sticky=W)

# listbox
list_box = Listbox(app, height=15, width=120, border=1)
list_box.grid(row=12, column=0, columnspan=5, rowspan=10, pady=20,padx=10)

# scrollbar
scrollbar_y = Scrollbar(app)
scrollbar_y.grid(row=12, column=5,pady=20)
list_box.configure(yscrollcommand=scrollbar_y.set)
scrollbar_y.config(command=list_box.yview())


# BUTTONS
sulje = Button(app,text='Sulje', width = 8, command=exit)
sulje.grid(row=10, column=3)
laske = Button(app, text='Laske', width = 12, command=korko_skenaariot)
laske.grid(row=10,column=4)

app.mainloop()
































