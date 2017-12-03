'''
file: create_mambo_mode_table.py

Script that creates mambo tables for a given mode.

Usage:
python create_mambo_mode_table.py <input_file_path> <mode_name> <dataset_name> <dataset_id>

Positional Arguments:
input_file:              Path to the input file; Input file should be a tsv.
mode_name:               Name of the mode being created e.g. genes
dataset_name:            Name of dataset being used to create the mambo mode tables i.e. the 
                         dataset the input file comes from. e.g. STRING
dataset_id:              unique integer id for this dataset.


Optional arguments:
--node_index:            If there are multiple columns in the input tsv, the index of the column with the node id.
                         Defaults to 0.
--output_dir:            Directory to create output files. Defaults to the current working directory.
--full_mode_file:        Name of output file tsv containing a list of <mambo_id>\t<dataset_id>.
                         Defaults to output_dir/miner-<mode_name>-<date>.tsv
--db_node_file:          Name of output file tsv for a specific dataset; contains a list of <mambo_id>\t<dataset_specific_entity_id>
                         Defaults to output_dir/miner-<mode_name>-<dataset_id>-<dataset>-<date>.tsv
--mambo_id_counter_start  Start assigning mambo ids from this integer value; this number MUST be greater
                         than any id found in the full mode file. If not specified, finds the max id in the
                         full_mode_file.

Example usage:
Creating files for genes using two datasets, GeneOntology and HUGO:

Input files: hugo.tsv and go.tsv

Output directory: outputs/genes/

Output files: miner-gene-20160520.tsv, miner-gene-0-GO-20160520.tsv, miner-gene-1-HUGO-20160520.tsv

Workflow:

python create_mambo_mode_table.py go.tsv gene GO 0 --output_dir outputs/genes/
python create_mambo_mode_table.py hugo.tsv gene HUGO 1 --output_dir outputs/genes/
'''

import argparse
import utils
import os

COMMENT = ["#", "!", "\n"]
DELIMITER = "\t"


def create_mambo_mode_table(input_file, db_id, mode_name, dataset_name, 
                           full_mode_file, output_dir, db_node_file,
                           mambo_id_counter_start, node_index, verbose=False, delimiter=DELIMITER):
    # Process command line arguments, get default path names
    inFNm = input_file
    db_id = db_id
    mode_name = mode_name
    dataset = dataset_name
    outFNm = full_mode_file
    if outFNm is None:
        outFNm = os.path.join(output_dir, utils.get_full_mode_file_name(mode_name))
    dbFNm = db_node_file
    if dbFNm is None:
        dbFNm = os.path.join(output_dir, utils.get_mode_file_name(mode_name, db_id, dataset))

    counter = mambo_id_counter_start
    if counter == -1:
        counter = utils.get_max_id(outFNm)

    # Read input file, create output files.
    seen = set()
    if verbose:
        print 'Starting at mambo id: %d' % counter
    with open(inFNm, 'r') as inF, open(outFNm, 'a') as outF, open(dbFNm, 'w') as dbF:
        if counter == 0:
            outF.write('# Full mode table for %s\n' % mode_name)
            outF.write('# File generated on: %s\n' % utils.get_current_date())
            outF.write('# mambo_nid%sdataset id\n' % delimiter)
        dbF.write('# Mode table for dataset: %s\n' % dataset)
        dbF.write('# File generated on: %s\n' % utils.get_current_date())
        add_schema = True
        for line in inF:
            if line[0] in COMMENT: # skip comments
                continue
            vals = utils.split_then_strip(line, delimiter)
            if add_schema:
                attrs_schema = '# mambo_nid%sdataset_nid' % delimiter
                for i in range(len(vals)):
                    if i != node_index:
                        attrs_schema += '%sC%d' % (delimiter, i)
                dbF.write('%s\n' % attrs_schema)
                add_schema = False
            node_id = vals[node_index]
            if node_id in seen or len(node_id) == 0:
                continue
            attrs_str = ''
            for i in range(len(vals)):
                if i != node_index:
                    attrs_str += delimiter + vals[i]
            outF.write('%d%s%d\n' % (counter, delimiter, db_id))
            dbF.write('%d%s%s%s\n' % (counter, delimiter, node_id, attrs_str))
            seen.add(node_id)
            counter += 1
    if verbose:
        print 'Ending at mambo id: %d' % counter


if __name__ == "__main__":
    
    # Create command line arguments
    parser = argparse.ArgumentParser(description='Create mambo node tables; for more detailed description, please see file header.')
    parser.add_argument('input_file', help='input file name. File should be a tsv, with one mode-specific id per line (unless --node_index specified)')
    parser.add_argument('mode_name', type=str, help='mode name')
    parser.add_argument('dataset_name', type=str, help='name of dataset')
    parser.add_argument('db_id', type=int, help='int id for this dataset')
    parser.add_argument('--node_index', type=int, help='column index that contains node ids', default=0)
    parser.add_argument('--output_dir', help='directory to output files; either this argument or full_mode_file and db_node_file MUST be specified', default='.')
    parser.add_argument('--full_mode_file', help='output file name; outputs a list of mambo ids and the db ids (db the mambo id was derived from);' \
        + 'note that this file is appended to; OVERRIDES output_dir argument', default=None)
    parser.add_argument('--db_node_file', help='output file name; output contains mapping of mambo ids to db protein ids; OVERRIDES output dir argument', default=None)
    parser.add_argument('--mambo_id_counter_start', type=int, help='where to start assigning mambo ids', default=-1)
    
    # Parse command line arguments
    args = parser.parse_args()
    inFNm = args.input_file
    db_id = args.db_id
    mode_name = args.mode_name
    dataset = args.dataset_name
    outFNm = args.full_mode_file
    output_dir = args.output_dir
    dbFNm = args.db_node_file
    counter = args.mambo_id_counter_start
    node_index = args.node_index
    
    # Construct the mode tables
    create_mambo_mode_table(inFNm, db_id, mode_name, dataset, outFNm, output_dir, dbFNm, counter, node_index)
