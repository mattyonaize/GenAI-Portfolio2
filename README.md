# HBO Kennisbank Titelgenerator

## Over het project

Binnen dit project is een NLP-pipeline ontwikkeld voor automatische titelgeneratie op basis van publicaties uit de HBO Kennisbank.

De pipeline bestaat uit:

- webscraping
- data cleaning
- fine-tuning van een FLAN-T5 model
- evaluatie met ROUGE
- vergelijking van samplingstrategieën
- voorkeurgeneratie met AI feedback (RLAIF)
- Direct Preference Optimization (DPO)

---

## Dataset

De data is gescrapet van de **HBO Kennisbank**.

Belangrijke velden:

- title
- abstract
- metadata

De dataset is opgesplitst in een train-, validatie- en testset voor het trainen en evalueren van het model.

---

## Gebruikte technieken

### Prompt Engineering
- Role Prompting
- Iterative Prompting
- Instruction Prompting

### Fine-tuning
- FLAN-T5-small
- Seq2Seq Training (HuggingFace Transformers)

### Decodingstrategieën
- Greedy Decoding
- Beam Search
- Top-p Sampling

### Preference Learning
- AI Feedback (Llama 3.1)
- Direct Preference Optimization (DPO)

### Evaluatie
- ROUGE-1
- ROUGE-2
- ROUGE-L

---

## Installatie

```bash
pip install -r requirements.txt
```

---

## Uitvoeren

Open het notebook:

```bash
jupyter notebook
```

Voer vervolgens alle cellen uit om de volledige pipeline te doorlopen:

1. Data inladen
2. Fine-tuning
3. Evaluatie
4. Vergelijking van decodingstrategieën
5. Genereren van preference pairs
6. DPO-training
7. Eindevaluatie

---

## Resultaten

De verschillende decodingstrategieën zijn vergeleken met behulp van ROUGE-L. Hoewel **top-p sampling** de hoogste score behaalde, werd **beam search** gebruikt als stabiele referentiestrategie. Voor het genereren van preference pairs tijdens DPO zijn **beam search** en **top-p sampling** gecombineerd: beam search levert consistente titels, terwijl top-p voor voldoende variatie zorgt zodat de AI-evaluator een betekenisvolle voorkeur kan bepalen.

Na de supervised fine-tuning is het model verder geoptimaliseerd met **Direct Preference Optimization (DPO)** op basis van AI-gegenereerde voorkeuren.

---

## Gebruikte libraries

- Python
- PyTorch
- HuggingFace Transformers
- TRL
- Datasets
- Evaluate
- Pandas
- NumPy
- Matplotlib
- Groq API