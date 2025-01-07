import fire
from rich import print
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

# model_name = "Jean-Baptiste/camembert-ner"
model_name = "Babelscape/wikineural-multilingual-ner"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name)
nlp = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple", stride=0)

# https://www.gutenberg.org/cache/epub/17989/pg17989.txt

def text() -> str:
    return """Marseille.--L'arrivée.


Le 24 février 1815, la vigie de Notre-Dame de la Garde signala le
trois-mâts le _Pharaon_, venant de Smyrne, Trieste et Naples.

Comme d'habitude, un pilote côtier partit aussitôt du port, rasa le
château d'If, et alla aborder le navire entre le cap de Morgion et l'île
de Rion.

Aussitôt, comme d'habitude encore, la plate-forme du fort Saint-Jean
s'était couverte de curieux; car c'est toujours une grande affaire à
Marseille que l'arrivée d'un bâtiment, surtout quand ce bâtiment, comme
le _Pharaon_, a été construit, gréé, arrimé sur les chantiers de la
vieille Phocée, et appartient à un armateur de la ville.

Cependant ce bâtiment s'avançait; il avait heureusement franchi le
détroit que quelque secousse volcanique a creusé entre l'île de
Calasareigne et l'île de Jaros; il avait doublé Pomègue, et il
s'avançait sous ses trois huniers, son grand foc et sa brigantine, mais
si lentement et d'une allure si triste, que les curieux, avec cet
instinct qui pressent un malheur, se demandaient quel accident pouvait
être arrivé à bord. Néanmoins les experts en navigation reconnaissaient
que si un accident était arrivé, ce ne pouvait être au bâtiment
lui-même; car il s'avançait dans toutes les conditions d'un navire
parfaitement gouverné: son ancre était en mouillage, ses haubans de
beaupré décrochés; et près du pilote, qui s'apprêtait à diriger le
_Pharaon_ par l'étroite entrée du port de Marseille, était un jeune
homme au geste rapide et à l'oeil actif, qui surveillait chaque
mouvement du navire et répétait chaque ordre du pilote.

La vague inquiétude qui planait sur la foule avait particulièrement
atteint un des spectateurs de l'esplanade de Saint-Jean, de sorte qu'il
ne put attendre l'entrée du bâtiment dans le port; il sauta dans une
petite barque et ordonna de ramer au-devant du _Pharaon_, qu'il
atteignit en face de l'anse de la Réserve.

En voyant venir cet homme, le jeune marin quitta son poste à côté du
pilote, et vint, le chapeau à la main, s'appuyer à la muraille du
bâtiment.

C'était un jeune homme de dix-huit à vingt ans, grand, svelte, avec de
beaux yeux noirs et des cheveux d'ébène; il y avait dans toute sa
personne cet air calme et de résolution particulier aux hommes habitués
depuis leur enfance à lutter avec le danger.

«Ah! c'est vous, Dantès! cria l'homme à la barque; qu'est-il donc
arrivé, et pourquoi cet air de tristesse répandu sur tout votre bord?

--Un grand malheur, monsieur Morrel! répondit le jeune homme, un grand
malheur, pour moi surtout: à la hauteur de Civita-Vecchia, nous avons
perdu ce brave capitaine Leclère.

--Et le chargement? demanda vivement l'armateur.

--Il est arrivé à bon port, monsieur Morrel, et je crois que vous serez
content sous ce rapport; mais ce pauvre capitaine Leclère....

--Que lui est-il donc arrivé? demanda l'armateur d'un air visiblement
soulagé; que lui est-il donc arrivé, à ce brave capitaine?

--Il est mort.

--Tombé à la mer?

--Non, monsieur; mort d'une fièvre cérébrale, au milieu d'horribles
souffrances.»

Puis, se retournant vers ses hommes:

«Holà hé! dit-il, chacun à son poste pour le mouillage!»

L'équipage obéit. Au même instant, les huit ou dix matelots qui le
composaient s'élancèrent les uns sur les écoutes, les autres sur les
bras, les autres aux drisses, les autres aux hallebas des focs, enfin
les autres aux cargues des voiles.

Le jeune marin jeta un coup d'oeil nonchalant sur ce commencement de
manoeuvre, et, voyant que ses ordres allaient s'exécuter, il revint à
son interlocuteur.

«Et comment ce malheur est-il donc arrivé? continua l'armateur,
reprenant la conversation où le jeune marin l'avait quittée.

--Mon Dieu, monsieur, de la façon la plus imprévue: après une longue
conversation avec le commandant du port, le capitaine Leclère quitta
Naples fort agité; au bout de vingt-quatre heures, la fièvre le prit;
trois jours après, il était mort....

«Nous lui avons fait les funérailles ordinaires, et il repose, décemment
enveloppé dans un hamac, avec un boulet de trente-six aux pieds et un à
la tête, à la hauteur de l'île d'El Giglio. Nous rapportons à sa veuve
sa croix d'honneur et son épée. C'était bien la peine, continua le jeune
homme avec un sourire mélancolique, de faire dix ans la guerre aux
Anglais pour en arriver à mourir, comme tout le monde, dans son lit.

--Dame! que voulez-vous, monsieur Edmond, reprit l'armateur qui
paraissait se consoler de plus en plus, nous sommes tous mortels, et il
faut bien que les anciens fassent place aux nouveaux, sans cela il n'y
aurait pas d'avancement; et du moment que vous m'assurez que la
cargaison....

--Est en bon état, monsieur Morrel, je vous en réponds. Voici un voyage
que je vous donne le conseil de ne point escompter pour 25.000 francs de
bénéfice.»

Puis, comme on venait de dépasser la tour ronde:

«Range à carguer les voiles de hune, le foc et la brigantine! cria le
jeune marin; faites penaud!»

L'ordre s'exécuta avec presque autant de promptitude que sur un bâtiment
de guerre.

«Amène et cargue partout!»

Au dernier commandement, toutes les voiles s'abaissèrent, et le navire
s'avança d'une façon presque insensible, ne marchant plus que par
l'impulsion donnée.

«Et maintenant, si vous voulez monter, monsieur Morrel, dit Dantès
voyant l'impatience de l'armateur, voici votre comptable, M. Danglars,
qui sort de sa cabine, et qui vous donnera tous les renseignements que
vous pouvez désirer. Quant à moi, il faut que je veille au mouillage et
que je mette le navire en deuil.»

L'armateur ne se le fit pas dire deux fois. Il saisit un câble que lui
jeta Dantès, et, avec une dextérité qui eût fait honneur à un homme de
mer, il gravit les échelons cloués sur le flanc rebondi du bâtiment,
tandis que celui-ci, retournant à son poste de second, cédait la
conversation à celui qu'il avait annoncé sous le nom de Danglars, et
qui, sortant de sa cabine, s'avançait effectivement au-devant de
l'armateur.

Le nouveau venu était un homme de vingt-cinq à vingt-six ans, d'une
figure assez sombre, obséquieux envers ses supérieurs, insolent envers
ses subordonnés: aussi, outre son titre d'agent comptable, qui est
toujours un motif de répulsion pour les matelots, était-il généralement
aussi mal vu de l'équipage qu'Edmond Dantès au contraire en était aimé.

«Eh bien, monsieur Morrel, dit Danglars, vous savez le malheur, n'est-ce
pas?

--Oui, oui, pauvre capitaine Leclère! c'était un brave et honnête homme!

--Et un excellent marin surtout, vieilli entre le ciel et l'eau, comme
il convient à un homme chargé des intérêts d'une maison aussi importante
que maison Morrel et fils, répondit Danglars.

--Mais, dit l'armateur, suivant des yeux Dantès qui cherchait son
mouillage, mais il me semble qu'il n'y a pas besoin d'être si vieux
marin que vous le dites, Danglars, pour connaître son métier, et voici
notre ami Edmond qui fait le sien, ce me semble, en homme qui n'a besoin
de demander des conseils à personne.

--Oui, dit Danglars en jetant sur Dantès un regard oblique où brilla un
éclair de haine, oui, c'est jeune, et cela ne doute de rien. À peine le
capitaine a-t-il été mort qu'il a pris le commandement sans consulter
personne, et qu'il nous a fait perdre un jour et demi à l'île d'Elbe au
lieu de revenir directement à Marseille.

--Quant à prendre le commandement du navire, dit l'armateur, c'était son
devoir comme second; quant à perdre un jour et demi à l'île d'Elbe, il a
eu tort; à moins que le navire n'ait eu quelque avarie à réparer.

--Le navire se portait comme je me porte, et comme je désire que vous
vous portiez, monsieur Morrel; et cette journée et demie a été perdue
par pur caprice, pour le plaisir d'aller à terre, voilà tout.

--Dantès, dit l'armateur se retournant vers le jeune homme, venez donc
ici.

--Pardon, monsieur, dit Dantès, je suis à vous dans un instant.»

Puis s'adressant à l'équipage: «Mouille!» dit-il.

Aussitôt l'ancre tomba, et la chaîne fila avec bruit. Dantès resta à son
poste, malgré la présence du pilote, jusqu'à ce que cette dernière
manoeuvre fût terminée; puis alors:

«Abaissez la flamme à mi-mât, mettez le pavillon en berne, croisez les
vergues!

--Vous voyez, dit Danglars, il se croit déjà capitaine, sur ma parole.

--Et il l'est de fait, dit l'armateur.

--Oui, sauf votre signature et celle de votre associé, monsieur Morrel.

--Dame! pourquoi ne le laisserions-nous pas à ce poste? dit l'armateur.
Il est jeune, je le sais bien, mais il me paraît tout à la chose, et
fort expérimenté dans son état.»

Un nuage passa sur le front de Danglars.

«Pardon, monsieur Morrel, dit Dantès en s'approchant; maintenant que le
navire est mouillé, me voilà tout à vous: vous m'avez appelé, je crois?»

Danglars fit un pas en arrière.

«Je voulais vous demander pourquoi vous vous étiez arrêté à l'île
d'Elbe?

--Je l'ignore, monsieur; c'était pour accomplir un dernier ordre du
capitaine Leclère, qui, en mourant, m'avait remis un paquet pour le
grand maréchal Bertrand.

--L'avez-vous donc vu, Edmond?

--Qui?

--Le grand maréchal?

--Oui.»

Morrel regarda autour de lui, et tira Dantès à part.

«Et comment va l'Empereur? demanda-t-il vivement.

--Bien, autant que j'aie pu en juger par mes yeux.

--Vous avez donc vu l'Empereur aussi?

--Il est entré chez le maréchal pendant que j'y étais.

--Et vous lui avez parlé?

--C'est-à-dire que c'est lui qui m'a parlé, monsieur, dit Dantès en
souriant.

--Et que vous a-t-il dit?

--Il m'a fait des questions sur le bâtiment, sur l'époque de son départ
pour Marseille, sur la route qu'il avait suivie et sur la cargaison
qu'il portait. Je crois que s'il eût été vide, et que j'en eusse été le
maître, son intention eût été de l'acheter; mais je lui ai dit que je
n'étais que simple second, et que le bâtiment appartenait à la maison
Morrel et fils. «Ah! ah! a-t-il dit, je la connais. Les Morrel sont
armateurs de père en fils, et il y avait un Morrel qui servait dans le
même régiment que moi lorsque j'étais en garnison à Valence.»

--C'est pardieu vrai! s'écria l'armateur tout joyeux; c'était Policar
Morrel, mon oncle, qui est devenu capitaine. Dantès, vous direz à mon
oncle que l'Empereur s'est souvenu de lui, et vous le verrez pleurer, le
vieux grognard. Allons, allons, continua l'armateur en frappant
amicalement sur l'épaule du jeune homme, vous avez bien fait, Dantès, de
suivre les instructions du capitaine Leclère et de vous arrêter à l'île
d'Elbe, quoique, si l'on savait que vous avez remis un paquet au
maréchal et causé avec l'Empereur, cela pourrait vous compromettre.

--En quoi voulez-vous, monsieur, que cela me compromette? dit Dantès: je
ne sais pas même ce que je portais, et l'Empereur ne m'a fait que les
questions qu'il eût faites au premier venu. Mais, pardon, reprit Dantès,
voici la santé et la douane qui nous arrivent; vous permettez, n'est-ce
pas?

--Faites, faites, mon cher Dantès.»

Le jeune homme s'éloigna, et, comme il s'éloignait, Danglars se
rapprocha.

«Eh bien, demanda-t-il, il paraît qu'il vous a donné de bonnes raisons
de son mouillage à Porto-Ferrajo?

--D'excellentes, mon cher monsieur Danglars.

--Ah! tant mieux, répondit celui-ci, car c'est toujours pénible de voir
un camarade qui ne fait pas son devoir.

--Dantès a fait le sien, répondit l'armateur, et il n'y a rien à dire.
C'était le capitaine Leclère qui lui avait ordonné cette relâche.

--À propos du capitaine Leclère, ne vous a-t-il pas remis une lettre de
lui?

--Qui?

--Dantès.

--À moi, non! En avait-il donc une?

--Je croyais qu'outre le paquet, le capitaine Leclère lui avait confié
une lettre.

--De quel paquet voulez-vous parler, Danglars?

--Mais de celui que Dantès a déposé en passant à Porto-Ferrajo?

--Comment savez-vous qu'il avait un paquet à déposer à Porto-Ferrajo?»

Danglars rougit.

«Je passais devant la porte du capitaine qui était entrouverte, et je
lui ai vu remettre ce paquet et cette lettre à Dantès.

--Il ne m'en a point parlé, dit l'armateur; mais s'il a cette lettre, il
me la remettra.»

Danglars réfléchit un instant.

«Alors, monsieur Morrel, je vous prie, dit-il, ne parlez point de cela à
Dantès; je me serai trompé.»

En ce moment, le jeune homme revenait; Danglars s'éloigna.

«Eh bien, mon cher Dantès, êtes-vous libre? demanda l'armateur.

--Oui, monsieur.

--La chose n'a pas été longue.

--Non, j'ai donné aux douaniers la liste de marchandises; et quant à la
consigne, elle avait envoyé avec le pilote côtier un homme à qui j'ai
remis nos papiers.

--Alors, vous n'avez plus rien à faire ici?»

Dantès jeta un regard rapide autour de lui.

«Non, tout est en ordre, dit-il.

--Vous pouvez donc alors venir dîner avec nous?

--Excusez-moi, monsieur Morrel, excusez-moi, je vous prie, mais je dois
ma première visite à mon père. Je n'en suis pas moins reconnaissant de
l'honneur que vous me faites.

--C'est juste, Dantès, c'est juste. Je sais que vous êtes bon fils.

--Et... demanda Dantès avec une certaine hésitation, et il se porte
bien, que vous sachiez, mon père?

--Mais je crois que oui, mon cher Edmond, quoique je ne l'aie pas
aperçu.

--Oui, il se tient enfermé dans sa petite chambre.

--Cela prouve au moins qu'il n'a manqué de rien pendant votre absence.»

Dantès sourit.

«Mon père est fier, monsieur, et, eût-il manqué de tout, je doute qu'il
eût demandé quelque chose à qui que ce soit au monde, excepté à Dieu.

--Eh bien, après cette première visite, nous comptons sur vous.

--Excusez-moi encore, monsieur Morrel, mais après cette première visite,
j'en ai une seconde qui ne me tient pas moins au coeur.

--Ah! c'est vrai, Dantès; j'oubliais qu'il y a aux Catalans quelqu'un
qui doit vous attendre avec non moins d'impatience que votre père: c'est
la belle Mercédès.»

Dantès sourit.

«Ah! ah! dit l'armateur, cela ne m'étonne plus, qu'elle soit venue trois
fois me demander des nouvelles du _Pharaon_. Peste! Edmond, vous n'êtes
point à plaindre, et vous avez là une jolie maîtresse!

--Ce n'est point ma maîtresse, monsieur, dit gravement le jeune marin:
c'est ma fiancée.

--C'est quelquefois tout un, dit l'armateur en riant.

--Pas pour nous, monsieur, répondit Dantès.

--Allons, allons, mon cher Edmond, continua l'armateur, que je ne vous
retienne pas; vous avez assez bien fait mes affaires pour que je vous
donne tout loisir de faire les vôtres. Avez-vous besoin d'argent?

--Non, monsieur; j'ai tous mes appointements du voyage, c'est-à-dire
près de trois mois de solde.

--Vous êtes un garçon rangé, Edmond.

--Ajoutez que j'ai un père pauvre, monsieur Morrel.

--Oui, oui, je sais que vous êtes un bon fils. Allez donc voir votre
père: j'ai un fils aussi, et j'en voudrais fort à celui qui, après un
voyage de trois mois, le retiendrait loin de moi.

--Alors, vous permettez? dit le jeune homme en saluant.

--Oui, si vous n'avez rien de plus à me dire.

--Non.

--Le capitaine Leclère ne vous a pas, en mourant, donné une lettre pour
moi?

--Il lui eût été impossible d'écrire, monsieur; mais cela me rappelle
que j'aurai un congé de quinze jours à vous demander.

--Pour vous marier?

--D'abord; puis pour aller à Paris.

--Bon, bon! vous prendrez le temps que vous voudrez, Dantès; le temps de
décharger le bâtiment nous prendra bien six semaines, et nous ne nous
remettrons guère en mer avant trois mois.... Seulement, dans trois mois,
il faudra que vous soyez là. Le _Pharaon_, continua l'armateur en
frappant sur l'épaule du jeune marin, ne pourrait pas repartir sans son
capitaine.

--Sans son capitaine! s'écria Dantès les yeux brillants de joie; faites
bien attention à ce que vous dites là, monsieur, car vous venez de
répondre aux plus secrètes espérances de mon coeur. Votre intention
serait-elle de me nommer capitaine du _Pharaon_?

--Si j'étais seul, je vous tendrais la main, mon cher Dantès, et je vous
dirais: «C'est fait.» Mais j'ai un associé, et vous savez le proverbe
italien: _Che a compagne a padrone_. Mais la moitié de la besogne est
faite au moins, puisque sur deux voix vous en avez déjà une.
Rapportez-vous-en à moi pour avoir l'autre, et je ferai de mon mieux.

--Oh! monsieur Morrel, s'écria le jeune marin, saisissant, les larmes
aux yeux, les mains de l'armateur; monsieur Morrel, je vous remercie, au
nom de mon père et de Mercédès.

--C'est bien, c'est bien, Edmond, il y a un Dieu au ciel pour les braves
gens, que diable! Allez voir votre père, allez voir Mercédès, et revenez
me trouver après.

--Mais vous ne voulez pas que je vous ramène à terre?

--Non, merci; je reste à régler mes comptes avec Danglars. Avez-vous été
content de lui pendant le voyage?

--C'est selon le sens que vous attachez à cette question, monsieur. Si
c'est comme bon camarade, non, car je crois qu'il ne m'aime pas depuis
le jour où j'ai eu la bêtise, à la suite d'une petite querelle que nous
avions eue ensemble, de lui proposer de nous arrêter dix minutes à l'île
de Monte-Cristo pour vider cette querelle; proposition que j'avais eu
tort de lui faire, et qu'il avait eu, lui, raison de refuser. Si c'est
comme comptable que vous me faites cette question je crois qu'il n'y a
rien à dire et que vous serez content de la façon dont sa besogne est
faite.

--Mais, demanda l'armateur, voyons, Dantès, si vous étiez capitaine du
_Pharaon_, garderiez-vous Danglars avec plaisir?

--Capitaine ou second, monsieur Morrel, répondit dit Dantès, j'aurai
toujours les plus grands égards pour ceux qui posséderont la confiance
de mes armateurs.

--Allons, allons, Dantès, je vois qu'en tout point vous êtes un brave
garçon. Que je ne vous retienne plus: allez, car je vois que vous êtes
sur des charbons.

--J'ai donc mon congé? demanda Dantès.

--Allez, vous dis-je.

--Vous permettez que je prenne votre canot?

--Prenez.

--Au revoir, monsieur Morrel, et mille fois merci.

--Au revoir, mon cher Edmond, bonne chance!»

Le jeune marin sauta dans le canot, alla s'asseoir à la poupe, et donna
l'ordre d'aborder à la Canebière. Deux matelots se penchèrent aussitôt
sur leurs rames, et l'embarcation glissa aussi rapidement qu'il est
possible de le faire, au milieu des mille barques qui obstruent l'espèce
de rue étroite qui conduit, entre deux rangées de navires, de l'entrée
du port au quai d'Orléans.

L'armateur le suivit des yeux en souriant, jusqu'au bord, le vit sauter
sur les dalles du quai, et se perdre aussitôt au milieu de la foule
bariolée qui, de cinq heures du matin à neuf heures du soir, encombre
cette fameuse rue de la Canebière, dont les Phocéens modernes sont si
fiers, qu'ils disent avec le plus grand sérieux du monde et avec cet
accent qui donne tant de caractère à ce qu'ils disent: «Si Paris avait
la Canebière, Paris serait un petit Marseille.»

En se retournant, l'armateur vit derrière lui Danglars, qui, en
apparence, semblait attendre ses ordres, mais qui, en réalité, suivait
comme lui le jeune marin du regard.

Seulement, il y avait une grande différence dans l'expression de ce
double regard qui suivait le même homme."""

class PIIRemoval:
    def run(self):
        print("NER example!")
        encoded = tokenizer(text())
        print('|'.join(encoded.tokens()))
        print(len(text()))
        print(nlp(text()))

if __name__ == '__main__':
    fire.Fire(PIIRemoval)

