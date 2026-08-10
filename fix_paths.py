import glob

for dosya in glob.glob("notebooks/*.ipynb"):
    with open(dosya, "r", encoding="utf-8") as f:
        icerik = f.read()
    icerik = icerik.replace('"data/', '"../data/')
    icerik = icerik.replace("'data/", "'../data/")
    icerik = icerik.replace('"outputs/', '"../outputs/')
    icerik = icerik.replace("'outputs/", "'../outputs/")
    with open(dosya, "w", encoding="utf-8") as f:
        f.write(icerik)
    print(f"{dosya} guncellendi.")