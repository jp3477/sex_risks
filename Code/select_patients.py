from utils import Utils
from database import Database
import pandas as pd
import numpy as np

u = Utils()
db = Database('Mimir from Munnin')


def fetch_patients():
    # get patients that have sex
    q_patients_w_sex = "SELECT safetyreportid, patient_sex, patient_custom_master_age FROM effect_openfda_19q2.patient WHERE patient_sex='Female' OR patient_sex='Male'"
    res_patients_w_sex = db.run_query(q_patients_w_sex)

    # make dataframe
    df_patients = pd.DataFrame(res_patients_w_sex,
                               columns=['PID', 'Sex', 'Age'])

    # replace 'Male' 'Female' with M, F
    df_patients = df_patients.replace('Female', 'F').replace('Male', 'M')

    # drop missing ages
    df_patients = df_patients.patients.replace('', np.nan)
    df_patients = df_patients.dropna(subset=['Age'])
    df_patients = df_patients.astype({'Age': 'int'})

    # remove age below 18 and above 85
    df_patients = df_patients.query('Age>=18 and Age<=85')

    # Save patients
    u.save_df(df_patients, 'df_patients')

    return df_patients


if __name__ == '__main__':
    fetch_patients()