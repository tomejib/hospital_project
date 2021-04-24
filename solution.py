import pandas as pd
import numpy as np

def give_treatment(row):
    result = None
    if row['covid_positive']:
        weights = [0.6, 0.4] if row['age'] <= 16 else [0.7, 0.3]
        result = np.random.choice([0, 1], p=weights)
    return result

def create_emergency_room():
    df = pd.read_csv("hospital.csv", delimiter="\|")
    df.columns = ["idx", "first_name", "last_name", "age", "personal_id", "lnum", "bt", "symp"]
    df[['symp']] = df[['symp']].fillna(value='N/A')
    df['isolate'] = (df['bt'] > 37.5) | (df['symp'] == 'cough')
    df['covid_positive'] = df.age.apply(
        lambda x: np.random.choice([0, 1], p=[0.8, 0.2]) if x <= 16 else np.random.choice([0, 1], p=[
            1 - min(0.8, max(0.25, x / 100)), min(0.8, max(0.25, x / 100))]))
    df['recovered'] = df.apply(lambda x: give_treatment(x), axis=1)

def generate_nurse_report():
    report = pd.DataFrame({
        "Ratio of COVID patients from total patients": [df[df.covid_positive == 1].shape[0] / df.shape[0]],
         "Ratio of COVID patients from patients with symptoms": [df[df.covid_positive == 1].shape[0] / df[df.isolate == True].shape[0]],
         "Ratio of COVID children from total children patients": [df[(df.age <= 16) & (df.covid_positive == 1)].shape[0] / df[(df.age <= 16)].shape[0]],
         "Ratio of COVID senior citizens (above 65) from total patients": [df[(df.age > 65) & (df.covid_positive == 1)].shape[0] / df.shape[0]]
                                 })
    return report

if __name__ == '__main__':
    df = pd.read_csv("hospital.csv", delimiter="\|")
    df.columns = ["idx", "first_name", "last_name", "age", "personal_id", "lnum", "bt", "symp"]
    df[['symp']] = df[['symp']].fillna(value='N/A')
    df['isolate'] = (df['bt'] > 37.5) | (df['symp'] == 'cough')
    df['covid_positive'] = df.age.apply(lambda x: np.random.choice([0, 1], p=[0.8, 0.2]) if x <= 16 else np.random.choice([0, 1], p=[1 - min(0.8, max(0.25, x / 100)), min(0.8, max(0.25, x / 100))]))
    df['recovered'] = df.apply(lambda x: give_treatment(x), axis=1)

    nurse_report = pd.DataFrame({
        "Ratio of COVID patients from total patients": [df[df.covid_positive == 1].shape[0] / df.shape[0]],
         "Ratio of COVID patients from patients with symptoms": [df[df.covid_positive == 1].shape[0] / df[df.isolate == True].shape[0]],
         "Ratio of COVID children from total children patients": [df[(df.age <= 16) & (df.covid_positive == 1)].shape[0] / df[(df.age <= 16)].shape[0]],
         "Ratio of COVID senior citizens (above 65) from total patients": [df[(df.age > 65) & (df.covid_positive == 1)].shape[0] / df.shape[0]]
                                 })

    # doctor_report = pd.DataFrame(
    #     {
    #         "Total ratio of recovered COVID patients": [df[df.recovered == 1].shape[0] / df[df.covid_positive == 1].shape[0]],
    #         "Ratio of COVID recovered children": [df[(df.age <= 16) & (df.recovered == 1)].shape[0] / df[(df.age <= 16)
    #                                                                                                      & (df.covid_positive == 1)].shape[0]],
    #         "Ratio of COVID senior citizens": [
    #             df[(df.age > 65) & (df.recovered == 1)].shape[0] / df[(df.age > 65) & (df.covid_positive == 1)].shape[
    #                 0]]
    #     }
    # )

    print("Done")