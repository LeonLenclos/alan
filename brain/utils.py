
import string
import unicodedata
from difflib import SequenceMatcher
import math

############
# CLEANING #
############

stopwords = ["a","abord","absolument","afin","ah","ai","aie","aient","aies","ailleurs","ainsi","ait","allaient","allo","allons","allô","alors","anterieur","anterieure","anterieures","apres","après","as","assez","attendu","au","aucun","aucune","aucuns","aujourd","aujourd'hui","aupres","auquel","aura","aurai","auraient","aurais","aurait","auras","aurez","auriez","aurions","aurons","auront","aussi","autre","autrefois","autrement","autres","autrui","aux","auxquelles","auxquels","avaient","avais","avait","avant","avec","avez","aviez","avions","avoir","avons","ayant","ayez","ayons","b","bah","bas","basee","bat","beau","beaucoup","bien","bigre","bon","boum","bravo","brrr","c","car","ce","ceci","cela","celle","celle-ci","celle-là","celles","celles-ci","celles-là","celui","celui-ci","celui-là","celà","cent","cependant","certain","certaine","certaines","certains","certes","ces","cet","cette","ceux","ceux-ci","ceux-là","chacun","chacune","chaque","cher","chers","chez","chiche","chut","chère","chères","ci","cinq","cinquantaine","cinquante","cinquantième","cinquième","clac","clic","combien","comme","comment","comparable","comparables","compris","concernant","contre","couic","crac","d","da","dans","de","debout","dedans","dehors","deja","delà","depuis","dernier","derniere","derriere","derrière","des","desormais","desquelles","desquels","dessous","dessus","deux","deuxième","deuxièmement","devant","devers","devra","devrait","different","differentes","differents","différent","différente","différentes","différents","dire","directe","directement","dit","dite","dits","divers","diverse","diverses","dix","dix-huit","dix-neuf","dix-sept","dixième","doit","doivent","donc","dont","dos","douze","douzième","dring","droite","du","duquel","durant","dès","début","désormais","e","effet","egale","egalement","egales","eh","elle","elle-même","elles","elles-mêmes","en","encore","enfin","entre","envers","environ","es","essai","est","et","etant","etc","etre","eu","eue","eues","euh","eurent","eus","eusse","eussent","eusses","eussiez","eussions","eut","eux","eux-mêmes","exactement","excepté","extenso","exterieur","eûmes","eût","eûtes","f","fais","faisaient","faisant","fait","faites","façon","feront","fi","flac","floc","fois","font","force","furent","fus","fusse","fussent","fusses","fussiez","fussions","fut","fûmes","fût","fûtes","g","gens","h","ha","haut","hein","hem","hep","hi","ho","holà","hop","hormis","hors","hou","houp","hue","hui","huit","huitième","hum","hurrah","hé","hélas","i","ici","il","ils","importe","j","je","jusqu","jusque","juste","k","l","la","laisser","laquelle","las","le","lequel","les","lesquelles","lesquels","leur","leurs","longtemps","lors","lorsque","lui","lui-meme","lui-même","là","lès","m","ma","maint","maintenant","mais","malgre","malgré","maximale","me","meme","memes","merci","mes","mien","mienne","miennes","miens","mille","mince","mine","minimale","moi","moi-meme","moi-même","moindres","moins","mon","mot","moyennant","multiple","multiples","même","mêmes","n","na","naturel","naturelle","naturelles","ne","neanmoins","necessaire","necessairement","neuf","neuvième","ni","nombreuses","nombreux","nommés","non","nos","notamment","notre","nous","nous-mêmes","nouveau","nouveaux","nul","néanmoins","nôtre","nôtres","o","oh","ohé","ollé","olé","on","ont","onze","onzième","ore","ou","ouf","ouias","oust","ouste","outre","ouvert","ouverte","ouverts","o|","où","p","paf","pan","par","parce","parfois","parle","parlent","parler","parmi","parole","parseme","partant","particulier","particulière","particulièrement","pas","passé","pendant","pense","permet","personne","personnes","peu","peut","peuvent","peux","pff","pfft","pfut","pif","pire","pièce","plein","plouf","plupart","plus","plusieurs","plutôt","possessif","possessifs","possible","possibles","pouah","pour","pourquoi","pourrais","pourrait","pouvait","prealable","precisement","premier","première","premièrement","pres","probable","probante","procedant","proche","près","psitt","pu","puis","puisque","pur","pure","q","qu","quand","quant","quant-à-soi","quanta","quarante","quatorze","quatre","quatre-vingt","quatrième","quatrièmement","que","quel","quelconque","quelle","quelles","quelqu'un","quelque","quelques","quels","qui","quiconque","quinze","quoi","quoique","r","rare","rarement","rares","relative","relativement","remarquable","rend","rendre","restant","reste","restent","restrictif","retour","revoici","revoilà","rien","s","sa","sacrebleu","sait","sans","sapristi","sauf","se","sein","seize","selon","semblable","semblaient","semble","semblent","sent","sept","septième","sera","serai","seraient","serais","serait","seras","serez","seriez","serions","serons","seront","ses","seul","seule","seulement","si","sien","sienne","siennes","siens","sinon","six","sixième","soi","soi-même","soient","sois","soit","soixante","sommes","son","sont","sous","souvent","soyez","soyons","specifique","specifiques","speculatif","stop","strictement","subtiles","suffisant","suffisante","suffit","suis","suit","suivant","suivante","suivantes","suivants","suivre","sujet","superpose","sur","surtout","t","ta","tac","tandis","tant","tardive","te","tel","telle","tellement","telles","tels","tenant","tend","tenir","tente","tes","tic","tien","tienne","tiennes","tiens","toc","toi","toi-même","ton","touchant","toujours","tous","tout","toute","toutefois","toutes","treize","trente","tres","trois","troisième","troisièmement","trop","très","tsoin","tsouin","tu","té","u","un","une","unes","uniformement","unique","uniques","uns","v","va","vais","valeur","vas","vers","via","vif","vifs","vingt","vivat","vive","vives","vlan","voici","voie","voient","voilà","vont","vos","votre","vous","vous-mêmes","vu","vé","vôtre","vôtres","w","x","y","z","zut","à","â","ça","ès","étaient","étais","était","étant","état","étiez","étions","été","étée","étées","étés","êtes","être","ô"]

def remove_stopwords(list_of_words):
    """Take a list of words and return the list without stopwords."""
    return [w for w in list_of_words if w not in stopwords]

def remove_accents(input_str):
    """Take a string and return the string with ascii characters only."""
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii.decode('ascii')

def remove_punctuation(input_str, gramatical_punctuation_to_spaces=True):
    """Take a string and return the string witout punctuation
    and with spaces instead of apostrophes"""
    exclude = set(string.punctuation)
    exclude.discard("'")
    exclude.discard("-")
    if gramatical_punctuation_to_spaces:
        input_str = input_str.replace("'", " ").replace("-", " ")
    return ''.join(ch for ch in input_str if ch not in exclude)

def clean(input_str):
    """Take a string return a cleaned string
    remove accents, remove punctuation, convert to lowercase"""
    return remove_accents(remove_punctuation(input_str.lower()))



#############
# COMPATING #
#############

def compare(s, compare_to):
    """Take a string and something to compare. Return a distance ratio.
    Also clean strings before comparing
    s must be a string
    compare_to can be a string or a list of strings"""
    s = clean(s)
    if type(compare_to) == str:
        compare_to = clean(compare_to)
        ratio = SequenceMatcher(None, s, compare_to).ratio()
    else :
        try:
            max_ratio = 0
            for s2 in compare_to:
                ratio = SequenceMatcher(None, s, s2).ratio()
                if ratio > max_ratio : max_ratio = ratio
            ratio = max_ratio
        except TypeError:
            raise TypeError(
                "string must be compared to a string or list of strings")
<<<<<<< HEAD
    return math.exp(3*ratio-3)


##############
# SUBSTITUTE #
##############


# oral elision (illegal elisions) to the right form
elision_sub = [
    ("t'es", "tu es"),
    ("t'as", "tu as"),
    ("t'aimes", "tu aimes")
]

# person reference id reversed
person_sub = [
    ("j'ai", "tu as"),
    ("nous avons", "vous avez"),
    ("je suis", "tu es"),
    ("j'aime", "tu aimes"),
    ("m'aime", "t'aime"),
    ("je t'aime", "tu m'aimes"),
    ("m'aimes", "t'aimes"),
    ("tu t'aimes", "je m'aimes"),
    ("nous sommes", "vous êtes"),
    ("mon", "ton"),
    ("ma", "ta"),
    ("moi", "toi"),
    ("mes", "tes"),
    ("je", "tu"),
    ("nous", "vous"),
    ("nos", "vos")
]
person_sub.extend([sub[::-1] for sub in person_sub])

def substitute(s, sub_list):
    """take a string and list of substitutions (tuple list)
    remove punctuation, lower and return it with the substituted ellements
    only substitute ellement with space around"""
    s = remove_punctuation(s, False).lower()
    for i, (a, b) in enumerate(sub_list):
        s = (" %s "%s).replace((" %s "%a)," <%s> "%i)
    for i, (a, b) in enumerate(sub_list):
        s = s.replace("<%s>"%i,b)
    return s.strip()

def do_person_sub(s):
    """Take a string and return it with person substitued.
    Try to work with elisions exceptions"""
    s = substitute(s, elision_sub)
    s = substitute(s, person_sub)
    return s

subject_i = [
    ("moi je suis", "-subject- est"),
    ("moi j'ai", "-subject- a"),
    ("moi j'aime", "-subject- aime"),
    ("je suis", "-subject- est"),
    ("j'ai", "-subject- a"),
    ("j'aime", "-subject- aime"),
    ("j'", "-subject-"),
    ("je", "-subject-"),
    ("moi", "-subject-")
]

subject_you = [
    ("toi tu es", "-subject- est"),
    ("toi t'as", "-subject- a"),
    ("toi tu aimes", "-subject- aime"),
    ("tu es", "-subject- est"),
    ("tu as", "-subject- a"),
    ("tu aimes", "-subject- aime"),
    ("t'", "-subject-"),
    ("tu", "-subject-"),
    ("toi", "-subject-")
]

def do_subject_sub(s, sub_list, subject):
    """take a string a substitution list (list of tuple) and a subject (str)
    the substitution list may contain -subject- tags that will be replace by
    the subject string"""
    s = substitute(s, sub_list)
    s = substitute(s, [("-subject-", subject)])
    return s

def magic_sub(s, user_name=None, bot_name="Alan"):
    """take a string, the user_name and the bot_name
    return the string with person and subject substitued
    """
    s = do_person_sub(s)
    print(s)
    if user_name:
        s = do_subject_sub(s, subject_you, user_name)
    if bot_name:
        s = do_subject_sub(s, subject_i, bot_name)
    return s
