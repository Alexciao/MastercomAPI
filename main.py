from mastercomapi import Mastercom
import logging


def main():
    student = Mastercom(
        instance="steam-bo",
        password="udscgmz498",
        username="898004",
        base_url="https://steam-bo-sito.registroelettronico.com",
        stripe_mid="d38a02cc-45ef-4064-8800-afa82d6b60659db487",
        stripe_sid="135ac403-8009-4bbd-98fa-5a6a09f56717c446e8",
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
