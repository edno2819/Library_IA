from nltk.tokenize import TweetTokenizer, ToktokTokenizer
from nltk.stem import WordNetLemmatizer
import nltk
import spacy
import re

class PreProcessingText:
    stopwords_add = ['já', 'estávamos', 'quando', 'muito', 'eles', 'meu', 'sou', 'esse', 'teus', 'tive', 'tenha',  'tenham', 'do', 'entre', 
    'estejam', 'serei', 'fôramos', 'estivemos', 'estava', 'minha', 'seriam', 'COELHO', 'estavam', 'vc', 'nossas', 'tém', 'terão', 'hão', 
    'Comments', 'temos', 'houverei', 'pelo', 'até', '3KE', 'tuas', 'tiverem', 'nos', 'houveríamos', 'hajamos', 'tivera', 'que', 
    'hei', 'tivessem', 'TOCA', 'tinha', 'eram', 'ao', 'fôssemos', 'dele', 'nossa', 'lhe', 'ele', 'estivera', 'Forwarded message',
    'estivéramos', 'fora', 'essa', 'tivemos', 'a', 'por', 'aqueles', 'hajam', 'seria', 'dela', 'https', 'Os', 'este', 'estamos', 
    'tenho', 'houve', 'tem', 'dos', 'à', 'lhes', 'será', 'for', 'da', 'fui', 'terá', 'plotlygraphs', 'estivessem', 'vcs', 'esteve', 
    'somos', 'delas', 'teu', 'elas', 'qual', 'aquelas', 'serão', 'aquilo', '4k', 'sua', 'e', 'pelas', 'pra', 'houver', 'para', 'nas', 'aquela', 
    'estas', 'houveriam', 'estive', 'esta', 'nem', 'estejamos', 'havemos', 'era', 'teve', 'as', 'fosse', 'isto', 'eu', 'o', 'estes', 'houvesse',
    'estiver', 'DE', 'haja', 'Forwarded', 'na', 'aquele', 'seremos', 'é', 'éramos', 'uma', 'mas', 'me', 'esteja', 'houveria', '2k', 'das', 'tu', 
    'no', 'houverem', 'num', 'tinham', 'vos', 'estou', 'houvemos', 'você', 'estiverem', 'terei', 'estivermos', 'pelos', 'meus', 'houveram', 'formos', 
    'NA', 'houverão', 'numa', 'com', 'como', 'também', 'nossos', 'deles', 'houvéssemos', 'foram', 'br', 'né', 'seu', 'tínhamos', 'houverá', 
    'só', 'nosso', 'em', 'depois', 'os', 'tiveram', 'tivéramos', 'sem', 'nós', 'tivesse', 'está', 'vocês', 'houvéramos', 
    'tivermos', 'seus', 'mais', 'essas', 'teriam', 'minhas', 'sejamos', 'O', 'forem', 'um', 'estivéssemos', 'houvessem', 'se', 
    'estiveram', 'fossem', 'seríamos', '3k', 'de', 'mesmo', 'teremos', 'aos', 'isso', 'suas', 'são', 'n', 'message', 'tenhamos', 'tivéssemos', 
    'estão', 'fomos', 'sejam', 'tua', 'houvera', 'estivesse', 'te', 'às', 'quem', 'ela', 'ou', 'esses', 'houvermos', 'houveremos', 'pela', 'q', 'teríamos', 
    'HTTPS', 'HTTP', 'http', 'ndd'] 

    STOPWORDS = set(nltk.corpus.stopwords.words('portuguese'))
    STOPWORDS.remove('não')
    STOPWORDS.remove('mas')
    STOPWORDS.remove('nem')
    STOPWORDS.update(stopwords_add)

    def __init__(self) -> None:
        '''nltk.download()
        nltk.download('wordnet')
        nltk.download('omw-1.4')
        nltk.download('rslp')
        python -m spacy download pt'''

        self.wordnet_lemmatizer = WordNetLemmatizer()
        self.tweet_tokenizer = TweetTokenizer()
        self.stemmer = nltk.stem.RSLPStemmer()
        self.toktok = ToktokTokenizer()
        self.spacy_lemma = spacy.load('pt_core_news_sm')


    def del_word(self, instance, word):
        while instance.find(word)!=-1:
            instance  = instance.replace(word, '')
        return instance
    
    def tokenizeTokTok(self, instance):
        '''Separa as palavras de acentos '''
        return self.toktok.tokenize(instance, return_str=True)

    def RemoveStopWords(self, instance):
        palavras = [i for i in instance.split() if not i in self.STOPWORDS]
        instance = self.del_word(" ".join(palavras), 'https')
        return (instance)

    def Limpeza_dados(self, instancia):
        remove = ['.', ';', '-', ':', ')', '(', '_', '@', '!', "?", ',']
        instancia = re.sub(r"http\S+", "", instancia).lower()
        for item in remove:
            instancia = instancia.replace(item, '')
        return instancia

    def Stemming(self, instancia):
        '''Na stemming vamos analisar cada palavra individualmente e reduzi-la à sua raiz'''
        palavras = []
        for w in instancia.split():
            palavras.append(self.stemmer.stem(w))
        return (" ".join(palavras))


    def Lemmatization(self, instancia):
        palavras = []
        for w in instancia.split():
            palavras.append(self.wordnet_lemmatizer.lemmatize(w))
        return (" ".join(palavras))

    def Lemmatization_Spacy(self, instancia):
        '''Já usa o toktok e funciona melhor que o Lemmatization'''
        phase = self.spacy_lemma(instancia)
        return (" ".join([token.lemma_ for token in phase]))

    def To_negation(self, texto):
        negacoes = ['não','not', 'nao']
        negacao_detectada = False
        resultado = []
        palavras = texto.split()
        for p in palavras:
            p = p.lower()
            if negacao_detectada == True:
                p = p + '_neg'
            if p in negacoes:
                negacao_detectada = True
            resultado.append(p)
        return (" ".join(resultado))


    def pop_indexs(self, data, exclud):
        count=0
        for c in sorted(exclud):
            data.pop(c+count)
            count-=1
        return data

class PipelineProcessText(PreProcessingText):

    def __init__(self) -> None:
        super().__init__()
    
    def preprocessingFullNeg(self, instancia):
        instancia = self.tokenizeTokTok(instancia)
        instancia = self.Limpeza_dados(instancia)
        instancia = self.RemoveStopWords(instancia)
        instancia = self.Lemmatization_Spacy(instancia)
        instancia = self.To_negation(instancia)
        return instancia

    def preprocessingFull(self, instancia):
        instancia = self.tokenizeTokTok(instancia)
        instancia = self.Limpeza_dados(instancia)
        instancia = self.RemoveStopWords(instancia)
        instancia = self.Lemmatization_Spacy(instancia)
        return instancia




if __name__ == '__main__':
    a = PipelineProcessText()
    text = 'teste de frase para aviriguar, teste, sacou? o tempo verbal passaram amigos'
    a.Limpeza_dados(text)
    a.RemoveStopWords(text)
    a.Lemmatization(text)
    a.Lemmatization_Spacy(text)
    a.tokenizeTokTok(text)
    # remove_itens_x([1,2,3,1,5,47,8,4,1,31,5,'sd'], 1, 2)

    # print(Preprocessing(['teste amiga! dessa função de expliti e tambem:']))