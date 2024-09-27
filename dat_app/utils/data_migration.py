import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dat.settings")
django.setup()
import pymysql
from dat_app import models
from dat_app.utils.dat_test import count_dat
# from django.conf import settings


def migrate_data():
    db = pymysql.connect(
        host='8.138.12.232',
        user='root',
        port=20308,
        password='wcaM6zg4532e',
        database='dat_test',
        charset='utf8mb4'
    )
    cursor = db.cursor()

    select_sql = "select * from `dat` where id > 3"
    cursor.execute(select_sql)
    results = cursor.fetchall()

    for result in results:
        # word1-10
        word1 = result[6]
        word2 = result[7]
        word3 = result[8]
        word4 = result[9]
        word5 = result[10]
        word6 = result[11]
        word7 = result[12]
        word8 = result[13]
        word9 = result[14]
        word10 = result[15]
        # score

        # effective_num

        # username
        username = result[4]
        # limited_time
        limited_time = 240

        instance = models.dat_test.objects.create(
            word1=word1, word2=word2,
            word3=word3, word4=word4,
            word5=word5, word6=word6,
            word7=word7, word8=word8,
            word9=word9, word10=word10,
            username=username,
            limited_time=limited_time
        )
        instance.save()
        data_dict = {"word1": word1, "word2": word2, "word3": word3, "word4": word4, "word5": word5, "word6": word6,
                     "word7": word7, "word8": word8, "word9": word9, "word10": word10}
        respond_dict = count_dat(data_dict, username)
        instance.dat_score = respond_dict["dat_score"]
        instance.effective_num = respond_dict["effective_num"]
        instance.picture_path = respond_dict["filepath"]
        instance.save()
        print(data_dict)


if __name__ == "__main__":
    migrate_data()
