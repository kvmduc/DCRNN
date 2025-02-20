from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import tensorflow as tf
import yaml
import numpy as np
import os.path as osp

from lib.utils import load_graph_data
from model.dcrnn_supervisor import DCRNNSupervisor


def main(args):
    with open(args.config_filename) as f:
        supervisor_config = yaml.load(f)
        # print(supervisor_config)
        # graph_pkl_filename = supervisor_config['data'].get('graph_pkl_filename')
        # sensor_ids, sensor_id_to_ind, adj_mx = load_graph_data(graph_pkl_filename)
        ######### Load adj matrix
        #########

        tf_config = tf.ConfigProto()
        if args.use_cpu_only:
            tf_config = tf.ConfigProto(device_count={'GPU': 0})
        tf_config.gpu_options.allow_growth = True
        with tf.Session(config=tf_config) as sess:
            ########################
            for year in range(int(supervisor_config['data']['begin_year']), int(supervisor_config['data']['end_year'])+1):
                adj_mx = np.load(osp.join(supervisor_config['data']['graph_pkl_filename'], str(year)+"_adj.npz"))["x"]
            ########################
                supervisor = DCRNNSupervisor(adj_mx=adj_mx, year=year, **supervisor_config)
                supervisor.train(sess=sess)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_filename', default=None, type=str,
                        help='Configuration filename for restoring the model.')
    parser.add_argument('--use_cpu_only', default=False, type=bool, help='Set to true to only use cpu.')
    args = parser.parse_args()
    main(args)
