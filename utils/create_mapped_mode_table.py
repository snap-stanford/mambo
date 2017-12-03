'''
file: create_mapped_mode_table.py

Script that creates mambo tables for a given mode which requires a mapping file.

Usage:
python create_mapped_mode_table.py <mode_name> <input_file_path> <dataset_name> <dataset_id> <mapping_file> <map_index>

Positional Arguments:
mode_name:               Name of the mode being created e.g. genes
input_file:              Path to the input file; Input file should be a tsv.
dataset_name:            Name of dataset being used to create the mambo mode tables i.e. the 
                         database the input file comes from. e.g. STRING
db_id:                   unique integer id for this datadatabaseset.
mapping_file:            Path to the dictionary that maps unique mambo node ids to database and/or naming scheme specific ids.
map_index:               In the dictionary (mapping file), the index of the column with the naming scheme for this database.

Optional arguments:
--node_index:            If there are multiple columns in the input tsv, the index of the column with the node id.
                         Defaults to 0.
--output_dir:            Directory to create output files. Defaults to the current working directory.
--full_mode_file:        Name for the output file tsv containing a list of <mambo_id>\t<dataset_id>.
                         Defaults to output_dir/miner-<mode_name>-<date>.tsv
--db_node_file:          Name of output file tsv for a specific dataset; contains a list of <mambo_id>\t<dataset_specific_entity_id>
                         Defaults to output_dir/miner-<mode_name>-<dataset_id>-<dataset>-<date>.tsv
--skip_missing_ids:      For ids in the database but not the dictionary, skip if false. Otherwise add to the mapping file. 
                         Defaults to False.

Example usage:
Creating files for genes using two datasets, STRING and GO:

Input files: string_parsed.tsv and go_parsed.tsv

Mapping file: uniprot_ensembl.tsv

Output directory: outputs/protein/

Output files: miner-gene-20160520.tsv, miner-gene-0-GO-20160520.tsv, miner-gene-1-HUGO-20160520.tsv

Workflow:

python create_mapped_mode_table.py protein string_parsed.tsv STRING 0 uniprot_ensembl.tsv 1 --output_dir outputs/protein/
python create_mapped_mode_table.py protein go_parsed.tsv GO_UNIPROT 1 uniprot_ensembl.tsv 2 --output_dir outputs/protein/
'''

import argparse
import os
import utils

COMMENT = ["#", "!", "\n"]
DELIMITER = "\t"
NONE = "None"


def create_mapped_mode_table(mode_name, input_file, dataset_name, db_id,
                             mapping_file, skip, map_index, node_index,
                             output_dir, full_mode_file, db_node_file, delimiter=DELIMITER):
    if full_mode_file is None:
        full_mode_file = os.path.join(output_dir, utils.get_full_mode_file_name(mode_name))
    full_mode_map = {}
    if os.path.isfile(full_mode_file):
        with open(full_mode_file, 'r') as fm_file:
            for line in fm_file:
                if line[0] in COMMENT:  # skip comments
                    continue
                split_line = line.strip().split(delimiter)
                full_mode_map[int(split_line[0])] = split_line[1]

    if db_node_file is None:
        db_node_file = os.path.join(output_dir, utils.get_mode_file_name(mode_name, db_id, dataset_name))

    max_id = 0
    mapping = {}
    num_cols = 0
    with open(mapping_file, 'r') as mf:
        for line in mf:
            if line[0] in COMMENT:
                continue
            split_line = line.strip().split(delimiter)
            num_cols = len(split_line)
            mapping[split_line[map_index]] = split_line[0]
            max_id = int(split_line[0])

    has_header = True
    seen = set()
    seen_counter = set()
    with open(full_mode_file, 'w') as fm_file, \
            open(input_file, "r") as in_file, \
            open(db_node_file, 'w') as db_file, open(
            mapping_file, 'a') as mf:
        fm_file.write('# Full mode table for %s\n' % mode_name)
        fm_file.write('# File generated on: %s\n' % utils.get_current_date())
        fm_file.write('# mambo_nid%sdataset_ids\n' % delimiter)

        db_file.write('# Mode table for dataset: %s\n' % dataset_name)
        db_file.write('# File generated on: %s\n' % utils.get_current_date())

        add_schema = True
        for line in in_file:
            if line[0] in COMMENT or has_header:  # skip comments
                has_header = False
                continue

            vals = utils.split_then_strip(line, delimiter)
            if add_schema:
                attrs_schema = '# mambo_nid%sdataset_nid' % delimiter
                for i in range(len(vals)):
                    if i != node_index:
                        attrs_schema += '%sC%d' % (delimiter, i)
                db_file.write('%s\n' % attrs_schema)
                add_schema = False

            node_id = vals[node_index].split('.')
            node_id = node_id[0] if len(node_id) == 1 else node_id[1]
            if node_id in seen or len(node_id) == 0:
                continue
            attrs_str = ''
            for i in range(len(vals)):
                if i != node_index:
                    attrs_str += delimiter + vals[i]
            counter = 0
            if node_id in mapping:
                counter = int(mapping[node_id])
            elif not skip:
                max_id = max_id + 1
                counter = max_id
                result = "%d%s" % (counter, delimiter)
                for i in range(num_cols - 1):
                    label = NONE if i + 1 != map_index else node_id
                    result = result + label + delimiter
                result = result.strip(delimiter) + '\n'
                mf.write(result)
            db_ids = full_mode_map[counter] + "," + str(db_id) if counter in full_mode_map else str(db_id)
            fm_file.write('%d%s%s\n' % (counter, delimiter, db_ids))
            db_file.write('%d%s%s%s\n' % (counter, delimiter, vals[node_index], attrs_str))
            seen.add(node_id)
            seen_counter.add(counter)
        for counter in full_mode_map:
            if counter not in seen_counter:
                fm_file.write('%d%s%s\n' % (counter, delimiter, full_mode_map[counter]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create mapped mambo mode tables')
    parser.add_argument('mode_name', type=str, help='mode name')
    parser.add_argument('input_file',
                        help='input file name. File should be a tsv, with one mode-specific id per line (unless --node_index specified)')
    parser.add_argument('dataset_name', type=str, help='name of dataset')
    parser.add_argument('db_id', type=int, help='int id for this dataset')
    parser.add_argument('mapping_file', type=str, help='int id for this dataset')
    parser.add_argument('map_index', type=int, help='int id for this dataset')

    parser.add_argument('--node_index', type=int, help='column index that contains node ids', default=0)
    parser.add_argument('--output_dir',
                        help='directory to output files; either this argument or full_mode_file and db_node_file MUST be specified',
                        default='.')
    parser.add_argument('--full_mode_file',
                        help='output file name; outputs a list of mambo ids and the db ids (db the mambo id was derived from);' \
                             + 'note that this file is appended to; OVERRIDES output_dir argument', default=None)
    parser.add_argument('--db_node_file',
                        help='output file name; output contains mapping of mambo ids to db protein ids; OVERRIDES output dir argument',
                        default=None)
    parser.add_argument('--skip_missing_ids', action='store_true')
    args = parser.parse_args()

    mode_name = args.mode_name
    input_file = args.input_file
    dataset_name = args.dataset_name
    db_id = args.db_id
    mapping_file = args.mapping_file
    skip = args.skip_missing_ids
    map_index = args.map_index
    node_index = args.node_index
    output_dir = args.output_dir
    full_mode_file = args.full_mode_file
    db_node_file = args.db_node_file

    create_mapped_mode_table(mode_name, input_file, dataset_name, db_id,
                             mapping_file, skip, map_index, node_index,
                             output_dir, full_mode_file, db_node_file)
