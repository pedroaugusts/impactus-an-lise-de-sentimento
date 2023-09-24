from tweepy.auth import OAuthHandler
import tweepy as tw
from textblob import TextBlob as tb
from googletrans import Translator
from unidecode import unidecode
import pandas as pd
pd.options.mode.chained_assignment = None
import matplotlib.pyplot as plt
import plotly.express as px

#classe que possui as keys de acesso a api do twitter e realiza o processo de autenticação

class Autorizador:
    def __init__(self):
        self.api_key = ''
        self.api_key_secret = ''
        self.acess_token = ''
        self.acess_token_secret = ''



    def autorizar(self):
        """
        função que utiliza as chaves de acesso para criar um obj validador
        """
        auth = tw.OAuthHandler(self.api_key, self.api_key_secret)
        return auth


    def createapi(self):
        return tw.API(self.autorizar())



class Twitterapi(Autorizador):


    def __init__(self):
        #criando um obj do tipo Autorizador para conseguir o validador de acesso
        #criando um obj do tipo API que me permitira buscar os Tweets
        self._api = Autorizador()
        self._df = pd.DataFrame()


    def __busca(self, palavras : list[str]):
        """
        palavras : é o que você quer buscar nos tweets, podendo ser apenas uma string ou uma lista de strings
        funcao que busca os tweets mais recentes(lembrando que só é possível buscar o dos ultimos 7 dias)
        1 - coleta : tw.Cursor(blablabla)
        2 - loop que:
         2.1 - salva cada tweets pt-br em uma lista chamada lista_de_tweets
         2.2 - traduz o mesmo tweet coletado para o inglês e realiza um append em uma lista chamada tradutor
         2.3 - retira a polaridade do tweet utilizando TextBlob
          2.3.1 - TextBlop é uma biblioteca de Processamento de Linguagem Natural
          2.3.2 - Processamento de Linguagem Natural é uma área da ciência da computação que busca, através do machine learning,
                  softwares que entendam a linguagem humana
          2.3.3 - o material de treino do algoritimo se encontra na própria base de dados: corpora
           2.3.3.1 - para instalar a base de treino use a função: python -m textblob.download_corpora
        3 - retorna as 3 listas (pt,en,polaridade)

        """
        api = self.__acessarapi()

        lista_de_tweets = []
        tradutor = []
        polaridades = []

        for tweet in tw.Cursor(api.search_tweets, q= palavras , lang = "pt-br", result_type = "recent").items(1500):
            lista_de_tweets.append(tweet.text)
            pt = unidecode(tweet.text)
            texten = Translator().translate(pt)
            tradutor.append(texten.text)
            sentiment = tb(texten.text)
            polaridades.append(sentiment.polarity)
            print(".")

        return lista_de_tweets,tradutor,polaridades



    def __criardf(self, lista_de_tweets : list, tradutor : list, polaridades: list):
        #funcao que cria o df apartir dos dados coletados pela funcao __busca
        self._df = pd.DataFrame(list(zip(lista_de_tweets,tradutor,polaridades)), columns = ['Tweets',"Traduzido","Polaridade"])


    def __acessarapi(self):
        return self._api.createapi()

    # categoriza a polaridade em negativo, positivo e neutro
    def __categorizar(self):
        i=0
        for item in range(len(self._df)):
            if self._df["Polaridade"].loc[i] == 0:
                self._df['Polaridade'].loc[i] = "Neutro"

            elif self._df["Polaridade"].loc[i] > 0:
                self._df['Polaridade'].loc[i] = "Positivo"

            else:
                self._df["Polaridade"].loc[i] = "Negativo"

            i += 1


    def executar_busca(self, palavras : list[str], nomedoarquivo :str):
        #roda em ordem, todas as funções necessária de coleta, armazenamento e tratamento
        lista_de_tweets,tradutor,polaridades = self.__busca(palavras)
        self.__criardf(lista_de_tweets,tradutor,polaridades)
        self.__categorizar()
        self.__salvar(nomedoarquivo)


    #salva em um arquivo excel
    def __salvar(self, nomedoarquivo):
        x = self._df
        x.to_excel(f"{nomedoarquivo}.xlsx")



class Plotter:
    def __init__(self, caminhoproarquivo):
        self._nome = caminhoproarquivo
        self._df =pd.DataFrame()


    def __lerarquivo(self):
        self._df= pd.read_excel(f"{self._nome}.xlsx")
        self._df = self._df[["Tweets", "Traduzido", "Polaridade"]]

    def pizza(self):
        self.__lerarquivo()
        fig = self._df["Polaridade"].value_counts().plot(kind ='pie', cmap = "Blues_r",  autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2)
        return plt.show()
