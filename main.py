from mastercomapi import Mastercom
import logging


def main():
    student = Mastercom(
        instance="",
        password="",
        username="",
        base_url="",
        stripe_mid="",
        stripe_sid="",
        store_token=True,
    ).get_student()

    timetable = student.get_grades()

    for period in timetable:
        print(period.to_dict())


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.WARN,
        format="%(asctime)s :: [%(name)s] [%(levelname)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler()],
    )

    main()
