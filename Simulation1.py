from scvi.harmonization.utils_chenling import CompareModels
use_cuda = True
import numpy as np
from scipy.sparse import csr_matrix
from scvi.dataset.dataset import GeneExpressionDataset

import sys
models = str(sys.argv[1])
plotname = 'Sim1'

count1 = np.load('../sim_data/count1.npy')
count2 = np.load('../sim_data/count2.npy')
label1 = np.load('../sim_data/label1.npy')
label2 = np.load('../sim_data/label2.npy')

dataset1 = GeneExpressionDataset(
            *GeneExpressionDataset.get_attributes_from_matrix(
                csr_matrix(count1), labels=label1),
            gene_names=['gene'+str(i) for i in range(2000)], cell_types=['type'+str(i+1) for i in range(5)])

dataset2 = GeneExpressionDataset(
            *GeneExpressionDataset.get_attributes_from_matrix(
                csr_matrix(count2), labels=label2),
            gene_names=['gene'+str(i) for i in range(2000)], cell_types=['type'+str(i+1) for i in range(5)])

gene_dataset = GeneExpressionDataset.concat_datasets(dataset1,dataset2)

import pandas as pd
genes1 = pd.read_table('../Seurat_data/'+plotname+'.1.hvg_info.csv',delimiter=',')
geneid1 =np.asarray([x.replace('gene_','') for x in genes1[genes1.keys()[0]]]).astype('int')
genenames1 = genes1['genename']
genes2 = pd.read_table('../Seurat_data/'+plotname+'.2.hvg_info.csv',delimiter=',')
geneid2 =np.asarray([x.replace('gene_','') for x in genes2[genes2.keys()[0]]]).astype('int')
genenames2 = genes2['genename']
assert np.sum(np.asarray(genenames1)==gene_dataset.gene_names)==len(gene_dataset.gene_names)
assert np.sum(np.asarray(genenames2)==gene_dataset.gene_names)==len(gene_dataset.gene_names)
geneid = np.union1d(geneid1[:ngenes],geneid2[:ngenes])-1
gene_dataset.X = gene_dataset.X[:,geneid]
gene_dataset.update_genes(geneid)
dataset1.X = dataset1.X[:,geneid]
dataset1.update_genes(geneid)
dataset2.X = dataset2.X[:,geneid]
dataset2.update_genes(geneid)

CompareModels(gene_dataset, dataset1, dataset2, plotname, models)
