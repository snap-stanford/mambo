'''
file: create_mambo_crossnet_table.py

Script that creates Mambo tables for a given crossnet.

Usage:
python create_mambo_crossnet_table.py <input_file_path> <src_file_path> <dst_file_path> <dataset_name> <dataset_id>

Positional Arguments:
input_file:              Path to the input file; Input file should be a tsv.
src_file:                Path to a dataset specific file, as outputted by create_mambo_mode_table.py,
                         corresponding to the source mode. File name MUST MATCH FORMAT:
                         miner-<mode_name>-<dataset_id>-<dataset>-<date>.tsv
dst_file:                Path to a dataset specific file, as outputted by create_mambo_mode_table.py,
                         corresponding to the destination mode. File name MUST MATCH FORMAT:
                         miner-<mode_name>-<dataset_id>-<dataset>-<date>.tsv
dataset_name:            Name of dataset being used to create the mambo crossnet tables i.e. the 
                         dataset the input file comes from. e.g. STRING
dataset_id:              unique integer id for this dataset.


Optional arguments:
--src_node_index:        If there are multiple columns in the input tsv, the index of the column with the src node id.
                         Defaults to 0.
--dst_node_index:        If there are multiple columns in the input tsv, the index of the column with the dst node id.
                         Defaults to 1.
--output_dir:            Directory to create output files. Defaults to the current working directory.
--full_crossnet_file:    Name of output file tsv containing a list of <mambo_id>\t<dataset_id>.
                         Defaults to output_dir/miner-<src_mode_name>-<dst_mode_name>-<date>.tsv
--db_edge_file:          Name of output file tsv for a specific dataset; contains a list of <mambo_id>\t<dataset_specific_entity_id>
                         Defaults to output_dir/miner-<src_mode_name>-<dst_mode_name>-<dataset_id>-<dataset>-<date>.tsv
--mambo_id_counter_start  Start assigning mambo ids from this integer value; this number MUST be greater
                         than any id found in the full crossnet file. If not specified, finds the max id in the
                         full_crossnet_file.
--skip_missing_ids       Flag; If any of the ids in the input tsv do not have mambo ids (which are fetched from
                         the src and dst files), skip the line and continue parsing the data.
--src_mode_filter        The name of a function in utils.py that should be applied to the source node id in 
                         in the input file before using it to look up the mambo id in the src_file. Defaults to None.
--dst_mode_filter        The name of a function in utils.py that should be applied to the destination node id in 
                         in the input file before using it to look up the mambo id in the dst_file. Defaults to None.

Example usage:
Creating files for genes-function relationships using Gene Ontology:

Input files: go.tsv, miner-gene-0-GO-20160520.tsv, miner-function-0-GO-20160520.tsv

Output directory: outputs/genes-functions/

Output files: miner-gene-function-20160520.tsv, miner-gene-function-0-GO-20160520.tsv

Workflow:

python create_mambo_crossnet_table.py go.tsv miner-gene-0-GO-20160520.tsv miner-function-0-GO-20160520.tsv GO 0 --output_dir outputs/genes-functions/
'''

import argparse
import utils
import os

COMMENT = ["#", "!", "\n"]
DELIMITER = "\t"


def create_mambo_crossnet_table(input_file, src_file, dst_file, dataset_name,
                               db_id, src_node_index, dst_node_index, mode_name1,
                               mode_name2, output_dir, full_crossnet_file, db_edge_file,
                               src_mode_filter, dst_mode_filter, mambo_id_counter_start,
                               skip_missing_ids, verbose=False, delimiter=DELIMITER):
    inFNm = input_file
    srcFile = src_file
    dstFile = dst_file
    dataset = dataset_name
    db_id = db_id

    srcIdx = src_node_index
    dstIdx = dst_node_index

    src_db_id = utils.parse_dataset_id_from_name(os.path.basename(srcFile))
    dst_db_id = utils.parse_dataset_id_from_name(os.path.basename(dstFile))

    mode_name1 = utils.parse_mode_name_from_name(os.path.basename(srcFile)) if mode_name1 is None else mode_name1
    mode_name2 = utils.parse_mode_name_from_name(os.path.basename(dstFile)) if mode_name2 is None else mode_name2

    outFNm = full_crossnet_file
    if outFNm is None:
        outFNm = os.path.join(output_dir, utils.get_full_cross_file_name(mode_name1, mode_name2))
    outFNm2 = db_edge_file
    if outFNm2 is None:
        outFNm2 = os.path.join(output_dir, utils.get_cross_file_name(mode_name1, mode_name2, db_id, dataset))


    src_mapping = utils.read_mode_file(srcFile)
    if os.path.samefile(srcFile, dstFile):
        dst_mapping = src_mapping
    else:
        dst_mapping = utils.read_mode_file(dstFile)

    src_filter = utils.get_filter(src_mode_filter)
    dst_filter = utils.get_filter(dst_mode_filter)

    add_schema = True
    counter = mambo_id_counter_start
    if counter == -1:
        counter = utils.get_max_id(outFNm)
    if verbose:
        print 'Starting at mambo id: %d' % counter
    with open(inFNm, 'r') as inF, open(outFNm, 'a') as fullF, open(outFNm2, 'w') as dbF:
                # Add schema/metadata
        if counter == 0:
            fullF.write('# Full crossnet file for %s to %s\n' % (mode_name1, mode_name2))
            fullF.write('# File generated on: %s\n' % utils.get_current_date())
            fullF.write('# mambo_eid%sdataset_id%ssrc_mambo_nid%sdst_mambo_nid\n' % (
                delimiter, delimiter, delimiter))
        dbF.write('# Crossnet table for dataset: %s\n' % dataset)
        dbF.write('# File generated on: %s\n' % utils.get_current_date())
        # Process file
        for line in inF:
            if line[0] in COMMENT:
                continue
            vals =  utils.split_then_strip(line, delimiter)
            if add_schema:
                attrs_schema = '# mambo_eid%ssrc_dataset_id%sdst_dataset_id' % (delimiter, delimiter)
                for i in range(len(vals)):
                    if i != srcIdx and i != dstIdx:
                        attrs_schema += '%sC%d' % (delimiter, i)
                dbF.write('%s\n' % attrs_schema)
                add_schema = False
            id1 = vals[srcIdx]
            id2 = vals[dstIdx]
            if src_filter:
                id1 = src_filter(id1)
            if dst_filter:
                id2 = dst_filter(id2)
            if id1 == '' or id2 == '':
                continue
            if skip_missing_ids and (id1 not in src_mapping or id2 not in dst_mapping):
                #print id1, id2
                continue
            attr_strs = ''
            for i in range(len(vals)):
                if i != srcIdx and i != dstIdx:
                    attr_strs += delimiter + vals[i]
            fullF.write('%d%s%d%s%d%s%d\n' % (
                counter, delimiter, db_id, delimiter, src_mapping[id1], delimiter, dst_mapping[id2]))
            dbF.write('%d%s%d%s%d%s\n' % (counter, delimiter, src_db_id, delimiter, dst_db_id, attr_strs))
            counter += 1
    if verbose:
        print 'Ending at mambo id: %d' % counter


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create mambo edge tables')
    parser.add_argument('input_file', help='input file name. File should be a tsv, containing interactions between ids found in src_file_name and ids found in dst_file_name')
    parser.add_argument('src_file', help='input file name. Should be a file outputted by create_mambo_mode_table (with properly formatted name).')
    parser.add_argument('dst_file', help='input file name. Should be a file outputted by create_mambo_mode_table (with properly formatted name).')
    parser.add_argument('dataset_name', type=str, help='name of dataset')
    parser.add_argument('db_id', type=int, help='int id for this dataset')

    parser.add_argument('--mode_name1', type=str, default = None)
    parser.add_argument('--mode_name2', type=str, default=None)

    parser.add_argument('--src_node_index', type=int, help='column index that contains src node ids (NOT mambo ids, from src_input_file)', default=0)
    parser.add_argument('--dst_node_index', type=int, help='column index that contains dst node ids (NOT mambo ids, from dst_input_file)', default=1)
    parser.add_argument('--output_dir', help='directory to output files; either this argument or full_crossnet_file and db_edge_file MUST be specified', default='.')
    parser.add_argument('--full_crossnet_file', help='output file name; outputs a list of mambo ids, the db ids (db the mambo id was derived from), and source and destination mambo node ids;' \
        + 'note that this file is appended to; OVERRIDES output_dir argument', default=None)
    parser.add_argument('--db_edge_file', help='output file name; output contains mapping of mambo ids to dataset ids; OVERRIDES output dir argument', default=None)
    parser.add_argument('--skip_missing_ids', action='store_true', help='don\'t throw an error if ids in input_file not found in src or dst file.')
    parser.add_argument('--mambo_id_counter_start', type=int, help='where to start assigning mambo ids', default=-1)
    parser.add_argument('--src_mode_filter', type=str, default=None)
    parser.add_argument('--dst_mode_filter', type=str, default=None)
    args = parser.parse_args()
    
    inFNm = args.input_file
    srcFile = args.src_file
    dstFile = args.dst_file
    dataset = args.dataset_name
    db_id = args.db_id

    srcIdx = args.src_node_index
    dstIdx = args.dst_node_index
    
    mode_name1 = args.mode_name1
    mode_name2 = args.mode_name2
    
    output_dir = args.output_dir
    outFNm = args.full_crossnet_file
    outFNm2 = args.db_edge_file
    
    src_mode_filter = args.src_mode_filter
    dst_mode_filter = args.dst_mode_filter
    
    counter = args.mambo_id_counter_start
    skip_missing_ids = args.skip_missing_ids
    
    create_mambo_crossnet_table(inFNm, srcFile, dstFile, dataset,
                               db_id, srcIdx, dstIdx, mode_name1,
                               mode_name2, output_dir, outFNm, outFNm2,
                               src_mode_filter, dst_mode_filter, counter,
                               skip_missing_ids)
