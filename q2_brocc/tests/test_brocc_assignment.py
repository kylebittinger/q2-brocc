# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from qiime2.plugin.testing import TestPluginBase

from q2_types.feature_data import DNAFASTAFormat
from q2_brocc.plugin_setup import classify_brocc


class BroccTests(TestPluginBase):
    package = 'q2_brocc.tests'

    def test_brocc_basic(self):
        reads_fp = self.get_data_path('query.fasta')
        reads = DNAFASTAFormat(reads_fp, mode='r')
        blastdb = self.get_data_path('somefungi.fasta')
        result = classify_brocc(
            reads, blastdb=str(blastdb),
            min_species_id=95.0, min_genus_id=85.0,
        )
        self.assertEqual(result.Taxon.to_dict(), expected_assignments)


expected_assignments = {
    'pichia1': (
        'Eukaryota;Fungi;Ascomycota;Saccharomycetes;Saccharomycetales;'
        'Phaffomycetaceae;Cyberlindnera;Cyberlindnera jadinii'),
    'trichosporon1': (
        'Eukaryota;Fungi;Basidiomycota;Tremellomycetes;Trichosporonales;'
        'Trichosporonaceae;Trichosporon;Trichosporon asahii'),
}
