from Bio import PDB
parser = PDB.PDBParser()
structure = parser.get_structure('2FH7', '2FH7.pdb')
ppb = PDB.PPBuilder()

for pp in ppb.build_peptides(structure):
    print(pp.get_sequence())

model = structure[0]
for pp in ppb.build_peptides(model):
    print(pp.get_sequence())