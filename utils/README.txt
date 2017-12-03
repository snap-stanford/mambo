This directory creates generic scripts than can be used to create snap-formatted tsvs for modes
and crossnets. This directory currently consists of three files:

1. create_snap_mode_table.py
	Input:    - original dataset, in tsv form
	Output:   - Snap mode table tsv (snap_nid\tdataset_id)
	          - dataset specific mode snap table tsv (snap_nid\tdataset_entity_id)
2. create_mapped_mode_table.py
	Input:    - original dataset and dictionary, in tsv form
	Output:   - Snap mode table tsv (snap_nid\tdataset_id)
	          - dataset specific mode snap table tsv (snap_nid\tdataset_entity_id)
3. create_snap_crossnet_table.py
	Input:    - Source dataset specific snap mode table tsv
	          - Destination dataset specific snap mode table tsv
	          - the dataset (in tsv form) specifying edges.
	Output:   - Snap crossnet table tsv (snap_eid\tdataset_id\tsnap_src_nid\tsnap_dst_nid) 
	          - The dataset specific snap table tsv (snap_eid\tsrc_dataset_id\tdst_dataset_id)

It also contains scripts to pull out unique node ids and create an edge list (i.e. remove 
extraneous fields, but can also handle input lines that model many-to-many, many-to-1, and
1-to-many relationships):

Below are details on the arguments and usage for each script (taken from the header of each file):

########################################
###     create_snap_mode_table.py    ###
########################################

Script that creates snap tables for a given mode.

Usage:
python create_snap_mode_table.py <input_file_path> <mode_name> <dataset_name> <dataset_id>

Positional Arguments:
input_file:              Path to the input file; Input file should be a tsv.
mode_name:               Name of the mode being created e.g. genes
dataset_name:            Name of dataset being used to create the snap mode tables i.e. the 
                         dataset the input file comes from. e.g. STRING
dataset_id:              unique integer id for this dataset.


Optional arguments:
--node_index:            If there are multiple columns in the input tsv, the index of the column with the node id.
                         Defaults to 0.
--output_dir:            Directory to create output files. Defaults to the current working directory.
--full_mode_file:        Name of output file tsv containing a list of <snap_id>\t<dataset_id>.
                         Defaults to output_dir/miner-<mode_name>-<date>.tsv
--db_node_file:          Name of output file tsv for a specific dataset; contains a list of <snap id>\t<dataset_specific_entity_id>
                         Defaults to output_dir/miner-<mode_name>-<dataset_id>-<dataset>-<date>.tsv
--snap_id_counter_start  Start assigning snap ids from this integer value; this number MUST be greater
                         than any id found in the full mode file. If not specified, finds the max id in the
                         full_mode_file.

Example usage:
Creating files for genes using two datasets, GeneOntology and HUGO:

Input files: hugo.tsv and go.tsv

Output directory: outputs/genes/

Output files: miner-gene-20160520.tsv, miner-gene-0-GO-20160520.tsv, miner-gene-1-HUGO-20160520.tsv

Workflow:

python create_snap_mode_table.py go.tsv gene GO 0 --output_dir outputs/genes/
python create_snap_mode_table.py hugo.tsv gene HUGO 1 --output_dir outputs/genes/

########################################
###    create_mapped_mode_table.py   ###
########################################

file: create_mapped_mode_table.py

Script that creates snap tables for a given mode which requires a mapping file.

Usage:
python create_mapped_mode_table.py <mode_name> <input_file_path> <dataset_name> <dataset_id> <mapping_file> <map_index>

Positional Arguments:
mode_name:               Name of the mode being created e.g. genes
input_file:              Path to the input file; Input file should be a tsv.
dataset_name:            Name of dataset being used to create the snap mode tables i.e. the 
                         database the input file comes from. e.g. STRING
db_id:                   unique integer id for this datadatabaseset.
mapping_file:            Path to the dictionary that maps unique snap node ids to database and/or naming scheme specific ids.
map_index:               In the dictionary (mapping file), the index of the column with the naming scheme for this database.

Optional arguments:
--node_index:            If there are multiple columns in the input tsv, the index of the column with the node id.
                         Defaults to 0.
--output_dir:            Directory to create output files. Defaults to the current working directory.
--full_mode_file:        Name for the output file tsv containing a list of <snap_id>\t<dataset_id>.
                         Defaults to output_dir/miner-<mode_name>-<date>.tsv
--db_node_file:          Name of output file tsv for a specific dataset; contains a list of <snap id>\t<dataset_specific_entity_id>
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

############################################
###     create_snap_crossnet_table.py    ###
############################################

Script that creates snap tables for a given crossnet.

Usage:
python create_snap_crossnet_table.py <input_file_path> <src_file_path> <dst_file_path> <dataset_name> <dataset_id>

Positional Arguments:
input_file               Path to the input file; Input file should be a tsv.
src_file                 Path to a dataset specific file, as outputted by create_snap_mode_table.py,
                         corresponding to the source mode. File name MUST MATCH FORMAT:
                         miner-<mode_name>-<dataset_id>-<dataset>-<date>.tsv
dst_file                 Path to a dataset specific file, as outputted by create_snap_mode_table.py,
                         corresponding to the destination mode. File name MUST MATCH FORMAT:
                         miner-<mode_name>-<dataset_id>-<dataset>-<date>.tsv
dataset_name:            Name of dataset being used to create the snap crossnet tables i.e. the 
                         dataset the input file comes from. e.g. STRING
dataset_id:              unique integer id for this dataset.


Optional arguments:
--src_node_index:        If there are multiple columns in the input tsv, the index of the column with the src node id.
                         Defaults to 0.
--dst_node_index:        If there are multiple columns in the input tsv, the index of the column with the dst node id.
                         Defaults to 1.
--output_dir:            Directory to create output files. Defaults to the current working directory.
--full_crossnet_file:    Name of output file tsv containing a list of <snap_id>\t<dataset_id>.
                         Defaults to output_dir/miner-<src_mode_name>-<dst_mode_name>-<date>.tsv
--db_edge_file:          Name of output file tsv for a specific dataset; contains a list of <snap id>\t<dataset_specific_entity_id>
                         Defaults to output_dir/miner-<src_mode_name>-<dst_mode_name>-<dataset_id>-<dataset>-<date>.tsv
--snap_id_counter_start  Start assigning snap ids from this integer value; this number MUST be greater
                         than any id found in the full crossnet file. If not specified, finds the max id in the
                         full_crossnet_file.
--skip_missing_ids       Flag; If any of the ids in the input tsv do not have snap ids (which are fetched from
                         the src and dst files), skip the line and continue parsing the data.
--src_mode_filter        The name of a function in utils.py that should be applied to the source node id in 
                         in the input file before using it to look up the snap id in the src_file. Defaults to None.
--dst_mode_filter        The name of a function in utils.py that should be applied to the destination node id in 
                         in the input file before using it to look up the snap id in the dst_file. Defaults to None.

Example usage:
Creating files for genes-function relationships using GeneOntology:

Input files: go.tsv, miner-gene-0-GO-20160520.tsv, miner-function-0-GO-20160520.tsv

Output directory: outputs/genes-functions/

Output files: miner-gene-function-20160520.tsv, miner-gene-function-0-GO-20160520.tsv

Workflow:

python create_snap_crossnet_table.py go.tsv miner-gene-0-GO-20160520.tsv miner-function-0-GO-20160520.tsv GO 0 --output_dir outputs/genes-functions/