# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import brocclib.command
import pandas as pd
from qiime2.plugin import (
    Plugin, Citations, Int, Str, Float, Range
)
from q2_types.feature_data import (
    FeatureData, Taxonomy, Sequence, DNAFASTAFormat,
)
import q2_brocc
import os.path
import tempfile
import subprocess


citations = Citations.load('citations.bib', package='q2_brocc')
plugin = Plugin(
    name='brocc',
    version=q2_brocc.__version__,
    website='https://github.com/kylebittinger/q2-brocc',
    package='q2_brocc',
    description=('This QIIME 2 plugin supports taxonomic '
                 'classification of features using the BROCC '
                 'software.'),
    short_description='Plugin for taxonomic classification with BROCC.',
    citations=[citations['Dollive2012']]
)


def classify_brocc(
        query: DNAFASTAFormat,
        evalue: float=0.00001,
        maxaccepts: int=100,
        blastdb: str="nt",
        min_species_id: float=95.2,
        min_genus_id: float=83.05,
        min_id: float=80.0,
        ) -> pd.DataFrame:
    # Temp output directory for BROCC
    brocc_output_dir = tempfile.mkdtemp()
    # First order of business: generate BLAST output file
    with tempfile.NamedTemporaryFile() as blast_outfile:
        blast_cmd = [
            'blastn',
            '-query', str(query),
            '-evalue', str(evalue),
            '-outfmt', '7',
            '-db', blastdb,
            '-max_target_seqs', str(maxaccepts),
            '-out', blast_outfile.name,
        ]
        subprocess.run(blast_cmd, check=True)

        # Run BROCC using BLAST output file
        brocclib.command.main([
            "-i", str(query),
            "-b", blast_outfile.name,
            "-o", brocc_output_dir,
            "--min_species_id", str(min_species_id),
            "--min_genus_id", str(min_genus_id),
            "--min_id", str(min_id),
        ])
        brocc_taxonomy_fp = os.path.join(
            brocc_output_dir, "Standard_Taxonomy.txt")
        with open(brocc_taxonomy_fp) as brocc_outfile:
            results = import_brocc_taxonomy(brocc_outfile)
        return results


def import_brocc_taxonomy(f):
    dict_results = dict(
        (feat_id, (assign, 1.0))
        for feat_id, assign in read_brocc_taxonomy(f))
    result = pd.DataFrame.from_dict(dict_results, 'index')
    result.index.name = 'Feature ID'
    result.columns = ['Taxon', 'Confidence']
    return result


def read_brocc_taxonomy(f):
    for line in f:
        line = line.rstrip()
        if line:
            feature_id, assignment_str = line.split("\t", maxsplit=1)
            yield feature_id, assignment_str


plugin.methods.register_function(
    function=classify_brocc,
    inputs={'query': FeatureData[Sequence]},
    parameters={
        'evalue': Float,
        'maxaccepts': Int % Range(1, None),
        'blastdb': Str,
        'min_species_id': Float % Range(0.0, 100.0),
        'min_genus_id': Float % Range(0.0, 100.0),
        'min_id': Float % Range(0.0, 100.0),
    },
    outputs=[('classification', FeatureData[Taxonomy])],
    input_descriptions={'query': 'Sequences to classify taxonomically.'},
    parameter_descriptions={
        'evalue': 'BLAST expectation value (E) threshold for saving hits.',
        'maxaccepts': ('Maximum number of hits to keep for each query. Must '
                       'be in range [0, infinity].'),
        'blastdb': 'BLAST database to use for alignment.',
        'min_species_id': (
            'Minimum percent identity for species-level consensus. '
            'Suggested values are: 95.2 for ITS sequencing, '
            '99.0 for 18S sequencing, 97.0 for 16S sequencing, and '
            'something just below 95.0 for metagenomic sequencing '
            '(average nucleotide identity between genomes within a '
            'species is close to 95%).'),
        'min_genus_id': (
            'Minimum percent identity for genus-level consensus. '
            'Suggested values are: 83.0 for ITS sequencing, '
            '96.0 for 18S sequencing, 90-ish for 16S sequencing, and '
            'probably the same as min_id for metagenomic sequencing.'),
        'min_id': (
            'Minimum percent identity for reference sequences at any '
            'taxonomic rank.  Something around 80 is generally a good '
            'value here.'),
    },
    output_descriptions={
        'classification': 'Taxonomy classifications of query sequences.'},
    name='BROCC consensus taxonomy classifier',
    description=('Assign taxonomy to query sequences using BROCC. Performs '
                 'BLAST+ local alignment of query reads to the nt database '
                 ' from NCBI, then evaluates the results to form consensus '
                 ' taxonomic assignments.'),
)
