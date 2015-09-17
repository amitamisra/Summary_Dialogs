#!/usr/bin/python3

from optparse import OptionParser
from iac_objects import *
import sys, os, csv, shutil

# author: Brian (becker@ucsc.edu)
# Extract's chains of discussion between authors in createdebate
#
# Use the IAC python code provided at
# https://bitbucket.org/nlds_iac/internet-argument-corpus
# The iac database on the nldslab server will work with this
# script once you setup the username and password in your sql_auth.json
# file. You might need to do a few other things such as set your python
# path as covered in the readme for the repository.
#
# Create a directory iac/src/experiments/yourname/
# and place this script in that directory.
#
# This may also work for convinceme, as I think convinceme is threaded
# very similarly to createdebate.

def get_opts():
    parser = OptionParser()
    parser.add_option("-t", "--topic", dest="topic", action="store",
            help="The topic to extract from. If not specified, then use all topics."\
                    "Accepts many topics separated by commas")
    #parser.add_option("-d", "--dataset", dest="dataset", action="store",
    #        help="The dataset to extract from. If not sepcified, then use all datasets.")
    parser.add_option("-l", "--length-words", dest="word_max", action="store",
            help="The maximum length of a post in words. Default = 250.",
            default=250)
    parser.add_option("-c", "--length-chain", dest="chain_length", action="store",
            help="The chain length. Default = 6", default=6)
    parser.add_option("-o", "--output-dir", dest="output_dir", action="store",
            help="Where to store the output. Default = ./CSV/{topic}/discussion_dialogs",
            default="./CSV/{topic}/discussion_dialogs")

    (options, args) = parser.parse_args()
    output_dir = options.output_dir
    options.output_dir = output_dir if not output_dir.endswith("/") else output_dir[:-1]

    if "," in options.topic:
        # comma separated list, parse it
        options.topic = map(lambda x: x.strip(), options.topic.split(","))
    else:
        # make it into a singleton list for uniformity with the other possibility
        options.topic = [options.topic]

    if type(options.topic) is str:
        options.topic = [options.topic]

    # The first part of a chain counts as two
    options.chain_length = options.chain_length - 1

    # make this static.
    # createdebate uses parent posts as replies, applying this to fourforums would
    # not give quite the same result.
    options.dataset = "createdebate"

    return (options, args)

def get_id(table, res_col, selector_col, selector_val):
    if None in [table, res_col, selector_col, selector_val]:
        return None
    query_str = """select
        {0}
        from {1}
        where {2} = "{3}" """.format(res_col, table, selector_col, selector_val)

    return sql_session.execute(query_str).first()[0]

def get_topic_id(topic):
    return get_id("topics", "topic_id", "topic", topic)

def get_dataset_id(dataset):
    return get_id("datasets", "dataset_id", "name", dataset)

def get_discussions(topic, dataset):
    query = sql_session.query(Discussion)
    if not dataset is None:
        query = query.filter(Discussion.dataset_id==get_dataset_id(dataset))
    if not topic is None:
        query = query.filter(Discussion.topic_id==get_topic_id(topic))

    return query.all()

def get_parent_post(child_post):
    return sql_session.query(Post)\
        .filter(Post.dataset_id==child_post.dataset_id)\
        .filter(Post.discussion_id==child_post.discussion_id)\
        .filter(Post.post_id==child_post.parent_post_id)\
        .first()

def get_disc_from_post(post):
    return sql_session.query(Discussion)\
            .filter(Discussion.dataset_id==post.dataset_id)\
            .filter(Discussion.discussion_id==post.discussion_id)\
            .first()

def get_wc(post):
    query_str = """select count(*)
        from tokens
        where dataset_id = {0} and
              text_id = {1} """.format(post.dataset_id, post.text_obj.text_id)

    return sql_session.execute(query_str).first()[0]

def check_word_limit(limit, post):
     return get_wc(post) <= limit

def get_pairs(disc: Discussion):
    pairs = [(get_parent_post(post), post)
            if (post.parent_post_id is not None and post.parent_post_id != 0) else None
            for post in disc.posts]
    return filter(lambda x: x is not None, pairs)

def make_pairs_by_author(pairs):
    author_dict = dict()
    for parent, child in pairs:
        # Make sure that authors get grouped together no matter
        # there order
        pair_id = (parent.author_id, child.author_id) \
                if parent.author_id < child.author_id \
                else (child.author_id, parent.author_id)
        if pair_id not in author_dict:
            author_dict[pair_id] = list()
        author_dict[pair_id].append((parent, child))

    # These seem to be sorted even without doing this, but
    # sort anyways just in case.
    for k, v in author_dict.items():
        v = sorted(v, key=lambda x: x[0].post_id)

    return author_dict

def make_chains(pairs, word_limit, chain_limit):
    pairs_by_auth = make_pairs_by_author(pairs)
    # the list of valid chains to return
    chains = list()
    for k, pair_list in pairs_by_auth.items():
        # keep track of currently in progress chains by a dictionary which
        # uses the expected next post's id as the key. The value of the dict
        # is the chain in progress.
        chain_ends = dict()
        for pair in pair_list:
            key = pair[0].post_id
            new_key = pair[1].post_id
            if key in chain_ends:
                # There is already a chain in progress which this post should be
                # added onto
                chain = chain_ends[key]
                chain.append(pair)
                if not check_word_limit(word_limit, pair[1]):
                    # The post is too long, break the chain
                    if len(chain) > chain_limit:
                        chains.append(chain)
                else:
                    # setup the new end for the chain
                    chain_ends[new_key] = chain
                # Pop the old key because we have a new end of the chain
                # or the chain was completed (word limit)
                chain_ends.pop(key)

            elif key not in chain_ends:
                if check_word_limit(word_limit, pair[1]):
                    # Key isn't in the chain_ends, if it is passes the word limit
                    # check then add it to the chain_ends. There is no point in
                    # adding a new chain that doesn't pass the word limit check
                    # because it will immediately end as a chain of length 1.
                    chain_ends[new_key] = list()
                    chain_ends[new_key].append(pair)

        # add all the still open but valid chain_ends to chains
        for k, chain in chain_ends.items():
            if len(chain) >= chain_limit:
                chains.append(chain)

    return chains

# Write a row in the correct directory, creating it if it does not exist
def writerow(output_dir, disc_id, row):
    directory = "{0}/{1}".format(output_dir, disc_id)
    filename = "{0}/{1}dialog.csv".format(directory, disc_id)
    header = ["key", "quote_source_post_discussion_id",
        "posts_dataset_id", "posts_timestamp", "posts_author_id",
        "quote_source_author_id", "posts_native_post_id",
        "quote_source_timestamp", "post_text_id", "Word_Count",
        "quote_source_post_id", "post_text", "quote_source_text_id",
        "Dialog_Turn", "posts_discussion_id", "quote_source_post_dataset_id",
        "Fullquote_text", "discussion_url", "quote_source_native_post_id",
        "posts_post_id"]

    if not os.path.exists(directory):
        os.makedirs(directory)

    writeheader = False
    if not os.path.exists(filename):
        writeheader = True

    with open(filename, "a") as f:
        writer = csv.writer(f)
        if writeheader:
            writer.writerow(header)

        writer.writerow(row)

def make_row(post, dialog_turn):
    qp = get_parent_post(post)
    key = "{0}-{1}_{2}_{3}_{4}".format(post.dataset_id,
        post.discussion_id, post.post_id, qp.post_id,
        dialog_turn)

    row = [
            key, qp.discussion_id, post.dataset_id, post.timestamp,
            post.author_id, qp.author_id, post.native_post_id,
            qp.timestamp, post.text_id, get_wc(post), qp.post_id, post.text_obj.text,
            qp.text_id, dialog_turn, post.discussion_id, qp.dataset_id,
            qp.text_obj.text, get_disc_from_post(post).discussion_url,
            qp.native_post_id, post.post_id
          ]

    return row

# Returns a list of strings that a csv writer can print
def print_chains_to_file(output_dir, chains):
    dialog_turns = dict()
    for chain in chains:
        disc_id = chain[0][0].discussion_id
        if disc_id not in dialog_turns:
            dialog_turns[disc_id] = 1
        dialog_turn = dialog_turns[disc_id]
        first = True
        for pair in chain:
            writerow(output_dir, disc_id, make_row(pair[1], dialog_turn))

        dialog_turns[disc_id] += 1

def clear_output_dir(output_dir):
    for root, dirs, files in os.walk(output_dir + "/"):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

def print_chain_info(chain):
    print("Chain: is of length {0}".format(len(chain) + 1))
    for pair in chain:
        print("\t({0}) {1}: ({2}) {3}".format(pair[0].parent_post_id, pair[0].post_id,
            pair[1].parent_post_id, pair[1].post_id))

# print chains for debug
def print_chains_info(chains):
    print("There are {0} chains".format(len(chains)))
    for i in range(0, len(chains)):
        print_chain_info(chains[i])
        print("")

def run():
    (options, args) = get_opts()
    for topic in options.topic:
        print("working on topic: {0}".format(topic))
        output_dir = options.output_dir
        if "{topic}" in output_dir:
            # sub in the topic
            output_dir = output_dir.format(topic=topic)

        print("outputting to: {0}".format(output_dir))
        discussions = get_discussions(topic, options.dataset)
        chains = list()
        for disc in discussions:
            pairs = get_pairs(disc)
            chains += make_chains(pairs, options.word_max, options.chain_length)

        #print_chains_info(chains)
        clear_output_dir(output_dir)
        print_chains_to_file(output_dir, chains)

if __name__ == "__main__":
    run()
