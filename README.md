# HBO Kennisbank Titelgenerator
## Over het project

Binnen dit project is een NLP pipeline ontwikkeld voor automatische titelgeneratie op basis van publicaties uit de HBO Kennisbank.

De pipeline bestaat uit:

- webscraping
- data cleaning
- fine-tuning van een FLAN-T5 model
- evaluatie met ROUGE
- vergelijking van samplingstrategieën
- RLAIF evaluatie via AI feedback

---

## Dataset

De data is gescrapet van:

HBO Kennisbank

Belangrijke velden:

- title
- abstract
- metadata

---

## Gebruikte technieken

### Prompt Engineering
- Role Prompting
- Iterative Prompting
- Instruction Prompting

### Fine-tuning
- FLAN-T5-small
- Seq2Seq training

### Evaluatie
- ROUGE
- AI feedback (RLAIF)

---

## Installatie
`pip install -r requirements.txt`

---

## Uitvoeren

### Data scrapen
`python portfolio_m.ipynb`

### Notebook openen
`jupyter notebook`

---

## Resultaten

Beam search genereerde gemiddeld de meest consistente academische titels volgens zowel ROUGE als AI evaluatie.