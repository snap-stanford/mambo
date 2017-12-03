import os
import argparse

NULL = "NULL"
NONE = "None"
DELIMITER = "\t"
COMMENT = "#"


def create_mapping_table(mapping_file, mindex1, mindex2, output_file, 
                         output_index1, output_index2, output_title1, 
                         output_title2, delimiter=DELIMITER):
    index1 = output_index1 + 1
    index2 = output_index2 + 1
    title1 = output_title1 if output_title1 else "Index%d" % index1
    title2 = output_title2 if output_title2 else "Index%d" % index2
    titles = [title1, title2]

    mapping = {}
    with open(mapping_file, "r") as mf:
        for line in mf:
            if line[0] == COMMENT:
                continue
            split_line = line.strip().split(delimiter)
            name = split_line[mindex1]
            mname = split_line[mindex2]
            if name == NULL or mname == NULL:
                continue
            mapping[name] = mname

    num_fields = 0
    name_uid_map = {}
    uid_other_map = {}
    title_line = None
    if os.path.isfile(output_file):
        with open(output_file, "r") as of:
            for line in of:
                if line[0] == COMMENT:
                    title_line = line.strip()
                    continue
                split_line = line.strip().split(delimiter)
                num_fields = len(split_line) - 1
                uid_other_map[int(split_line[0])] = split_line[1:]
                if split_line[index1] != NONE:
                    name_uid_map[split_line[index1]] = int(split_line[0])
    max_count = max(uid_other_map.keys()) if len(uid_other_map.keys()) > 0 else -1
    seen_ids = set()
    with open(output_file, "w") as of:
        title_fields = title_line.split(delimiter)[1:] if title_line else []
        first_index = 0 if output_index1 < output_index2 else 1
        second_index = 1 if output_index1 < output_index2 else 0
        if first_index >= len(title_fields):
            title_fields.insert(first_index, titles[first_index])
            title_fields.insert(second_index, titles[second_index])
        else:
            title_fields[first_index] = titles[first_index]
            if second_index >= len(title_fields):
                title_fields.insert(second_index, titles[second_index])
            else:
                title_fields[second_index] = titles[second_index]
        title_field_string = delimiter.join(title_fields).strip()
        lines_to_write = ["%sMambo_id%s" % (COMMENT, delimiter)  + title_field_string + "\n"]

        for name in mapping:
            terms = []
            if name in name_uid_map:
                counter = name_uid_map[name]
                terms = uid_other_map[counter]
            else:
                max_count = max_count + 1
                counter = max_count
            if len(terms) == 0:
                new_num_fields = num_fields if index2 <= num_fields else num_fields + 1
                new_num_fields = 2 if len(uid_other_map.keys()) == 0 else new_num_fields
                terms = [NONE] * new_num_fields
                terms[index1-1] = name
                terms[index2-1] = mapping[name]
            elif len(terms) < index2:
                terms.append(mapping[name])
            elif terms[index2-1] == NONE:
                print terms, name, mapping[name]
                terms[index2-1] = name

            string = delimiter.join(terms)
            lines_to_write.append("%d%s%s\n" % (counter, delimiter, string))
            seen_ids.add(counter)

        for sid in uid_other_map:
            if sid not in seen_ids:
                terms = uid_other_map[sid]
                if len(terms) < index2:
                    terms.append(NONE)

                string = delimiter.join(terms)
                lines_to_write.append("%d%s%s\n" % (int(sid), delimiter, string))
        of.writelines(lines_to_write)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create dictionary mapping between naming terms.')
    parser.add_argument('mapping_file', type=str, help='mapping file name. should be a tsv.')
    parser.add_argument('output_file', type=str, help='output file name. should be a tsv.')

    parser.add_argument('--map_index1', type=int, default = 0)
    parser.add_argument('--map_index2', type=int, default=1)

    parser.add_argument('--output_index1', type=int, default = 0)
    parser.add_argument('--output_index2', type=int, default = 1)
    parser.add_argument('--output_title1', type=int, default = None)
    parser.add_argument('--output_title2', type=int, default = None)

    args = parser.parse_args()

    mapping_file = args.mapping_file
    mindex1 = args.map_index1
    mindex2 = args.map_index2

    output_file = args.output_file
    output_index1 = args.output_index1
    output_index2 = args.output_index2
    output_title1 = args.output_title1
    output_title2 = args.output_title2

    create_mapping_table(mapping_file, mindex1, mindex2, output_file,
                       output_index1, output_index2, output_title1,
                       output_title2)
