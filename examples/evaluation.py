import pandas as pd
from datasets import load_dataset, Dataset, Features, Sequence, Value, ClassLabel
from evaluate import evaluator
import typing as t

LABEL_MAPPING = {
    'O': 0,
    'B-PER': 1,
    'I-PER': 2,
    'B-ORG': 3,
    'I-ORG': 4,
    'B-LOC': 5,
    'I-LOC': 6,
    'B-MISC': 7,
    'I-MISC': 8
}

def evaluate(data: Dataset, models: t.List[str]) -> pd.DataFrame:
    task_evaluator = evaluator("token-classification")
    results = []
    for model in models:
        results.append(
            task_evaluator.compute(
                model_or_pipeline=model,
                data=data,
                metric="seqeval"
                )
            )

    return pd.DataFrame(results, index=models)


def format_features(data: Dataset, labels: t.Dict[str, int]) -> Dataset:
    data_dict = {
        "tokens": [],
        "ner_tags": [],
    }
    for entry in data:
        data_dict["tokens"].append(entry["tokens"])
        data_dict["ner_tags"].append(entry["ner_tags"])
    
    features = Features({
            "tokens": Sequence(feature=Value(dtype="string")),
            "ner_tags": Sequence(feature=ClassLabel(names=list(labels.keys()))),
            })
    return Dataset.from_dict(
        data_dict, features=features
    )


def format_results(results: pd.DataFrame, models: t.List[str]) -> pd.DataFrame:
    data = {
        "model": [],
        "precision": [],
        "recall": [],
        "f1": [],
        "number": [],
    }

    for model in models:
        res = results.loc[model]
        data["model"].append(model)
        data["precision"].append(res["precision"])
        data["recall"].append(res["recall"])
        data["f1"].append(res["f1"])
        data["number"].append(res["number"])
    
    return pd.DataFrame(data)


def format_ai4privacy(dataset: Dataset) -> Dataset:
    mapping_token_label = {
        'O': 'O',
        'I-USERNAME': 'I-PER',
        'I-TIME': 'I-MISC',
        'I-DATE': 'I-MISC',
        'I-LASTNAME1': 'I-PER',
        'I-LASTNAME2': 'I-PER',
        'I-EMAIL': 'I-MISC',
        'I-SOCIALNUMBER': 'I-MISC',
        'I-IDCARD': 'I-MISC',
        'I-COUNTRY': 'I-LOC',
        'I-BUILDING': 'I-MISC',
        'I-STREET': 'I-MISC',
        'I-CITY': 'I-LOC',
        'I-STATE': 'I-LOC',
        'I-POSTCODE': 'I-MISC',
        'I-PASS': 'I-MISC',
        'I-PASSPORT': 'I-MISC',
        'I-TEL': 'I-MISC',
        'I-DRIVERLICENSE': 'I-MISC',
        'I-BOD': 'I-MISC',
        'I-SEX': 'I-MISC',
        'I-IP': 'I-MISC',
        'I-SECADDRESS': 'I-MISC',
        'I-LASTNAME3': 'I-PER',
        'I-GIVENNAME1': 'I-PER',
        'I-GIVENNAME2': 'I-PER',
        'I-TITLE': 'I-MISC',
        'I-GEOCOORD': 'I-MISC',
        'I-CARDISSUER': 'I-MISC',
        'B-USERNAME': 'B-PER',
        'B-TIME': 'B-MISC',
        'B-DATE': 'B-MISC',
        'B-LASTNAME1': 'B-PER',
        'B-LASTNAME2': 'B-PER',
        'B-EMAIL': 'B-MISC',
        'B-SOCIALNUMBER': 'B-MISC',
        'B-IDCARD': 'B-MISC',
        'B-COUNTRY': 'B-LOC',
        'B-BUILDING': 'B-MISC',
        'B-STREET': 'B-MISC',
        'B-CITY': 'B-LOC',
        'B-STATE': 'B-LOC',
        'B-POSTCODE': 'B-MISC',
        'B-PASS': 'B-MISC',
        'B-PASSPORT': 'B-MISC',
        'B-TEL': 'B-MISC',
        'B-DRIVERLICENSE': 'B-MISC',
        'B-BOD': 'B-MISC',
        'B-SEX': 'B-MISC',
        'B-IP': 'B-MISC',
        'B-SECADDRESS': 'B-MISC',
        'B-LASTNAME3': 'B-PER',
        'B-GIVENNAME1': 'B-PER',
        'B-GIVENNAME2': 'B-PER',
        'B-TITLE': 'B-MISC',
        'B-GEOCOORD': 'B-MISC',
        'B-CARDISSUER': 'B-MISC',
    }
    data={
    "tokens": [],
    "ner_tags": [],
    }
    # limit the length of tokes (the evaluator fails otherwise)
    limit = 200
    for i, entry in enumerate(dataset):
        a = entry["mbert_text_tokens"][:limit]
        b = [LABEL_MAPPING[mapping_token_label[l]] for l in  entry["mbert_bio_labels"]][:limit]
        assert len(a)==len(b)
        data["tokens"].append(a)
        data["ner_tags"].append(b)

    return Dataset.from_dict(
        mapping=data,
        features=Features({
            "tokens": Sequence(feature=Value(dtype="string")),
            "ner_tags": Sequence(feature=ClassLabel(names=list(LABEL_MAPPING.keys()))),
            }),
    )


def main():
    size = 100

    conll2003 = load_dataset("conll2003", split="validation").shuffle().select(range(size))
    wikineural = load_dataset("Babelscape/wikineural")

    
    wn_de = format_features(wikineural['test_de'].shuffle().select(range(size)), LABEL_MAPPING)
    wn_en = format_features(wikineural['test_en'].shuffle().select(range(size)), LABEL_MAPPING)
    wn_es = format_features(wikineural['test_es'].shuffle().select(range(size)), LABEL_MAPPING)
    wn_fr = format_features(wikineural['test_fr'].shuffle().select(range(size)), LABEL_MAPPING)
    wn_it = format_features(wikineural['test_it'].shuffle().select(range(size)), LABEL_MAPPING)

    ai4privacy = load_dataset("ai4privacy/pii-masking-300k", split='validation').shuffle().select(range(1000))
    ready_ai4privacy = format_ai4privacy(ai4privacy)
    models = [
        "dslim/bert-base-NER",
        "xlm-roberta-large-finetuned-conll03-english",
        "Babelscape/wikineural-multilingual-ner",
        "Jean-Baptiste/camembert-ner"
    ]

    datasets = {
        'conll2003': conll2003,
        'ai4privacy': ready_ai4privacy,
        'wn_de': wn_de,
        'wn_en': wn_en,
        'wn_es': wn_es,
        'wn_fr': wn_fr,
        'wn_it': wn_it,
    }
    for ds_name, ds in datasets.items():
        df = evaluate(ds, models = models)
        res_df=format_results(df["PER"], models)
        print(ds_name)
        print(res_df)

if __name__ == "__main__":
    main()