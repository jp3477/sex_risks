from select_patients import fetch_patients
from psm_model_rf import run_rf_model


def main():
    fetch_patients()
    run_rf_model()


if __name__ == '__main__':
    main()