from nlp_preprocessing_toolbox.tokenizer import Tokenizer
from nlp_preprocessing_toolbox.sentence_splitter import SentenceSplitter
from nlp_preprocessing_toolbox.normalizer import Normalizer
from nlp_preprocessing_toolbox.stemmer import Stemmer
from nlp_preprocessing_toolbox.stopword_elimination import stopword_elimination


text = '''Çünkü ben de o yaşadığı çevreyi kirleterek bozulmasına neden olan, tüm uyarılara
kulağını tıkayan soya aitim. Kimileri buna kader diyordu, kimileri unut. Bu da
zaman ister, emek ister. İki veli dokunulsa ağlayacaktı. Bu meslek böyledir.
Filmde kamburunu çıkarmış eski Yugoslav lideri, iki kişinin arasında elleri
önden bağlı, cezaevi avlusunda yürüyor. Sabahları hiçbir şey yemeden içmeden,
paldür küldür çıkıyorum evden. Bu albüm hit şarkı çıkarmaz, dedim. Bu tesisin ,
SASA'nın büyümesinde büyük katkısı oldu. Çağırdım Genelkurmay Başkanı'nı. Ama
önce, uyumadan önce notlarıma bir çeki düzen vermem gerek. Saçlarını yıkamış.
"Hayır, ben masal istiyorum!" Helikopterler ve uçaklar da gökyüzünde uçarlar.
Postmodernleşen dünyayla birlikte edebiyatın algılanışı da dönüştü; giderek bir
eğlence nesnesi, hoşça vakit geçirme aracı olarak değerlendiriliyor. Sonradan
bir inceldi, bir inceldi. "Baba" deriz, "baba ölüm nedir?Cevap şöyleydi: Bu
soruya Veysel'in "Tabi olur." diyerek uzun uzun anlatmaya girişeceğini
zannediyordum. İstanbulspor, Vanspor, Karşıyaka, Göztepe gibi bazı kulüpler,
dernek yapısı dışında futbol şubelerini, kurulan veya kurulmuş bulunan anonim
şirketlere devrediyor. Birtakım gerilimler yaşadık. Hatta Türkiye'ye 1986
yılında geri döndükten sonra bile.'''

text = '''Saçma ve Gereksiz Bir Yazı.
Bakkaldan 5 TL'lik 2 çikola-
ta al. 12.02.2018 tarihinde saat tam 15:45'te yap-
malıyız bu işi. Tamam mı? Benimle esatmahmutbayol@gmail.com 
adresinden iletişime geçebilirsin. Yarışta 1. oldu. Doç. Dr. 
Esat Bayol'un(Böyle bir ünvanım yok!) yanından geliyorum.
12 p.m. mi yoksa 12 a.m. mi? 100 milyon insan gelmiş! www.deneme.com.tr 
adresinden sitemizi inceleyebilirsin. 24 Eylül 2018 Pazartesi günü ge-
lecekmiş. 19 Mayıs'ı coşkuyla kutladık.
Sonra dedi ki "Ben seni sevmiyorum."'''

# text = '''Saçma ve Gereksiz Bir Yazı.
# Bakkaldan 5 TL'lik 2 çikola-
# ta al. 12.02.2018 tarihinde saat tam 15:45'te yap-
# malıyız bu işi. Tamam mı? Benimle goktugocal41@gmail.com 
# adresinden iletişime geçebilirsin.'''

tokenizer = Tokenizer()
tokenizer.setText(text)
tokenizer.run()
words = tokenizer.tokens
print("\tTokenization :",words)

sentSplit = SentenceSplitter(text)
sentSplit.run()
print(sentSplit.sentences_types)
print("\tSentences :", sentSplit.sentences)
exit()

normalizer = Normalizer()
normalizer.setText(words)
words = normalizer.new_words
print("\tNormalization :",words)

stemmer = Stemmer()
stemmer.setText(words)
words = stemmer.stems
print("\tStemming :",words)

words = stopword_elimination(stemmer.stems)
print("\tStopword :",words)