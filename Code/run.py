import sys
from collections import Counter
import numpy as np
import pandas as pd
import pyarrow.feather as feather
from scipy import stats
import pymysql
import pymysql.cursors
from database import Database
from utils import Utils
from drug import Drug

from tqdm import tqdm

np.random.seed(222020)


def main(argv):

    u = Utils()
    iterations = 25

    # idx = int(argv[1])
    print('Loading drugs')
    drugs = u.load_np('drugs')

    pbar = tqdm(drugs)
    for drugID in pbar:
        pbar.set_description(f"drug: {drugID}")
        # drugID = drugs[idx]
        try:

            # print(f'DrugID: {drugID}')

            # print('Reading status')
            # status = u.read_status(drugID)

            # if status == 'no':

            # try:

            u.write_status(drugID, 'working')

            drug = Drug(drugID)

            # print('Iterating and matching')
            for itr in tqdm(range(1, iterations + 1), desc='iterations'):
                drug.match()
                drug.count_adr()
                drug.assign_abcd(itr)
                drug.do_chi_square()
                drug.calc_logROR()
                drug.reset_for_next_itr()

            # print('Saving results')
            x = drug.save_results(iterations)

            if x:
                u.write_status(drugID, 'yes')
            else:
                u.write_status(drugID, 'no')

        except:
            # print('Failed miserably')
            info = str(sys.exc_info()[1])
            u.write_status(drugID, 'error ' + info)


if __name__ == "__main__":
    main(sys.argv)
