import random
from pathlib import Path
import spacy
from spacy.training.example import Example
from tqdm import tqdm

OUTPUT_DIR = Path("csv_parser/output")

# На основе фраз из диалогов проводится тренировка модели
# Данная модель будет применяться для выявления ключевых слов в диалогах
TRAIN_DATA = [
    ("Алло здравствуйте",
     {"entities": [(5, 17, "GREETING")]}),

    ("Алло дмитрий добрый день",
     {"entities": [(13, 24, "GREETING")]}),

    ("Добрый меня максим зовут компания китобизнес удобно говорить",
     {"entities": [(0, 6, "GREETING")]}),

    ("Меня зовут ангелина компания диджитал бизнес",
     {"entities": [(11, 19, "NAME")]}),

    ("Добрый меня максим зовут компания китобизнес удобно говорить",
     {"entities": [(12, 18, "NAME")]}),

    ("Да это анастасия",
     {"entities": [(7, 16, "NAME")]}),

    ("Добрый меня максим зовут компания китобизнес удобно говорить",
     {"entities": [(34, 44, "COMPANY")]}),

    ("Меня зовут ангелина компания диджитал бизнес",
     {"entities": [(29, 44, "COMPANY")]}),

    ("Угу все хорошо да понедельника тогда всего доброго",
     {"entities": [(37, 50, "GOODBYE")]}),

    ("Всего хорошего до свидания",
     {"entities": [(15, 26, "GOODBYE")]}),
]

model = None
output_dir = OUTPUT_DIR
n_iter = 100

if model is not None:
    nlp = spacy.load(model)
    print("Loaded model '%s'" % model)
else:
    nlp = spacy.blank('ru')
    print("Created blank 'ru' model")

if 'ner' not in nlp.pipe_names:
    ner = nlp.add_pipe('ner', last=True)
else:
    ner = nlp.get_pipe('ner')

for _, annotations in TRAIN_DATA:
    for ent in annotations.get('entities'):
        ner.add_label(ent[2])

other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
with nlp.disable_pipes(*other_pipes):  # only train NER
    optimizer = nlp.begin_training()
    for itn in range(n_iter):
        random.shuffle(TRAIN_DATA)
        losses = {}
        for text, annotations in tqdm(TRAIN_DATA):
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update(
                [example],
                drop=0.5,
                sgd=optimizer,
                losses=losses)
        print(losses)

# тест модели
for text, _ in TRAIN_DATA:
    doc = nlp(text)
    print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
    print('Tokens', [(t.text, t.ent_type_, t.ent_iob) for t in doc])

# сохранение модели
if output_dir is not None:
    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir()
    nlp.to_disk(output_dir)
    print("Saved model to", output_dir)
