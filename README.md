# q2-brocc

[![Build Status](https://travis-ci.org/kylebittinger/q2-brocc.svg?branch=master)](https://travis-ci.org/kylebittinger/q2-brocc)

This is a QIIME 2 plugin to support the BROCC software for taxonomic
assignment. BROCC was originally built to generate taxonomic
assignments of marker gene sequences from fungi. However, we've found
BROCC to be useful with many other types of data.

The strategy applied by BROCC is to search against a large reference
database, the nt database from NCBI, using BLAST. Then, BROCC applies
a voting process to generate taxonomic assignments. The main factors
that differentiate BROCC from other software in this area are the
level of control in the voting, and the efforts to remove undesirable
or uninformative votes from the results.

More details about BROCC can be found in our publication (PMID
22759449) and on the github page for the software
(https://github.com/kylebittinger/brocc).

## Installing the plugin

QIIME 2 must be installed for the plugin to work. Instructions for
installing QIIME 2 can be found at https://qiime2.org. If you'd like
to use BROCC outside of QIIME 2, that's totally possible.  The
standalone software can be installed by running `pip install brocc`.

To install the BROCC plugin for QIIME 2, run

     pip install q2-brocc

Once installed, we should check that QIIME 2 can pick up on our new
plugin.  If you run

     qiime --help
	 
you should see `brocc` listed under the available commands.
Furthermore, if you run

     qiime brocc --help

you should see some help documentation for the plugin.

To run this plugin, you'll need to have the nt database from NCBI
downloaded and configured. It's about 60G and it takes a while to
download.  You can download over FTP using a command

     wget "ftp://ftp.ncbi.nlm.nih.gov/blast/db/nt.??.tar.gz" 
	 
NCBI has some tips on downloading large data sets at
https://www.ncbi.nlm.nih.gov/home/download/. Once the nt database is
downloaded, you'll need to make sure that BLAST can find the database
files. You do this by setting an environment variable, BLASTDB, to the
directory where the nt database files are stored.  Do this by running:

     export BLASTDB=/path/to/directory/containing/nt-database-files

While you're at it, copy/paste this line into your `~/.bashrc` file so
the environment variable is set the next time you log in.

Let's test that the nt database is configured correctly by BLASTing a
couple of fungal sequences.  Download the sequences with

     wget https://raw.githubusercontent.com/kylebittinger/q2-brocc/master/q2_brocc/tests/data/query.fasta
	 
and then search against the nt database with

     blastn -query query.fasta -db nt -outfmt 7

If successful, you should see a table of search results printed to
your screen.

We have one more thing to do before we start assigning sequences to
taxa.  To improve performance, we'll need to create a local database
of the NCBI taxonomy.  Run the following command to download and
process the taxonomy files:

     create_local_taxonomy_db.py

Once downloaded and configured, you should see a file at
`~/.brocc/taxonomy.db`, about 5G in size.  The BROCC software should
work without this database, but it will be unbearably slow to look up
the taxa one-by-one over a network connection.

## Making some taxonomic assignments

Let's download a couple of fungal sequences and try out the
assigner. We'll be using the plugin on QIIME 2 artifacts, not raw
sequence files.  The fungal sequences above are available as a QIIME 2
artifact by running:

    wget https://github.com/kylebittinger/q2-brocc/blob/master/q2_brocc/tests/data/query.qza?raw=true
	
We'll run the BROCC plugin using the command:

    qiime brocc classify-brocc --i-query query.qza --o-classification query-brocc.qza

Once the classifier has finished running, the `brocc-fungi-test`
directory should contain a QIIME 2 artifact, `query-brocc.qza`.  We
can create a visualization for this artifact by running:

    qiime metadata tabulate --m-input-file query-brocc.qza --o-visualization query-brocc.qzv
	
You can check out the visualization by dragging the file into your web
browser at https://view.qiime2.org/.  Your results should match those
in our test files: the sequence "pichia1" should be assigned to
"Eukaryota; Fungi; Ascomycota; Saccharomycetes; Saccharomycetales;
Phaffomycetaceae; Cyberlindnera; Cyberlindnera jadinii", and the
sequence named "trichosporon1" should be assigned to "Eukaryota;
Fungi; Basidiomycota; Tremellomycetes; Trichosporonales;
Trichosporonaceae; Trichosporon; Trichosporon asahii".

    

