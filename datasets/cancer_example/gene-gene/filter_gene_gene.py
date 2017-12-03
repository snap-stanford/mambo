import os
input_dir = '/dfs/scratch2/MINER-BIO/data-genemania/genemania.org/data/current/Homo_sapiens'
output_dir = 'genemania_data'

types = ["Co-expression", "Co-localization", "Genetic_interactions", "Pathway", "Physical_interactions", "Predicted"]

gene_filename = "../gene/icgc_parsed.tsv"
genes = set()
with open(gene_filename, "r") as gf:
    for line in gf:
        genes.add(line.split('\t')[0].strip())
print genes


for filename in os.listdir(input_dir):
    if any(typename in filename for typename in types):
        filepath = os.path.join(input_dir, filename)
        output_string = ""
        with open(filepath, 'r') as f:
            output_string = '# ' + f.readline()
            for line in f:
                gene1 = line.split('\t')[0]
                gene2 = line.split('\t')[0]
                if gene1 in genes and gene2 in genes:
                    print line
                    output_string += line
            
        output_filename = os.path.join(output_dir, filename)
        with open(output_filename, "w") as of:
            of.write(output_string)